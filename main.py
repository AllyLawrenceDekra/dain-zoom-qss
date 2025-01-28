from flask import Flask, request, jsonify
import hmac
import hashlib
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global variable to store the secret token
SECRET_TOKEN = None  # Will be set dynamically during validation

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    global SECRET_TOKEN
    event_data = request.json

    # Extract the Authorization header
    received_token = request.headers.get('Authorization')

    # Handle Zoom URL validation
    if event_data.get("event") == "endpoint.url_validation":
        plain_token = event_data["payload"].get("plainToken")
        if plain_token:
            # Set the SECRET_TOKEN dynamically if it's not already set
            if not SECRET_TOKEN and received_token:
                SECRET_TOKEN = received_token
                logging.info(f"Secret token captured: {SECRET_TOKEN}")

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
            logging.error("Invalid validation request: plainToken missing")
            return jsonify({"error": "Invalid validation request"}), 400

    # For other events, validate the secret token
    if not received_token or received_token != SECRET_TOKEN:
        logging.warning("Unauthorized request: Invalid or missing token")
        return jsonify({"error": "Unauthorized"}), 401

    # Log or process the event payload
    event_type = event_data.get("event")
    payload = event_data.get("payload")

    if event_type == "phone.call_qos":
        # Log the phone.call_qos payload
        logging.info("Received phone.call_qos event payload:")
        logging.info(payload)

    # Respond to all valid requests
    logging.info(f"Received event: {event_type}")
    return jsonify({"status": "Event received"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
