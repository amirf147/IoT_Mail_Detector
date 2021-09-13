from errors import NotString
from constants import API_KEY
from telegram.ext import *
#import logging


# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)

class TelegramBot:

    def __init__(self, sensors):
        self.sensors = sensors
    
    updater = Updater(API_KEY, use_context = True)
    dispatcher = updater.dispatcher

    def responses(self, query):

        if not isinstance(query, str):
            raise NotString("query must be string")
        query = query.lower()
        
        if query in ('temp', 'temperature', 't'):
            reading = self.sensors['temperature']
            resp = f'{reading} degrees Celsius'
            return resp
        elif query in ('pressure', 'press', 'p'):
            reading = self.sensors['pressure']
            resp = f'{reading} millibar'
            return resp
        elif query in ('humidity', 'humid', 'h'):
            reading = self.sensors['humidity']
            resp = f'{reading}%'
            return resp
        elif query in ('brightness', 'bright', 'b'):
            return self.sensors['brightness']
        else:
            return 'unknown query'

    def start_command(self, update, context):
        update.message.reply_text("I hear you loud and clear!")

    def help_command(self, update, context):
        update.message.reply_text("commands = t, p, h, b")
    
    def handle_message(self, update, context):
        text = str(update.message.text).lower()
        response = self.responses(text)
    
        update.message.reply_text(response)
    
    def error(self, update, context):
        print(f'Update {update} caused error {context.error}')


