import os
import requests
from datetime import datetime, time
import pytz

def send_telegram_message(bot_token, chat_id, message):
    """
    Skicka meddelande via Telegram Bot API
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # Tillåter HTML-formatering
    }
    
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
    Kontrollera om det är rätt tid att skicka meddelandet
    Måltid: 11:02 svensk tid.
    """
    stockholm_tz = pytz.timezone('Europe/Stockholm')
    now_stockholm = datetime.now(stockholm_tz)
    
    # Måltid i svensk tid
    target_hour = 11
    target_minute = 2
    
    print(f"🕐 Svensk tid nu: {now_stockholm.strftime('%H:%M:%S')}")
    
    # Kontrollera om vi är inom 40 minuter från måltiden
    current_time = now_stockholm.time()
    target_time = time(target_hour, target_minute)
    
    current_minutes = current_time.hour * 60 + current_time.minute
    target_minutes = target_time.hour * 60 + target_time.minute
    
    time_diff = abs(current_minutes - target_minutes)

    #debug = True #kan köra alla tider för test
    debug = False #normalbeteende
    
    if time_diff <= 40 or debug:
        print("✅ Inom tidsramen - kör!")
        return True
    else:
        print(f"❌ För långt från måltiden ({time_diff} min diff) - avslutar")
        return False

def main():
    print("🚀 Startar bot...")
    
    # 1. Kontrollera tid (så den inte skickar dubbelt om GitHub körs vid fel tillfälle)
    if not is_within_target_time():
        exit(0)
    
    # 2. Hämta secrets
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    daily_message = os.getenv('DAILY_MESSAGE') # Här hämtas ditt fasta meddelande
    
    # 3. Validera att allt finns
    if not bot_token:
        print("❌ BOT_TOKEN saknas i Secrets")
        exit(1)
        
    if not chat_id:
        print("❌ CHAT_ID saknas i Secrets")
        exit(1)

    if not daily_message:
        print("❌ DAILY_MESSAGE saknas i Secrets. Lägg till texten du vill skicka där.")
        exit(1)

    # 4. Skicka meddelandet
    success = send_telegram_message(bot_token, chat_id, daily_message)
    
    if success:
        print("🎉 Klart!")
    else:
        exit(1)

if __name__ == "__main__":
    main()
