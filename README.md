![CryptAPI](https://i.imgur.com/IfMAa7E.png)

# CryptAPI's WhiteLabel setup
CryptAPI's WhiteLabel setup in Django

## Requirements:

```
Docker
Docker-compose
Git
```

## Install


```shell script
git clone https://github.com/cryptapi/cryptapi-whitelabel
```

&nbsp;

##### Install Docker & Docker Compose (skip this if already installed)

```shell script
./get_started.sh
```

## Configuration

Edit the following files:

##### docker-compose.yml

Set `POSTGRES_PASSWORD` to the DB password you wish to set

&nbsp;

##### conf/web/httpd.conf

Set `ServerName`, `ServerAlias` and `ServerAdmin` inside the `<VirtualHost>` tag

> If you wish to set HTTPS, uncomment the 443 `<VirtualHost>` tag and set the same items as above.

&nbsp;

##### volumes/web/CAWhiteLabel/settings.py

Set `SECRET_KEY` to a randomly-generated string ( ! Important ! )

Set `DEBUG` to False

Add your domain (eg. example.com) to `ALLOWED_HOSTS` 

Set Database password to the password you set on `docker-compose.yml`

## First Start

Run the following commands:

```shell script
docker-compose up -d
docker-compose exec web bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata default_settings.json
python3 manage.py collectstatic
```

> Reply yes

```shell script
python3 manage.py createsuperuser
```

> Input your admin username

> Input your email (optional)

> Input and confirm your admin password

## Settings

1. Open the admin panel, which is by default on `/admin`
2. Go to Settings and open the first one ("White Label")
3. Set the settings for your service. 

> Do not change default CryptAPI settings unless CryptAPI has updated fee settings.


## Customize the layout

If you want to customize the layout, change the files in the following directories:

CSS files:
* volumes/web/static/css/

JS files:
* volumes/web/static/js/

HTML template files:
* volumes/web/index/templates/

## Help

Need help?  
Contact us @ https://cryptapi.io/contact/