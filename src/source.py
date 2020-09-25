from lxml import html, etree
from datetime import datetime
from settings import *
import requests
import yagmail
import sys

verbose = True
if verbose:
    print("Staring job, verbose = TRUE")
else:
    print("Starting job, verbose = FALSE")

DATE_NOW = datetime.now()

headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

results = []

for link in links_to_check:

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

            if verbose: print("{} seconds ago: {} ({} texts found)".format((DATE_NOW - dt).total_seconds(), text[0].text_content(), len(text)))

            if (DATE_NOW - dt).total_seconds() < run_frequency_in_h*3600:
                # new comment found
                new_comments.append((dt,text[0].text_content()))

        except (TypeError, IndexError):
            pass
        except:
            print("Unexpected error:", sys.exc_info())

    if len(new_comments) > 0:
        results.append((url, new_comments))

# send mail
if len(results) > 0:
    
    subject = 'New comments on steamtrades.com'

    content_string = 'Found these new comments (checked last ' + str(run_frequency_in_h) + ' hours):\n'

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
