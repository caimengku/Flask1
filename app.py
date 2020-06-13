# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel access token (long-lived)
line_bot_api = LineBotApi('p3J97VWu/jTlaKtXbklSw+uJySd8GHFvwGs/tzSJTNBxNFIVn02El0zmf90nxt7fPMt4B66s3VGa4FwB37j2A591SsowMnSzBdOfOElxe/XQ+upvVifB7VTyPrGwq1duTyXdqQOqFGO/4BbDMvPMkwdB04t89/1O/w1cDnyilFU=')

# Channel secret 
handler = WebhookHandler('d0e35eafb0c19c429166f41375a45240')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

from bs4 import BeautifulSoup
import requests
def movie():
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmListAll a')):
        if index == 20:
            break
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n'.format(title, link)
    return content


def getNews():
    """
    建立一個抓最新消息的function
    """
    import requests
    import re
    from bs4 import BeautifulSoup

    url = 'https://www.ettoday.net/news/focus/3C%E5%AE%B6%E9%9B%BB/'
    r = requests.get(url)
    reponse = r.text

    url_list = re.findall(r'<h3><a href="/news/[\d]*/[\d]*.htm" .*>.*</a>',reponse)

    soup = BeautifulSoup(url_list[0])
    url = 'https://fashion.ettoday.net/' + soup.find('a')['href']
    title = soup.text


    tmp = title + ': ' +url
    return tmp


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 傳送文字
    if event.message.text == '傳送文字':
        message = TextSendMessage(getNews())
    # 傳送圖片
    elif event.message.text == '我要圖片':
        message = ImageSendMessage(
            original_content_url='https://i.imgur.com/QPJ8A1b.png',
            preview_image_url='https://i.imgur.com/QPJ8A1b.png'
        )

     # 傳送新聞連結
    elif event.message.text == '新聞':
        message = TextSendMessage(getNews())
        
    elif event.message.text == "選單":
        Carousel_template = TemplateSendMessage(
        alt_text='選單',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://imgur.com/a/rIeZFES',
                title='this is menu1',
                text='description1',
                actions=[
                    PostbackTemplateAction(
                        label='postback1',
                        text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message1',
                        text='message text1'
                    ),
                    URITemplateAction(
                        label='新聞連結',
                        uri='https://www.ettoday.net/news/20200613/1737170.htm'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://imgur.com/a/rIeZFES',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackTemplateAction(
                        label='postback2',
                        text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageTemplateAction(
                        label='message2',
                        text='message text2'
                    ),
                    URITemplateAction(
                        label='連結2',
                        uri='http://example.com/2'
                    )
                ]
            )
        ]
    )
    )
    
        
        
        
    # 傳送貼圖
    elif event.message.text == '傳送貼圖':
        message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

    
if __name__ == '__main__':
    app.run(debug=True)