import os
import requests
from datetime import datetime, time
import pytz

def send_telegram_message(bot_token, chat_id, message, thread_id=None):
    """
    Skicka meddelande via Telegram Bot API.
    Nu tvingar vi thread_id att vara en siffra (int).
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    # VIKTIGT: Vi måste göra om thread_id till en int (siffra)
    if thread_id:
        try:
            payload['message_thread_id'] = int(thread_id)
        except ValueError:
            print(f"⚠️ Varning: Topic ID '{thread_id}' är inte en siffra. Ignorerar.")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        if response.json().get('ok'):
            print(f"✅ Meddelande skickat!")
            return True
        else:
            print(f"❌ Telegram API fel: {response.json()}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Nätverksfel: {e}")
        return False

def is_within_target_time():
    """
    Kontrollera om det är rätt tid att skicka (ca 11:02 svensk tid).
    """
    stockholm_tz = pytz.timezone('Europe/Stockholm')
    now_stockholm = datetime.now(stockholm_tz)
    
    target_hour = 11
    target_minute = 2
    
    print(f"🕐 Svensk tid nu: {now_stockholm.strftime('%H:%M:%S')}")
    
    current_time = now_stockholm.time()
    target_time = time(target_hour, target_minute)
    
    current_minutes = current_time.hour * 60 + current_time.minute
    target_minutes = target_time.hour * 60 + target_time.minute
    
    time_diff = abs(current_minutes - target_minutes)
    
    # --- MANUELL DEBUG ---
    debug = True  # <--- Sätt till False när du är klar!
    
    if time_diff <= 40 or debug:
        if debug:
            print(f"⚠️ Debug är PÅ (Tidsskillnad: {time_diff} min) - kör ändå!")
        else:
            print("✅ Inom tidsramen - kör!")
        return True
    else:
        print(f"❌ För långt från måltiden ({time_diff} min diff) - avslutar")
        return False

def main():
    print("🚀 Startar bot...")
    
    if not is_within_target_time():
        exit(0)
    
    bot_token = os.getenv('BOT_TOKEN')
    raw_chat_id = os.getenv('CHAT_ID') 
    daily_message = os.getenv('DAILY_MESSAGE')

    if not bot_token or not raw_chat_id or not daily_message:
        print("❌ Något saknas i Secrets (Token, Chat ID eller Message).")
        exit(1)

    # Hantera om det är en Topic (kolon) eller vanlig grupp
    if ':' in raw_chat_id:
        chat_id, thread_id = raw_chat_id.split(':')
        chat_id = chat_id.strip()
        thread_id = thread_id.strip()
        print(f"🎯 Mål: Topic {thread_id} i grupp {chat_id}")
    else:
        chat_id = raw_chat_id.strip()
        thread_id = None
        print(f"🎯 Mål: Grupp {chat_id} (General)")

    success = send_telegram_message(bot_token, chat_id, daily_message, thread_id)
    
    if success:
        print("🎉 Klart!")
    else:
        exit(1)

if __name__ == "__main__":
    main()
