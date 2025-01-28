from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Log headers and body for debugging
    print("Headers:", dict(request.headers))
    print("Body:", request.get_data(as_text=True))

    # Extract the secret token from the x-dain-key header
    secret_token = request.headers.get("x-dain-key")
    if not secret_token:
        return jsonify({"error": "Missing secret token in x-dain-key header"}), 401

    # Parse the request body
    event_data = request.json

    # Handle Zoom URL validation
    if event_data.get("event") == "endpoint.url_validation":
        plain_token = event_data["payload"].get("plainToken")
        if not plain_token:
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

        return jsonify(response), 200

    # Handle `phone.call_qos` event
    if event_data.get("event") == "phone.call_qos":
        # Extract details from the event payload
        call_qos_data = event_data.get("payload", {})
        call_id = call_qos_data.get("callId", "Unknown")
        user_id = call_qos_data.get("userId", "Unknown")
        qos_metrics = call_qos_data.get("qos", {})

        # Log or process the QoS data
        print(f"Call QoS Event Received - Call ID: {call_id}, User ID: {user_id}")
        print("QoS Metrics:", qos_metrics)

        # Respond to Zoom
        return jsonify({"message": "QoS event received", "callId": call_id}), 200

    # Handle other events
    print("Received event:", event_data)
    return jsonify({"message": "Event received"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
