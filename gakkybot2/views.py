# from django.shortcuts import render

# Create your views here.
import json
import os
import requests

import doco.client

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from .models import Greeting
from .models import Dialogue

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
docomo_api_key = settings.DOCOMO_API_KEY
docomo_client = doco.client.Client(apikey=docomo_api_key)

@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                # get text from line
                user_utt = event.message.text
                user_dialogue = Dialogue(user_name='user', text=user_utt)
                user_dialogue.save()

                
                # send to docomo api
                docomo_res = docomo_client.send(
                    utt=user_utt, apiname='Dialogue')
                bot_utt = docomo_res['utt']

                line_bot_api.reply_message(
                    event.reply_token,
                   TextSendMessage(text=bot_utt)
                )
                bot_dialogue = Dialogue(user_name='bot', text=bot_utt)
                bot_dialogue.save()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def db(request):
    dialogues = Dialogue.objects.all()
    return render(request, 'db.html', {'dialogues': dialogues})

