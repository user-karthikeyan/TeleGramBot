import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.error import *
from bs4 import BeautifulSoup




def getMessage(name):
    Request = requests.get("https://telegram.me/s/aripdf")
    soup = BeautifulSoup(Request.content, 'html.parser')
    elements = soup.find_all("a", {"class":"tgme_widget_message_document_wrap"})
    for element in elements:
        if element.find("div", {"class":"tgme_widget_message_document_title accent_color"}).text == name:
            return element["href"].split("/")[-1]

def getFiles():
    Request = requests.get("https://telegram.me/s/aripdf")
    soup = BeautifulSoup(Request.content, 'html.parser')
    elements = soup.find_all("div", {"class":"tgme_widget_message_document_title accent_color"})
    Message = "======Available Documents======\n" + "\n".join([str(i + 1) + ". " + element.text for i, element in enumerate(elements)]) + "\n To get pdf - /pdf filename"
    return Message
    


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Wassup buddy? Need notes to study? I'm here 😉")


async def pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_message.text.replace("/pdf ", "")
    message_id = getMessage(name)
    try:
        await context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=-1001717260438, message_id=message_id)
    except BadRequest:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid filename\nTo know exact filename /help")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = getFiles()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)




    

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("Key")).build()
    
    #Building bot on the given ID

    
    start_handler = CommandHandler('start', start)
    pdf_handler = CommandHandler('pdf', pdf)
    help_handler= CommandHandler('help', help)
    
    #Adding commands
    application.add_handler(start_handler)
    application.add_handler(pdf_handler)
    application.add_handler(help_handler)
    
    application.run_polling()
