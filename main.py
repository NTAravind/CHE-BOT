from instagrapi import Client
import random
import time
import os
from datetime import datetime, timedelta

cl = Client()
cl.load_settings("session.json")
cl.login(os.getenv("IG_USER"), os.getenv("IG_PASS"))

sent_users = set()
sent_count = 0
HOURLY_LIMIT = 50
last_reset = datetime.now()

responses = [
    "Here's your discount code: {}",
    "Hey! Your code is: {} 🎉",
    "Discount code just for you: {}",
    "You got it! Code: {} ✅",
    "Thanks for messaging! Here's your code: {}"
]

follow_msg = "Hey! Please follow me to get your discount code 😊"

def generate_discount_code():
    return "DISC" + str(random.randint(1000, 9999))

while True:
    try:
        if datetime.now() - last_reset > timedelta(hours=1):
            sent_count = 0
            last_reset = datetime.now()

        inbox = cl.direct_threads(amount=10)

        for thread in inbox:
            if not thread.messages or not thread.users:
                continue

            user = thread.users[0]
            username = user.username

            message_obj = thread.messages[0]
            if not message_obj or not message_obj.text:
                continue

            message = message_obj.text.lower().strip()

            if username in sent_users or message != "discount":
                continue

            if cl.user_following(user.pk):
                if sent_count < HOURLY_LIMIT:
                    code = generate_discount_code()
                    reply = random.choice(responses).format(code)
                    cl.direct_send(reply, [user.pk])
                    print(f"✅ Sent code to @{username}")
                    sent_users.add(username)
                    sent_count += 1
                    time.sleep(random.randint(6, 12))
                else:
                    print("⏸️ Hourly DM limit reached.")
            else:
                cl.direct_send(follow_msg, [user.pk])
                print(f"⚠️ @{username} messaged but is not a follower.")
                time.sleep(random.randint(6, 12))

    except Exception as e:
        print(f"⚠️ Error: {e}")

    time.sleep(30)

