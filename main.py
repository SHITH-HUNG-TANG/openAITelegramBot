import logging
import configparser
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
#內連模式
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from openAI import openAIChat, keyToImage
from PIL import Image
import requests

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

text = ""
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global text
    
    text += (f"Human:{update.message.text}\nAI:")
    anser = openAIChat(text)
    text += (f"{anser}\n")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=anser)
    if update.message.text == "拜拜":
        text = ""

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def getImage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args[0]:
        url = keyToImage(context.args[0])
        # im = Image.open(requests.get(url, stream=True).raw)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
        # await context.bot.send_message(chat_id=update.effective_chat.id, text=context.args[0])

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(1111111111111111111111)
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

if __name__ == '__main__':
    application = ApplicationBuilder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    image_handler = CommandHandler('img', getImage)    
    inline_caps_handler = InlineQueryHandler(inline_caps)


    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(image_handler)
    application.add_handler(inline_caps_handler)
    
    application.run_polling()





