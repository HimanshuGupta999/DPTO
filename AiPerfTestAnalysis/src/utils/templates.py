REPORT_ANALYSIS_PROMPT = """
You are an expert AI Agent specialized in performance testing analysis. Your task is to analyze and interpret the 
performance testing summary report, infrastructure details, and test configurations provided below.

Inputs:
- Summary Report: {SUMMARY}
- Test and Infrastructure Details (from CSV): {TEST_AND_INFRA_DETAILS}
- JMeter Logs: {JMETER_LOGS}
- Contextual Information: {CONTEXT_DATA}
- Test Feature Under Evaluation: {TEST_FEATURE}

Your objective:
1. Identify performance bottlenecks, anomalies, or inefficient resource usage.
2. Recommend **infrastructure scaling strategies** (e.g., increase CPU cores, memory, instances, etc.).
3. Suggest **performance optimization techniques** (e.g., caching, connection pooling, rate limiting).
4. Propose specific machine-level updates such as CPU, memory, or disk changes.
4. Propose specific machine-level updates such as CPU, memory, or disk changes.
5. If the system is well-performing, confirm that no scaling is currently needed and provide reasons.
6. Answer the following **custom evaluation questions** related to the system’s performance and behavior:
{CUSTOM_QUESTIONS}

Additional Context:
Use the provided CONTEXT_DATA and TEST_FEATURE to align recommendations with system behavior, application architecture, 
usage patterns, and expected performance baselines. Adjust recommendations depending on the nature of the feature under 
test (e.g., login, search, checkout, etc.), as each has different performance characteristics and scaling needs.

Output Requirements:
- Format: JSON only (strictly no extra explanation).
- Keep responses concise and structured.
- Use **numeric representation** where applicable (e.g., response time thresholds, CPU utilization %, TPS).
- Justifications in `"recommendations"` and `"update_machine"` must reference the `{CONTEXT_DATA}` or `{TEST_FEATURE}` where applicable (e.g., model behavior, known bottlenecks, infra design).
- Highlight issues using short bullet points and provide **specific, actionable recommendations**.
- Avoid lengthy or verbose sentences.

Make sure the output JSON includes:
- "bottlenecks": [List of detected performance issues]
- "recommendations": [List of scaling/optimization suggestions]
- "update_machine": {{suggested changes to CPU, memory, disk, or other infra specs}}
- "custom_question_responses": {{answers to the CUSTOM_QUESTIONS}}

Be analytical, precise, and data-driven in your response.

Example JSON Output:
{ANALYSIS_RESPONSE_FORMAT}
"""

ANALYSIS_RESPONSE_FORMAT = """
{
  "bottlenecks": [
    {
      "component": "<component_name>",
      "severity": "<low|medium|high>",
      "phase": "<ramp_up|steady_state|cool_down|all>",
      "description": "<short summary of the issue>",
      "evidence": [
        "<brief evidence from logs or metrics>",
        "<affected files or services>"
      ]
    }
    // Repeat for multiple bottlenecks
  ],
  "recommendations": {
    "infra": [
      {
        "priority": "<low|medium|high>",
        "action": "<infrastructure change or addition>",
        "reason": "<why this change is recommended>"
      }
    ],
    "application": [
      {
        "priority": "<low|medium|high>",
        "action": "<code-level or design-level change>",
        "reason": "<justification based on observed behavior>"
      }
    ],
    "config": [
      {
        "priority": "<low|medium|high>",
        "action": "<config parameter tuning>",
        "reason": "<performance or stability optimization>"
      }
    ],
    "api_gateway": [
      {
        "priority": "<low|medium|high>",
        "action": "<gateway-related setting or rule>",
        "reason": "<traffic shaping or error prevention>"
      }
    ]
  },
  "infra_suggestions": {
    "cpu_cores_per_node": {
      "current": <integer>,
      "suggested": <integer>,
      "note": "<reason for change>"
    },
    "memory_gb_per_node": {
      "current": <integer>,
      "suggested": <integer>,
      "note": "<reason for change>"
    },
    "disk_type": {
      "current": "<e.g., SSD>",
      "suggested": "<e.g., NVMe>",
      "note": "<justification>"
    },
    "network_bandwidth": {
      "current": "<e.g., 1Gbps>",
      "suggested": "<e.g., 10Gbps>",
      "note": "<rationale>"
    }
  },
  "answers": [
    {
      "question": "<performance-related or diagnostic question>",
      "answer": "<short direct answer>",
      "evidence": [
        "<log excerpts, metrics or test results>"
      ],
      "real_world_guidance": "<general takeaway or practical advice>"
    }
    // Repeat for multiple Q&A
  ],
  "test_validation_analysis": {
    "details": {
      "concurrent_users": {
        "expected": <integer>,
        "actual": <integer>,
        "status": "<Pass|Fail|Warning>",
        "note": "<additional context>"
      },
      "throughput_rps": {
        "expected": <integer>,
        "actual": <integer>,
        "status": "<Pass|Fail|Warning>",
        "note": "<additional context>"
      },
      "max_retries": {
        "expected": <integer>,
        "actual": <integer>,
        "status": "<Pass|Fail|Warning>",
        "note": "<additional context>"
      },
      "response_code": {
        "expected": <integer>,
        "actual": <integer>,
        "status": "<Pass|Fail|Warning>"
      },
      "max_response_time_ms": {
        "expected": <integer>,
        "actual": <integer>,
        "status": "<Pass|Fail|Warning>",
        "note": "<optional extra comment>"
      }
    }
  },
  "test_feature_justification": {
    "feature_name": "<name of the feature, e.g., login, checkout>",
    "characteristics": "<what makes this feature resource-sensitive or performance-sensitive>",
    "expected_load_behavior": "<expected user pattern or load behavior>",
    "recommendation_alignment": "<how the above influenced infra or optimization recommendations>"
  }
}
"""