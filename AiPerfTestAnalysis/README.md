
# 🧠 AI-Powered Performance Report Analyzer

This project is an AI-enhanced tool that **automatically analyzes JMeter performance test results and logs**, leveraging **Google's Gemini LLM** to generate actionable infrastructure and optimization recommendations.

---

## 🚀 Features

- 📈 Parses performance metrics from JMeter summary JSON.
- ⚠️ Analyzes JMeter logs for warnings and errors.
- 🤖 Uses Google Gemini LLM to:
  - Detect performance bottlenecks.
  - Suggest scaling and tuning strategies.
- 🛠️ API endpoint to automate report analysis (`/analyse`).
- 📂 File-based input for integration with CI/CD or load testing pipelines.

---

## 📁 Project Structure

```
AiPerfTesting/
│
├── .env                            # API keys and model config
├── main.py                         # Flask app entry point
├── requirements.txt                # Python dependencies
│
├── src/
│   ├── inputs/
│   │   ├── jmeter.log              # Sample JMeter log file
│   │   └── summary.json            # Sample summary report (Total metrics)
│   │
│   ├── pipeline/
│   │   └── report_parser.py        # Core logic: log parsing + Gemini prompt
│   │
│   └── utils/
│       ├── constants.py            # Required keys, input dir constant
│       └── templates.py            # Gemini prompt + response format
│
└── README.md
```

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AiPerfTesting.git
cd AiPerfTesting
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root with the following:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_ID=gemini-pro  # or the model you're using
```

---

## 🧪 Sample Input Files

Place your input files in the `/src/inputs/` folder (or provide them through Postman):

- `summary.json` – Should include a `Total` object like:
  ```json
  {
    "Total": {
      "samples": 10000,
      "average": 320,
      "min": 15,
      "max": 1200,
      "errorRate": "2%"
    }
  }
  ```

- `jmeter.log` – Standard JMeter log files (contains `WARN` or `ERROR` lines). # Single or Multiple files 

---

## 🧩 Required JSON Schema for `test_config`

Example:

```json
{
  "context": {
    "test_name": "testplan_1k_user",
    "actual_load": {
      "users": 1000,
      "duration": 60,
      "ramp_up": 30
    },
    "infra": {
      "cpu_cores_per_node": 4,
      "memory_gb_per_node": 8,
      "total_nodes": 3,
      "disk_type": "SSD"
    },
    "expected_validations": {
      "throughput_rps": 350,
      "response_code": 200,
      "max_response_time_ms": 750
    }
  },
  "questions": [
    "What infra improvements would help us meet a 500ms response time SLA?",
    "How can we reach 1000 RPS with minimal additional cost?"
  ],
  "test_feature": "Login + View Order History"
}
```

- `test_feature` – Test Feature Input, Example: "Login + View Order History"

---

## 🚀 Running the Flask Server

```bash
python main.py # Start the Flask server and use postman to test the API

python app.py # Execute the script to run the analysis pipeline directly reading from input files present in the inputs folder
```

- Server starts at: `http://127.0.0.1:5000`

---

## 🧪 Testing with Postman

### Endpoint: `POST /analyse`

**Body Type:** `form-data`

| Key               | Type | Value                          |
|-------------------|------|--------------------------------|
| summary_file      | File | Upload `summary.json`          |
| jmeter_log_file   | File | Upload `jmeter.log`            |
| test_config       | Text | Paste valid JSON string config |

**Sample response:**

```json
{
  "response": {
    "bottlenecks": [],
    "recommendations": [],
    "update_machine": {}
  }
}
```

---

## 🧠 How It Works

1. Parses the uploaded files.
2. Validates test config schema.
3. Extracts key metrics + errors.
4. Craft a structured prompt using a predefined template.
4. Craft a structured prompt using a predefined template.
5. Sends it to Gemini and parses the structured JSON response.
6. Returns recommendations via API.

---