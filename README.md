# Webhook Listener & Dashboard

This repo contains a Flask-based webhook server that listens for GitHub events and stores them in MongoDB. It also includes a UI dashboard to view webhook activities.

### Features
- Handles `push`, `pull_request`, and `merge` events
- Saves events with author, branch info, and timestamp
- Stores data in MongoDB
- AJAX-based dashboard that auto-refreshes every 15 seconds

### Tech Stack
- Flask (Python)
- MongoDB
- HTML + Bootstrap + JavaScript (AJAX)
- Ngrok for exposing local server
