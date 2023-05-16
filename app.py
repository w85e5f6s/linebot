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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text
    if input_text == "查匯率":
        resp = requests.get('https://tw.rter.info/capi.php')
        currency_data = resp.json()
        usd_to_twd = currency_data['USDTWD']['Exrate']
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'美元 USD 對台幣 TWD：1:{usd_to_twd}'))
    elif input_text == '現在時間':
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=f"台北時間：{current_time}"))
    elif input_text == "現在幾度" elif input_text == "現在幾度" or input_text == "溫度":
        Rdata = requests.get(
            'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=ABC-#@12345324-KEY-1233-1237485723&locationName=%E8%87%BA%E5%8C%97,&elementName=TEMP&parameterName=CITY').json()
        Temp = Rdata["records"]["location"][0]["weatherElement"]
        Mdict = dict(enumerate(Temp))
        o1 = Mdict[0]['elementValue']
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'現在「台北」的目前溫度是：{o1}'))
    elif input_text == "股票":

        stock(x)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'現在「股票號碼{stock} 」的目前股價是：{getstock}'))
