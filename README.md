# NOT FINISHED DON'T USE AAAHHHHH

## Discord bot for my friends that translates things

### How to run:

<p>In order to run, please have python installed. Upon downloading, a few things are gonna be needed:</p>
<ul>
    <li>Python must be installed on your system</li>
    <li>You must fill in a .env variable with a bot token, and an optional test_bot token</li>
</ul>

### Uses:

It currently is unfinished, but will be able to be configured to auto_translate
into the current language, or be able to translate only into the default (currently 'en')

### How to install:

Download the code or git clone the repo into your local repository

` git clone https://github.com/Lumesque/disc_bot ; cd disc_bot`

Run the corresponding make command or pip install all required files into 
the top level directory

> Using make

`make install`

> Using pip

`pip3 install -r requirements.txt`

If you used make, a default env variable folder template will be created. If not,
create a .env variable with BOT_TOKEN

> Linux

`echo "BOT_TOKEN=XXXXXXXXXXX" >> .env`

> Windows powershell

`echo "BOT_TOKEN=XXXXXXXXXXX" | Out-File .env`



