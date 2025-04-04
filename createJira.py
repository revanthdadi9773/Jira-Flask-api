import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/createJira', methods=['POST'])
def createJira():
    # Step 1: Receive JSON payload from GitHub webhook
    data = request.get_json()
    print("Webhook received:", json.dumps(data, indent=2))  # For debugging

    # Step 2: Get comment body (if exists)
    comment_body = data.get("comment", {}).get("body", "").strip().lower()

    # Step 3: Check if comment is exactly "/jira"
    if comment_body != "/jira":
        return { "message": "No /jira command found in comment. Skipping Jira creation." }, 200

    # Step 4: Extract issue details from webhook payload
    issue_title = data.get("issue", {}).get("title", "No title")
    issue_body = data.get("issue", {}).get("body", "No description provided.")
    issue_url = data.get("issue", {}).get("html_url", "")

    # Step 5: Build Jira ticket payload
    payload = json.dumps({
        "fields": {
            "project": {
                "key": "AB"  # Replace with your Jira project key
            },
            "summary": issue_title,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"{issue_body}\n\nGitHub Issue Link: {issue_url}"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "id": "10006"  # Replace with your issue type ID
            }
        }
    })

    # Step 6: Send POST request to Jira API
    jira_url = "https://veeramallaabhishek.atlassian.net/rest/api/3/issue"
    jira_email = "your_email@example.com"           # Replace with your Jira email
    jira_token = "your_jira_api_token_here"         # Replace with your Jira API token

    auth = HTTPBasicAuth(jira_email, jira_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(jira_url, headers=headers, data=payload, auth=auth)

    # Step 7: Return response from Jira
    return json.dumps(json.loads(response.text), indent=4), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
