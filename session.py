from instagrapi import Client

cl = Client()
cl.login("infini.io", "cherryaravind")  # It will ask for OTP here
cl.dump_settings("session.json")

