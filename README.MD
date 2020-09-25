# Set up your steamtrades.com-notifications

## Installing the conda environment

Install the necessary packages based on the environment file
`conda env create -f environment.yml`
The environment is called **st-noti**.

In addition, install the packages dotenv, yagmail and lxml.

## Set up variables
Set up a google app password following this guide: https://support.google.com/mail/answer/185833.

the following variables are required in a `.env` file:
- URLS_TO_CHECK: string, urls of all trading pages you want to check for updates, separated with `;` (Semikolon)
- RUN_FREQUENCY_IN_H: check for comments posted the {RUN_FREQUENCY_IN_H} hours
- GMAIL_USERNAME: email address of the sender
- GMAIL_PASSWORD: of the sender addres
- MY_USERNAME: your steamtrades username (comments from this username will not trigger notifications)
- RECEIVER_ADDRESS: arbitrary email address

### Running the script
Add the script `run.sh` to a cron-job to let it run regularly.
