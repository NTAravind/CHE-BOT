from instagrapi import Client
import random
import time
import os

cl = Client()
cl.login(os.getenv("IG_USER"), os.getenv("IG_PASS"))

sent_users = set()

def generate_discount_code():
    return "DISC" + str(random.randint(1000, 9999))

while True:
    inbox = cl.direct_threads()
    for thread in inbox:
        user = thread.users[0]
        username = user.username
        message = thread.messages[0].text.lower()

        if username not in sent_users and message == "discount":
            if cl.user_following(user.pk):
                code = generate_discount_code()
                cl.direct_send(f"Here's your discount code: {code}", [user.pk])
                sent_users.add(username)
    time.sleep(30)

