import os
from dotenv import load_dotenv

load_dotenv()

# load env variables
links_to_check = os.getenv("URLS_TO_CHECK").split(';')
receiver_email = os.getenv("RECEIVER_ADDRESS")

gmail_name = os.getenv("GMAIL_USERNAME")
gmail_pw = os.getenv("GMAIL_PASSWORD")

my_username = os.getenv("MY_USERNAME")
