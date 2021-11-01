import re

from urllib.error import HTTPError
from urllib.request import urlopen, Request

base_url = "https://discordapp.com/api/invite/"
startswith_url = "https://discord"

def check_invite(invite_code):
    url = f"{base_url}{invite_code}"
    httprequest = Request(url, headers={'User-agent': 'Mozilla/5.0'})
    try:
        with urlopen(httprequest) as response:
            print(response.status)
            print(response.read().decode())
    except HTTPError as e:
        if e.code == 10006:
            print(f"Invalid invite code {invite_code}")
        elif e.code == 429:
            print(f"Too many requests")
        else:
            print(f"Error fetching {invite_code} (code: {e.code} reason:{e.reason}")

def extract_urls(text):
    markup_regex = '\(\s*(http[s]?://[^)]+)\s*\)'
    for match in re.findall(markup_regex, text):
        if match.startswith(startswith_url):
            invite_code = match.split("/")[-1]
            check_invite(invite_code)

with open('README.md') as f:
    extract_urls(f.read())
