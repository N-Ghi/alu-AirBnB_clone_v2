#!/usr/bin/env bash
# script that sets up web servers for the deployment of hbnb_static
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/
sudo mkdir -p /data/hbnb_static/
sudo mkdir -p /data/hbnb_static/releases/
sudo mkdir -p /data/hbnb_static/shared/
sudo mkdir -p /data/hbnb_static/releases/test/
sudo touch /data/hbnb_static/releases/test/index.html
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/hbnb_static/releases/test/index.html

sudo ln -s -f /data/hbnb_static/releases/test/ /data/hbnb_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/hbnb_static/current/;}' /etc/nginx/sites-enabled/default

sudo service nginx restart