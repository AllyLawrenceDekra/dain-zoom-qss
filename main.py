from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

# Dictionary to store secret tokens for multiple apps
SECRET_TOKENS = {
    "Ghost": "zvZ0YVNaRA-BkSkdpmDXzA",
    "HotDog": "TDrpVlHkQcSnxWmtf-JwHg"
}

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    event_data = request.json

    # Handle Zoom URL validation
    if event_data.get("event") == "endpoint.url_validation":
        plain_token = event_data["payload"].get("plainToken")
        if plain_token:
            # Determine which secret token to use based on a request header or other identifier
            app_id = request.headers.get('App-ID')  # Custom header or parameter to identify the app
            secret_token = SECRET_TOKENS.get(app_id)

            if not secret_token:
                return jsonify({"error": "Invalid or missing App-ID"}), 401

            # Generate the HMAC SHA-256 hash
            encrypted_token = hmac.new(
                secret_token.encode(), 
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

    # For other webhook events
    return jsonify({"message": "Event received"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
