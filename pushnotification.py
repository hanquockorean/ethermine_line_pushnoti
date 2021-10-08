from flask import Flask
import requests

from linebot import LineBotApi
from linebot import WebhookHandler

from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage
from linebot.models import AudioSendMessage
from keyinfo import keyLine
import time
class botNotification:
    def __init__(self):
        #self.audio_message = AudioSendMessage( \
        #    original_content_url='https://example.com/original.m4a', \
        #    duration=240000)
        li=keyLine()
        self.ip = ""
        try:
            self.ip = requests.get(li.li_getipadd).content.decode('utf8')
        except:
            pass

        self.outoflist_log = False
        self.outoflist_order = False
        self.cnt_log = int(999)

        self.report_time = time.time()

        cnt = 0
        while cnt < (len(li.li_log_key)): #retry 10s
            try:
                self.channel_log = LineBotApi(li.li_log_key[cnt])
                #self.channel_log_handler = WebhookHandler(li.li_log_token)[i]
                print(self.channel_log.get_bot_info())
            except:
                #time.sleep(1)
                cnt=cnt+1
            else:
                self.cnt_log = self.channel_log.get_message_quota_consumption().total_usage
                if self.cnt_log < 999:
                    break
                else:
                    cnt=cnt+1

            if cnt >= len(li.li_log_key):
                self.outoflist_log = True
        
        cnt = 0

    def broadtext(self, text):
        if self.cnt_log < 999:
            try:
                t = '%s[%d]>%s' %(self.ip, self.cnt_log+1, text)
                broadcast_response = self.channel_log.broadcast(TextSendMessage(text=t))
                self.cnt_log +=1
            except:
                pass
            else:
                return

        if not self.outoflist_log:
            self.__init__()
        return

if __name__ == "__main__":
    x = botNotification()
    print(x.channel_log.get_bot_info())
    #broadcast_response = x.channel_log.broadcast(TextSendMessage(text='Hello World!'))
    #broadcast_response = x.channel_order.broadcast(TextSendMessage(text='Hello World!'))


