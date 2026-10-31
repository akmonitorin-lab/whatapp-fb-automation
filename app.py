import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuration parameters (Telegram Bot)
TELEGRAM_BOT_TOKEN = "9131637655:AAHvH-Zn_BWLLGGMvQmmp_jvUa586G2N41k"  #[span_3](start_span)[span_3](end_span)
TELEGRAM_CHAT_ID = "5311023300"  #[span_4](start_span)[span_4](end_span)

# Meta Graph API Credentials (Bajwa fans Page)
PAGE_ID = "139559419030947"  #[span_5](start_span)[span_5](end_span)[span_6](start_span)[span_6](end_span)
ACCESS_TOKEN = (
    "EAA6ijRcRE1YBS0gLKErceabW2E6Eb1Kxwbv8aSV1bmgTJF265dE6XCcDJGDOjsbvIaL3WO6lpNzBxNPgP6w2kGcsZBVXi5aZBRXPNOGLY9E8tnJ8FxRs6nHAHupwIPgZA4dHhz1PYC6FXQUKK6AemLJBhmvuHZCurXaiCwNgBy53F7a4l8hxmZC6lxHiv657lM86WZCpOXrhm4sCuPINSkRokvZAUgCvZBfFBJVDdvB78kGjOe3CzheH2poZD"
)


def publish_to_facebook(image_url, caption):
  # Facebook Page par photo post karne ke liye request
  fb_url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"
  fb_payload = {"url": image_url, "caption": caption, "access_token": ACCESS_TOKEN}
  response = requests.post(fb_url, data=fb_payload)
  print("Facebook Response:", response.json())
  return response.json()


def send_approval_request(image_url, user_caption):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

  topic_hashtags = "#BreakingNews #ViralUpdate #CurrentAffairs"
  location_tag = "#Bahraich"
  final_caption = f"{user_caption}\n.\n.\n.\n{topic_hashtags} {location_tag}"

  keyboard = {
      "inline_keyboard": [[
          {"text": "✅ Approve & Post", "callback_data": "approve_post"},
          {"text": "❌ Reject", "callback_data": "reject_post"},
      ]]
  }

  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "photo": image_url,
      "caption": final_caption,
      "reply_markup": keyboard,
  }

  response = requests.post(url, json=payload)
  return response.json()


@app.route("/whatsapp-webhook", methods=["POST"])
def whatsapp_webhook():
  data = request.json
  incoming_caption = data.get("caption", "Default Update")
  image_url = data.get(
      "image_url",
      "https://via.placeholder.com/600",
  )

  send_approval_request(image_url, incoming_caption)
  return (
      jsonify(
          {
              "status": "Success",
              "message": "Forwarded to Telegram for approval.",
          }
      ),
      200,
  )


if __name__ == "__main__":
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)