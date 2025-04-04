# GitHub Webhook to Jira Ticket Creation using Flask

This project listens for GitHub issue comments via a **webhook**, and if the comment contains `/jira`, it automatically creates a Jira ticket using a **Flask API**.

---
## 🚀 Features
- Listens for GitHub **issue comments**.
- Checks if the comment contains `/jira`.
- Extracts issue details (title, description, and link).
- Creates a Jira ticket automatically.
- Uses **Flask**, **GitHub Webhooks**, and **Jira API**.

---
## 🏗 Project Structure
```
📂 github-webhook-jira
├── app.py                # Flask API handling GitHub webhooks
├── requirements.txt      # Required dependencies
└── README.md             # Project documentation
```

---
## 🛠 Setup Instructions
### 1️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 2️⃣ Configure Webhook in GitHub
1. Go to your GitHub repository.
2. Navigate to **Settings → Webhooks**.
3. Click **Add Webhook**.
4. In **Payload URL**, enter your Flask API URL (e.g., `http://your-server-ip:5000/createJira`).
5. Select **Content type** as `application/json`.
6. Choose **Just the issue comments event**.
7. Click **Add Webhook**.

### 3️⃣ Start Flask API
```sh
python app.py
```

---
## 🔧 How It Works
1. GitHub sends a `POST` request to `/createJira` whenever someone comments on an issue.
2. Flask API receives the request and extracts:
   - The **comment text** (`/jira` expected)
   - The **issue title & description**
   - The **issue URL**
3. If the comment **exactly matches** `/jira`, the API:
   - Builds a Jira ticket with extracted issue details.
   - Sends a request to **Jira API** to create the ticket.
4. Jira returns a response, which is sent back as a JSON response.

---
## 📜 Code Explanation
### `app.py`
```python
import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/createJira', methods=['POST'])
def createJira():
    # Receive JSON payload from GitHub webhook
    data = request.get_json()
    print("Webhook received:", json.dumps(data, indent=2))

    # Extract the comment text
    comment_body = data.get("comment", {}).get("body", "").strip().lower()

    # Check if comment is exactly "/jira"
    if comment_body != "/jira":
        return { "message": "No /jira command found. Skipping Jira creation." }, 200

    # Extract issue details
    issue_title = data.get("issue", {}).get("title", "No title")
    issue_body = data.get("issue", {}).get("body", "No description provided.")
    issue_url = data.get("issue", {}).get("html_url", "")

    # Build Jira payload
    payload = json.dumps({
        "fields": {
            "project": {"key": "AB"},
            "summary": issue_title,
            "description": {
                "type": "doc", "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": f"{issue_body}\n\nGitHub Issue Link: {issue_url}"}]}]
            },
            "issuetype": {"id": "10006"}
        }
    })

    # Jira API details
    jira_url = "https://your-domain.atlassian.net/rest/api/3/issue"
    jira_email = "your_email@example.com"
    jira_token = "your_jira_api_token_here"

    auth = HTTPBasicAuth(jira_email, jira_token)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(jira_url, headers=headers, data=payload, auth=auth)

    return json.dumps(json.loads(response.text), indent=4), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---
## 📌 Testing the Webhook
You can use a tool like **Postman** or GitHub’s built-in webhook test feature:
1. Go to **GitHub Repository → Settings → Webhooks**.
2. Click **Recent Deliveries**.
3. Check if a `POST` request was sent to your API.
4. If needed, resend the webhook for testing.

---
## 🏆 Conclusion
This project integrates **GitHub Webhooks** with **Jira API** using **Flask**, allowing automated issue tracking.

---
## 📝 Future Improvements
✅ Support multiple Jira projects.
✅ Add logging for better debugging.
✅ Use environment variables for API keys.

---
## 📚 References
- [GitHub Webhooks Docs](https://docs.github.com/webhooks)
- [Jira REST API Docs](https://developer.atlassian.com/cloud/jira/platform/rest/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---
🚀 **Happy Coding!**

