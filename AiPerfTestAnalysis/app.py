import os
import json
import sys
from dotenv import load_dotenv
from src.utils.constants import REQUIRED_KEYS, CONTEXT_FILES_PATH, INPUT_FILES_DIR, SUMMARY_FILE, TEST_CONFIG_FILE, \
    OUTPUT_FILE, OUTPUT_FILES_DIR, LOG_FILE
from src.pipeline.report_parser import ReportParser
from src.utils.helpers import get_logger

load_dotenv()

logger = get_logger(LOG_FILE)

src_path = os.environ.get("PYTHONPATH", "")
if src_path and src_path not in sys.path:
    sys.path.append(src_path)


def find_log_files(directory):
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".log")
    ]

def main():
    if not os.path.exists(SUMMARY_FILE):
        logger.error(f"Missing summary file: {SUMMARY_FILE}")
        return

    if not os.path.exists(TEST_CONFIG_FILE):
        logger.error(f"Missing test_config file: {TEST_CONFIG_FILE}")
        return

    jmeter_log_files = find_log_files(INPUT_FILES_DIR)
    if not jmeter_log_files:
        logger.error("No JMeter .log files found in the inputs/ directory.")
        return

    try:
        with open(TEST_CONFIG_FILE, 'r') as f:
            test_context = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in test_config.json: {e}")
        return

    context_data = test_context.get("context", {})
    missing_keys = [key for key in REQUIRED_KEYS if key not in context_data]
    if missing_keys:
        logger.error(f"Missing required keys in test_config['context']: {missing_keys}")
        return

    test_feature = test_context.get("test_feature", "").strip()
    if not test_feature:
        logger.error("'test_feature' is missing or empty in test_config.json")
        return

    try:
        logger.info("Starting report analysis")
        report_parser = ReportParser(
            test_and_infra_details=test_context,
            summary_file_path=SUMMARY_FILE,
            jmeter_log_paths=jmeter_log_files,
            context_file_path=CONTEXT_FILES_PATH,
            test_feature=test_feature
        )
        analysis = report_parser.get_analysis()
        recommendations = analysis.get("recommendation", {})

        logger.info("\nSaving Analysis")
        os.makedirs(OUTPUT_FILES_DIR, exist_ok=True)
        with open(OUTPUT_FILE, "w") as out_f:
            json.dump(recommendations, out_f, indent=2)

        logger.info("\nSaved analysis successfully")

    except Exception as e:
        logger.exception(f"Failed to analyze report: {str(e)}")

if __name__ == "__main__":
    main()
