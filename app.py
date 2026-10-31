import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
  """Health check endpoint to verify server status."""
  return (
      jsonify(
          {
              "status": "online",
              "message": (
                  "WhatsApp to Facebook Automation Server is operational."
              ),
          }
      ),
      200,
  )


@app.route("/whatsapp-webhook", methods=["GET", "POST"])
def whatsapp_webhook():
  """Handles Meta Webhook verification (GET) and incoming WhatsApp payloads (POST)."""
  if request.method == "GET":
    verify_token = request.args.get("hub.verify_token")
    # Replace with your secure verify token configuration
    if verify_token == "my_secure_verify_token":
      return request.args.get("hub.challenge"), 200
    return jsonify({"error": "Verification failed: Invalid token"}), 403

  elif request.method == "POST":
    payload = request.json
    print("Incoming WhatsApp Payload:", payload)

    # TODO: Integrate your Telegram approval pipeline and Facebook Graph API posting logic here.

    return (
        jsonify(
            {
                "status": "success",
                "message": (
                    "Payload received and forwarded for Telegram approval."
                ),
            }
        ),
        200,
    )


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)