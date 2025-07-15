import telepot

token = '7859667749:AAF9E_GRkGLXa-QrXgmXDoZNFNndm9efjec'
my_id = 6450921615
telegramBot = telepot.Bot(token)


def send_message(text):
    telegramBot.sendMessage(6450921615, text, parse_mode="Markdown")