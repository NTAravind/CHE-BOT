from instagrapi import Client
import random
import time
import os

cl = Client()
cl.load_settings("session.json")
cl.login(os.getenv("IG_USER"), os.getenv("IG_PASS"))

sent_users = set()

def generate_discount_code():
    return "DISC" + str(random.randint(1000, 9999))

while True:
    inbox = cl.direct_threads(amount=10)
    for thread in inbox:
        if not thread.messages:
            continue

        user = thread.users[0]
        username = user.username
        message = thread.messages[0].text.lower()

        if username not in sent_users and message == "discount":
            if cl.user_following(user.pk):
                code = generate_discount_code()
                cl.direct_send(f"Here's your discount code: {code}", [user.pk])
                print(f"Sent code to @{username}")
                sent_users.add(username)
            else:
                print(f"@{username} asked for a code but doesn't follow you.")
    time.sleep(30)

