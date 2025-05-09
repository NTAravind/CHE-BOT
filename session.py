from instagrapi import Client
import os
cl = Client()
cl.login("pytestinfini","cherryaravind")
cl.dump_settings("session.json")

