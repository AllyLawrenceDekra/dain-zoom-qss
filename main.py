from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

# Your secret token (provided by Zoom when setting up the webhook)
SECRET_TOKEN = "zvZ0YVNaRA-BkSkdpmDXzA"

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    event_data = request.json

    # Handle Zoom URL validation
    if event_data.get("event") == "endpoint.url_validation":
        plain_token = event_data["payload"].get("plainToken")
        if plain_token:
            # Generate the HMAC SHA-256 hash
            encrypted_token = hmac.new(
                SECRET_TOKEN.encode(), 
                plain_token.encode(), 
                hashlib.sha256
            ).hexdigest()

            # Construct the response required by Zoom
            response = {
                "plainToken": plain_token,
                "encryptedToken": encrypted_token
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "Invalid validation request"}), 400

    # For other webhook events (example)
    return jsonify({"message": "Event received"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
