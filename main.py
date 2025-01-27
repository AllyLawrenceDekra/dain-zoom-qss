from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store verification tokens for multiple apps
ZOOM_TOKENS = {
    "Ghost": "token_for_app_1",
    "Hotdog": "token_for_app_2",
}

@app.route('/webhook', methods=['POST'])
def zoom_webhook():
    # Get the token from the request header
    auth_header = request.headers.get('Authorization')

    # Validate the token
    if auth_header not in ZOOM_TOKENS.values():
        return jsonify({"error": "Unauthorized"}), 401

    # Identify the app based on the token
    app_name = [key for key, token in ZOOM_TOKENS.items() if token == auth_header][0]
    print(f"Request received from {app_name}")

    # Parse incoming event data
    event_data = request.json
    print(f"Event Data from {app_name}: {event_data}")

    # Respond to Zoom
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
