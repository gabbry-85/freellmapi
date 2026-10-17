import os
import requests
import telebot

# Il tuo token di Telegram inserito direttamente
TOKEN = "8910040696:AAHiaNdOTwqITs5rvIoyL4B1OIRMC1taoQc"

# ATTENZIONE: Sostituisci 123456789 con il tuo vero ID numerico di Telegram (ottenuto da @userinfobot)
OWNER_ID = 8431418750

# Endpoint di FreeLLMAPI (locale o su Render)
FREELLM_URL = os.environ.get("FREELLM_URL", "http://localhost:8000/v1/chat/completions")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Controllo di sicurezza: rispondi solo al proprietario autorizzato
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ Accesso non autorizzato.")
        return

    user_text = message.text
    processing_msg = bot.reply_to(message, "⏳ Generazione in corso...")

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_text}]
    }

    try:
        response = requests.post(FREELLM_URL, json=payload, timeout=60)
        data = response.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            reply_text = data["choices"][0]["message"]["content"]
        else:
            reply_text = f"Risposta inattesa dal server: {data}"
            
    except Exception as e:
        reply_text = f"Errore di connessione con FreeLLMAPI: {e}"

    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg.message_id, text=reply_text)
    except Exception:
        bot.send_message(message.chat.id, reply_text)

if __name__ == "__main__":
    print("Bot Telegram avviato...")
    bot.infinity_polling()
