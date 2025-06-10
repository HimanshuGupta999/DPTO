from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILES_DIR = ROOT / "inputs"
OUTPUT_FILES_DIR = ROOT / "outputs"

OUTPUT_FILE = OUTPUT_FILES_DIR / "analysis_recommendations.json"
LOG_FILE = OUTPUT_FILES_DIR / "run.log"

SUMMARY_FILE = INPUT_FILES_DIR / "statistics.json"
TEST_CONFIG_FILE = INPUT_FILES_DIR / "test_config.json"

CONTEXT_FILES_PATH = ROOT / "data" / "performance_test_scenarios.csv"

REQUIRED_KEYS = [
    'test_name',
    'actual_load',
    'infra',
    'expected_validations',
]
