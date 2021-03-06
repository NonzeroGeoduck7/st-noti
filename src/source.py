from lxml import html, etree
from dateutil import parser
from datetime import datetime
from settings import *
import requests
import yagmail
import pickle
import pytz
import sys
import os

verbose = True
if verbose:
    print("Staring job, verbose = TRUE")
else:
    print("Starting job, verbose = FALSE")

LAST_CHECK = datetime.fromtimestamp(0)
now = datetime.now()

# load time stamp
last_check_file = "last_check.p"
if os.path.exists(last_check_file):
    with open(last_check_file, "rb") as f:
        LAST_CHECK = pickle.load(f)


headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

def steamTradesComments(link):
    url = link + '/search?page=last'

    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.content)

    comments = tree.xpath('//div[not(@class="comment_children")]//div[@class="comment_outer"]/div[@class="comment_inner"and not(@data-username="{}")]/div[@class="comment_body"]'.format(my_username))

    if verbose: print("found {} comments.".format(len(comments)))

    new_comments = []
    for c in comments:
        try:
            date = c.xpath('.//span')
            text = c.xpath('.//div[@class="comment_body_default markdown"]')

            # if comment is edited, there are 2 span elements in date
            dt = datetime.fromtimestamp(int(date[-1].attrib['data-timestamp']))

            if verbose: print("{} seconds ago: {} ({} texts found)".format((datetime.now() - dt).total_seconds(), text[0].text_content(), len(text)))

            if (dt - LAST_CHECK).total_seconds() > 0:
                # new comment found
                new_comments.append((dt,text[0].text_content()))

        except (TypeError, IndexError):
            pass
        except:
            print("Unexpected error:", sys.exc_info())

    return url, new_comments

def barterComments(link):
    url = link + 'o/'

    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.content)

    comments = tree.xpath('//ul[@class="activity"]//li')

    if verbose: print("found {} comments.".format(len(comments)))

    new_comments = []
    for c in comments:
        try:

            if not(
                c[2].attrib['href'] != link and           # its not me that initiated
                (' proposed ' in c.xpath('./text()') or   # its an offer proposal
                ' accepted ' in c.xpath('./text()'))      # your offer has been accepted
                ):
                continue

            time = c.xpath('.//time')
            offer = c.xpath('.//a[text() = "offer"]')

            # if comment is edited, there are 2 span elements in date
            dt = parser.parse(time[0].attrib['datetime'])

            last_check_formatted = LAST_CHECK.replace(tzinfo=pytz.utc)
            if verbose: print("{} seconds ago: {} ({} texts found)".format((datetime.utcnow().replace(tzinfo=pytz.utc) - dt).total_seconds(), offer[0].attrib['href'], len(offer)))

            if (dt - last_check_formatted).total_seconds() > 0:
                # new comment found
                new_comments.append((dt,c.xpath('./text()')[2]+":"+offer[0].attrib['href']))

        except (TypeError, IndexError) as e:
            print("TypeError ", e)
            pass
        except:
            print("Unexpected error:", sys.exc_info())

    return url,new_comments


results = []

for link in links_to_check:

    new_comments = []
    if 'barter.vg' in link:
        url,new_comments = barterComments(link)
    elif 'steamtrades.com' in link:
        url,new_comments = steamTradesComments(link)
        
    if len(new_comments) > 0:
        results.append((url, new_comments))

# send mail
if len(results) > 0:
    
    subject = 'New comments for steam trades'

    content_string = 'Found these new comments:'

    for (link,comments) in results:
        content_string = content_string + '\n' + link + '\n\n'

        for (date,text) in comments:
            content_string = content_string + str(date) + ": " + text + "\n"

    content = [content_string]

    if verbose: print("mail body: ", content_string)

    with yagmail.SMTP(gmail_name, gmail_pw) as yag:
        yag.send(receiver_email, subject, content)
        print('Sent email successfully')

else:
    print('Job finished, no email sent')

with open(last_check_file, "wb") as f:
    pickle.dump(now, f)
