from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Print the request headers
    print("Headers:", request.headers)

    # Print the raw request body
    print("Body:", request.get_data(as_text=True))

    # Respond to Zoom
    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
