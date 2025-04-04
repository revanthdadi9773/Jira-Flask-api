import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Jira Credentials (Hardcoded for now)
JIRA_URL = "https://dadirevanth9773-1742278721180.atlassian.net/rest/api/3/issue"
JIRA_EMAIL = "dadirevanth9773@gmail.com"
JIRA_API_TOKEN = "ATATT3xFfGF0GE8SEocVAWSFllIJ-mZfE5QsNqJUHY51hIDltTU_suYMmnAjn95UHu7uPQRUw48XsT9Jy-Grt4S9dG3I1QdzpQFdCcrtr8jYWT8LqYHvQuBqRY6BvcbNXZLnQIvWC4dqtOjpy54erirNlMdruupLYnY8vDwbMIuBkx2vLmwm_i8=B684D7BD"

# Jira Project & Issue Type (Update if needed)
JIRA_PROJECT_KEY = "SCRUM"  # Ensure this is correct in Jira
JIRA_ISSUE_TYPE_ID = "10003"  # Verify this ID in your Jira settings

@app.route('/createJira', methods=['POST'])
def createJira():
    """Handles GitHub webhook and creates a Jira issue if '/jira' is commented."""

    # Ensure JSON payload
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Use application/json"}), 415

    # Parse incoming JSON
    data = request.get_json()
    print("Webhook received:", json.dumps(data, indent=2))  # Debugging

    # Extract and check the comment
    comment_body = data.get("comment", {}).get("body", "").strip().lower()
    if comment_body != "/jira":
        return jsonify({"message": "No /jira command found. Skipping Jira creation."}), 200

    # Extract issue details
    issue_title = data.get("issue", {}).get("title", "No title provided")
    issue_body = data.get("issue", {}).get("body", "No description available.")
    issue_url = data.get("issue", {}).get("html_url", "No URL available")

    # Construct Jira issue payload
    payload = json.dumps({
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": issue_title,
            "description": f"{issue_body}\n\nGitHub Issue: {issue_url}",
            "issuetype": {"id": JIRA_ISSUE_TYPE_ID}
        }
    })

    # Send Jira API request
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    response = requests.post(JIRA_URL, headers=headers, data=payload, auth=auth)

    # Handle API response
    try:
        response_json = response.json()
        print("Jira API Response:", json.dumps(response_json, indent=2))  # Debugging
        if response.status_code == 201:
            return jsonify({"message": "Jira issue created successfully", "jira_response": response_json}), 201
        else:
            return jsonify({"error": "Failed to create Jira issue", "jira_response": response_json}), response.status_code
    except json.JSONDecodeError:
        return jsonify({"error": "Jira API response is not valid JSON", "response_text": response.text}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
