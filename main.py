import logging
from flask import Flask, request, jsonify
import hmac
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Log headers and body for debugging
    logging.info("Headers: %s", dict(request.headers))
    logging.info("Body: %s", request.get_data(as_text=True))

    # Extract the secret token from the x-dain-key header
    secret_token = request.headers.get("x-dain-key")
    if not secret_token:
        logging.error("Missing secret token in x-dain-key header")
        return jsonify({"error": "Missing secret token in x-dain-key header"}), 401

    # Parse the request body
    event_data = request.json

    # Handle Zoom URL validation
    if event_data.get("event") == "endpoint.url_validation":
        plain_token = event_data["payload"].get("plainToken")
        if not plain_token:
            logging.error("Missing plainToken in request body")
            return jsonify({"error": "Missing plainToken in request body"}), 400

        # Generate the HMAC SHA-256 hash
        encrypted_token = hmac.new(
            secret_token.encode(),    # Secret token as the key (salt)
            plain_token.encode(),     # plainToken as the message
            hashlib.sha256            # HMAC SHA-256 algorithm
        ).hexdigest()

        # Construct the response required by Zoom
        response = {
            "plainToken": plain_token,
            "encryptedToken": encrypted_token
        }

        logging.info("URL validation successful")
        return jsonify(response), 200


    # Log other events
    logging.info("Received event: %s", event_data)
    return jsonify({"message": "Event received"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
