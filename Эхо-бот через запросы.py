import requests
from pprint import pprint
import asyncio

updates = requests.get('https://api.telegram.org/bot5490426200:AAG4MUqJppCYScZNADDkcmesq52huUxYGXo/getUpdates').json()

text_last_message = updates['result'][-1]['message']['text']
chat_id = updates['result'][0]['message']['chat']['id']


requests.get(f'https://api.telegram.org/bot5490426200:AAG4MUqJppCYScZNADDkcmesq52huUxYGXo/sendMessage?chat_id={chat_id}&text={text_last_message}')

len_spis = len(updates['result'])

async def otv():
    global len_spis
    while True:
        updates = requests.get(
            'https://api.telegram.org/bot5490426200:AAG4MUqJppCYScZNADDkcmesq52huUxYGXo/getUpdates').json()
        text_last_message = updates['result'][-1]['message']['text']
        chat_id = updates['result'][-1]['message']['chat']['id']
        if len_spis != len(updates['result']):
            requests.get(
            f'https://api.telegram.org/bot5490426200:AAG4MUqJppCYScZNADDkcmesq52huUxYGXo/sendMessage?chat_id={chat_id}&text={text_last_message}')
