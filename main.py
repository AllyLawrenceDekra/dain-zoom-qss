from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store verification tokens for multiple apps
SECRET_TOKENS = {
    "Ghost": "zvZ0YVNaRA-BkSkdpmDXzA",
}

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Parse the incoming request
    event_data = request.json

    # Handle Zoom URL validation
    if event_data.get("event") == "endpoint.url_validation":
        plain_token = event_data["payload"].get("plainToken")
        if plain_token:
            # Respond with the plainToken as required by Zoom
            return jsonify({"plainToken": plain_token}), 200
        else:
            return jsonify({"error": "Invalid validation request"}), 400

    # Extract the token from the Authorization header for other requests
    received_token = request.headers.get('Authorization')

    if not received_token:
        return jsonify({"error": "Missing token"}), 401

    # Check if the token matches any in the mapping
    account_id = next((key for key, value in SECRET_TOKENS.items() if value == received_token), None)

    if not account_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Log or process the event for the identified account
    print(f"Received event for {account_id}: {event_data}")

    # Process the event as needed (e.g., saving to a database)
    return jsonify({"status": "received", "account_id": account_id}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
