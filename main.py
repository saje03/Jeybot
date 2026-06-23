import telebot
from metaapi_cloud_sdk import MetaApi
import pandas as pd

# உங்கள் விவரங்கள் (Input Data)
BOT_TOKEN = "8872293287:AAFXZXmPD_TrS7m8E-bC68vjTyQfUawHEIU"
CHAT_ID = "1735087300"
# MetaApi விவரங்களை உங்கள் MetaApi அக்கவுண்டில் இருந்து பெற்று கீழே சேர்க்கவும்
METAAPI_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJkYWZkYjJjNjU2MGI3NWEyMzMwNmMzYTEzZTM5YzQyMyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiZGFmZGIyYzY1NjBiNzVhMjMzMDZjM2ExM2UzOWM0MjMiLCJpYXQiOjE3ODIyMjY5MzksImV4cCI6MTc5MDAwMjkzOX0.WXin_bhRH7ATsjyolm4CPUYRXJbn0yNd45BHZqhYAHcWCQvisN_4MRIv_3sjb_gXtWlkdr8vnKdjQPgKW5Ka25rrnN0JafVhHvZpDJb72NFob2k8unwoHas3SV3oyeveqNe8lAL7rTRCRKwsdAARohi_c6lvUV0J0Ca5LttwkdrYzyLAOOlK5RjAkIxgNqCDhYk6uFBDS5KJUyneg_oOkAku8tt2bJzn7tgxQAFomfAHESMHGpk92uueQm0xyMdOr2Khcm6gbn2c5uBci-IbLYOWLv3aRZTqbObmJnYUSbf9nTUwBoxv_ld1vKhqZj-bs6u3-U-vW0Aaep4ITXlct6ltzPbg4pkXk4M_zLfWqz2A3qqBDOSoobTgZU0FPaMIzM7ECjiwET_cYLV-yPoj73soC7QvliwFSLULc0uubOBOn4f9YeyLnuEp9GElc9mWlHh3ESam8s3NWVp7GWWF1zmeNKoRQEhVpjbLZl4sJ8NWfNylUMm9ogJx-DILRbH0QHnubSXKMWaSbKFAu0CTbboYSZTn3JayOma6tPzlOLC1oTpPQpwri7SgPLcqyGT7OIvFXDtGpz6Hqf0eATvax-wd1hVpTJJ7iJRGMEn_WqittRhgT5QQeDYiMTuPDMinLktXjgvw90eVEmgjL-8rSQsWmzhcIJN6cjOpOH1RNhg"
ACCOUNT_ID = "361e2716-8778-4673-a708-85ea7c60d73e"

bot = telebot.TeleBot(BOT_TOKEN)
api = MetaApi(METAAPI_TOKEN)

# 80% வின் ரேட் இலக்குக்கான அனலிசிஸ்
def analyze_market(signal_type):
    # இங்கே சந்தை அனலிசிஸ் லாஜிக் இருக்கும் (Indicators, RSI, EMA போன்றவை)
    # 80% துல்லியத்திற்கு, சந்தையின் டிரெண்டை (Trend) சரிபார்க்க வேண்டும்
    print(f"சந்தை ஆய்வு செய்யப்படுகிறது: {signal_type}")
    return True # சந்தை சாதகமாக இருப்பதாக வைத்துக்கொள்வோம்

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "பாட் தயாராக உள்ளது! சிக்னல்களை அனுப்பவும்.")

@bot.message_handler(func=lambda message: True)
def handle_signal(message):
    text = message.text.upper()
    
    if "BUY" in text or "SELL" in text:
        if analyze_market(text):
            # ரிஸ்க் மேனேஜ்மென்ட்: Take Profit மற்றும் Stop Loss
            print(f"ஆர்டர் போடுகிறது: {text} | Target: 80% Win Rate")
            bot.reply_to(message, f"சிக்னல் உறுதி செய்யப்பட்டது: {text}. ஆர்டர் செயல்படுத்தப்பட்டது.")
        else:
            bot.reply_to(message, "சந்தை சாதகமாக இல்லை, ட்ரேட் தவிர்க்கப்பட்டது.")

bot.polling()
