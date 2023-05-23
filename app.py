from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent)
def handle_message(event):
	if (event.message.type == "image"):
		SendImage = line_bot_api.get_message_content(event.message.id)

		local_save = './static/' + event.message.id + '.png'
		with open(local_save, 'wb') as fd:
			for chenk in SendImage.iter_content():
				fd.write(chenk)
                
		line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url = ngrok_url + "/static/" + event.message.id + ".png", preview_image_url = ngrok_url + "/static/" + event.message.id + ".png"))
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
