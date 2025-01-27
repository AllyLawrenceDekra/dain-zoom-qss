from flask import Flask, request, jsonify
import time  # For generating event_ts

app = Flask(__name__)

# Dictionary to store verification tokens for multiple apps
SECRET_TOKENS = {
    "Ghost": "zvZ0YVNaRA-BkSkdpmDXzA",
}

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    event_data = request.json

    # Handle Zoom URL validation
    if event_data.get("event") == "endpoint.url_validation":
        plain_token = event_data["payload"].get("plainToken")
        if plain_token:
            # Construct the response required by Zoom
            response = {
                "payload": {
                    "plainToken": plain_token
                },
                "event_ts": int(time.time() * 1000),  # Current timestamp in milliseconds
                "event": "endpoint.url_validation"
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "Invalid validation request"}), 400

    # For other events, validate the secret token
    received_token = request.headers.get('Authorization')

    if not received_token:
        return jsonify({"error": "Missing token"}), 401

    # Check if the received token matches any known secret token
    account_id = next((key for key, value in SECRET_TOKENS.items() if value == received_token), None)

    if not account_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Log or process the event for the identified account
    print(f"Received event for {account_id}: {event_data}")

    # Respond to valid requests
    return jsonify({"status": "received", "account_id": account_id}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
