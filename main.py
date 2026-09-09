# Uppdaterad för att köra på Google Cloud Run
import os
import requests

def send_telegram_message(bot_token, chat_id, message, thread_id=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
    
    if thread_id:
        try:
            payload['message_thread_id'] = int(thread_id)
        except ValueError:
            pass
            
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json().get('ok', False)

def main():
    bot_token = os.getenv('BOT_TOKEN')
    raw_chat_id = os.getenv('CHAT_ID') 
    daily_message = os.getenv('DAILY_MESSAGE')

    if not all([bot_token, raw_chat_id, daily_message]):
        exit(1)

    if ':' in raw_chat_id:
        chat_id, thread_id = raw_chat_id.split(':')
        chat_id, thread_id = chat_id.strip(), thread_id.strip()
    else:
        chat_id, thread_id = raw_chat_id.strip(), None

    if not send_telegram_message(bot_token, chat_id, daily_message, thread_id):
        exit(1)

if __name__ == "__main__":
    main()
