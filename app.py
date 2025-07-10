from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask import render_template_string
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["webhookDB"]
collection = db["events"]

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        payload = request.get_json()
        event_type = request.headers.get("X-GitHub-Event", "ping")

        print(f"Received event: {event_type}")

        timestamp = datetime.now().isoformat()
        author = payload.get("sender", {}).get("login", "unknown")

        if event_type == "push":
            to_branch = payload.get("ref", "").split("/")[-1]
            event_data = {
                "type": "push",
                "author": author,
                "to_branch": to_branch,
                "timestamp": timestamp
            }
            collection.insert_one(event_data)
            print("Push event saved to MongoDB.")

        elif event_type == "pull_request":
            action = payload.get("action")
            pr = payload.get("pull_request", {})
            from_branch = pr.get("head", {}).get("ref", "")
            to_branch = pr.get("base", {}).get("ref", "")
            merged = pr.get("merged", False)

            if action == "opened":
                event_data = {
                    "type": "pull_request",
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": timestamp
                }
                collection.insert_one(event_data)
                print("PR Opened event saved.")

            elif action == "closed" and merged:
                event_data = {
                    "type": "pull_request",
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": timestamp,
                    "merged": True
                }
                collection.insert_one(event_data)
                print("PR Merged event saved.")

        return jsonify({"message": "Webhook received"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route("/events", methods=["GET"])
def get_events():
    try:
        events = list(collection.find({}, {"_id": 0}))
        return jsonify(events), 200
    except Exception as e:
        print("Error fetching events:", e)
        return jsonify({"error": "Failed to fetch events"}), 500

@app.route("/")
def home():
    with open("ui/dashboard.html", "r", encoding="utf-8") as file:
        html = file.read()
    return render_template_string(html)


if __name__ == "__main__":
    app.run(port=5000)
