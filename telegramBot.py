import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler,ContextTypes, filters as Filters, CallbackContext,Application

# Telegram bot token
TOKEN = {'YourToken'}
CHANNEL_IDS = ['your channel ids']  

# Fonksiyon: Verilen linkten ürün adını ve görselini alır
def get_product_info(link):
    # Linkten HTML içeriğini al
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    html = requests.get(link, headers=headers).content
    soup = BeautifulSoup(html, "html.parser")

    # Ürün adını bul
    product_name_element = soup.find('h1')
    if product_name_element:
        product_name = product_name_element.text.strip()
    else:
        product_name = "Ürün adı bulunamadı."

    # Ürün resmini bul
    img_element = soup.find_all('img')
    if img_element:
        product_image = img_element[2]['src']
    else:
        product_image = None

    # Ürün fiyatını bul
    product_price_element=soup.find("span", {"class": "prc-dsc"})

    if product_price_element:
        product_price = product_price_element.text
    else:
        product_price = None

    return product_name, product_image,product_price



# Komut: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        "Merhabalar Test")
# Link alındığında çalışacak fonksiyon
async def handle_link(update: Update, context: CallbackContext) -> None:
    # Linki al
    link = update.message.text
    
    # Linkten ürün adını ve görselini al
    product_name, product_image ,product_price= get_product_info(link)
    
    # Mesajı hazırla ve gönder
    message_text = f"DUYURU!\n\n{product_name}\n\n Fiyat : {product_price}"
    message_markup = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("TIKLA GİT", url=link)
    )
    await update.message.reply_photo(
        photo=product_image, caption=message_text+"\n\n\n!BÜTÜN KANALLARDA DUYURU YAPILMIŞTIR", reply_markup=message_markup, parse_mode='HTML'
    )
    
    # Kanallara mesajı gönder
    for channel_id in CHANNEL_IDS:
        await context.bot.send_photo(chat_id=channel_id, photo=product_image, caption=message_text, reply_markup=message_markup, parse_mode='HTML')

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(Filters.TEXT& ~Filters.COMMAND, handle_link))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
