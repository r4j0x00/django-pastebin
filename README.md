# Django Pastebin
*A simple pastebin.*

<img src="images/image2.png">
<img src="images/image1.png">

## Descrition
A simple, open source pastebin based on python3 and django.  
It has syntax highlighting features for various languages and is easy to setup.  
It also comes with a tool which can be used to directly upload pastes through command line.

## Cli tool
[![asciicast](https://asciinema.org/a/R1a62ZUNhZRwdeXggjHzLuvj8.png)](https://asciinema.org/a/R1a62ZUNhZRwdeXggjHzLuvj8)


## Prerequisites
```bash
pip3 install -r requirements.txt
```

## Database
This project can be used with both mysql and postgresql.
### Mysql setup
```sql
create database pastebin;
grant all privileges on pastebin.* to 'user'@'localhost' identified by 'password';
flush privileges;
use pastebin;
create table pastes ( url varchar(40), data text, lang varchar(40) );
exit;
```
settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pastebin',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}
```
### Postgresql setup
```sql
create database pastebin;
create user user with password 'password';
alter role user set client_encoding TO 'utf8';
alter role user set default_transaction_isolation to 'read committed';
alter role user set timezone TO 'UTC';
grant all privileges on database pastebin to user;
exit
```
settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pastebin',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}
```
