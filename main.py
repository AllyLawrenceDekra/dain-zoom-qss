from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store verification tokens for multiple apps
ZOOM_TOKENS = {
    "Ghost": "zvZ0YVNaRA-BkSkdpmDXzA",
}

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Extract the token from the Authorization header
    received_token = request.headers.get('Authorization')

    if not received_token:
        return jsonify({"error": "Missing token"}), 401

    # Check if the token matches any in the mapping
    account_id = next((key for key, value in SECRET_TOKENS.items() if value == received_token), None)

    if not account_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Log or process the event for the identified account
    event_data = request.json
    print(f"Received event for {account_id}: {event_data}")

    # Process the event as needed (e.g., saving to a database)
    return jsonify({"status": "received", "account_id": account_id}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
