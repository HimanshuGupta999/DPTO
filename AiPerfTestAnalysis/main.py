import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from src.utils.constants import REQUIRED_KEYS, INPUT_FILES_DIR, CONTEXT_FILES_PATH
from src.pipeline.report_parser import ReportParser
import json
import sys

load_dotenv()

src_path = os.environ["PYTHONPATH"]
if src_path and src_path not in sys.path:
    sys.path.append(src_path)


app = Flask(__name__)
@app.route('/analyse', methods=['POST'])
def submit_test_config():
    if 'summary_file' not in request.files or 'jmeter_log_files' not in request.files:
        return jsonify({"error": "Both 'summary_file' and 'jmeter_log_files' are required."}), 400

    summary_file = request.files['summary_file']
    jmeter_log_files = request.files.getlist('jmeter_log_files')  # Get list of jmeter log files

    if len(jmeter_log_files) == 0:
        return jsonify({"error": "'jmeter_log_files' cannot be empty."}), 400

    # Save the summary file
    summary_path = os.path.join(INPUT_FILES_DIR, summary_file.filename)
    summary_file.save(summary_path)

    # Save each JMeter log file and store their paths
    jmeter_log_paths = []
    for jmeter_log_file in jmeter_log_files:
        jmeter_log_path = os.path.join(INPUT_FILES_DIR, jmeter_log_file.filename)
        jmeter_log_file.save(jmeter_log_path)
        jmeter_log_paths.append(jmeter_log_path)

    # Get and parse the test_config from the form data
    test_context = request.form.get('test_config')
    if not test_context:
        return jsonify({"error": "Missing 'test_config' in form data."}), 400

    try:
        test_context = json.loads(test_context)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON in 'test_config': {str(e)}"}), 400

    test_feature = request.form.get('test_feature')
    if not test_feature or not test_feature.strip():
        return jsonify({"error": "Missing or empty 'test_feature' field"}), 400

    missing_keys = [key for key in REQUIRED_KEYS if key not in test_context["context"]]
    if missing_keys:
        return jsonify({
            "error": "Missing required fields in test_config",
            "missing_keys": missing_keys
        }), 400
    try:
        report_parser = ReportParser(
            test_and_infra_details=test_context,
            summary_file_path=summary_path,
            jmeter_log_paths=jmeter_log_paths,
            context_file_path=CONTEXT_FILES_PATH,
            test_feature=test_feature
        )
        analysis = report_parser.get_analysis()

    except Exception as e:
        return jsonify({
            "step": "Report Analysis",
            "status": "failed",
            "error": f"Failed to analyze report: {str(e)}"
        }), 500

    # Return the analysis recommendations
    return jsonify({
        "response": analysis.get("recommendation", {})
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
