## How to make a deploy?
```sh
$ sudo nano /etc/systemd/system/museum_database.socket
```
insert there
```
[Unit]
Description=gunicorn socket
[Socket]
ListenStream=/run/museum_database.sock
[Install]
WantedBy=sockets.target
```

Next
```sh 
$ sudo nano /etc/systemd/system/museum_database.service
```

```
[Unit]
Description=gunicorn daemon
Requires=museum_database.socket
After=network.target
[Service]
User=yourusername
Group=www-data
WorkingDirectory=/home/username/museum_database
ExecStart=/home/username/museum_database/venv/bin/gunicorn --workers 3 --bind unix:/run/museum_database.sock museum_database.wsgi:application
[Install]
WantedBy=multi-user.target
```

Now create nginx files
```sh
$ sudo nano /etc/nginx/sites-available/museum_database
```
and put there
```
server {
    listen 80;
    server_name  yourdomainorip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/yourusername/museum_database;
    }
    location /media/ {
        root /home/yourusername/museum_database;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/museum_database.sock;
    }

}
```
Then run
```sh 
$ sudo nginx -t
$ sudo systemctl restart nginx
$ sudo systemctl daemon-reload
```
Now lets start and enable our services
```sh
$ sudo systemctl start museum_database.service
$ sudo systemctl start museum_database.socket
$ sudo systemctl enable museum_database.service
$ sudo systemctl enable museum_database.socket
```
And it SHOULD work (web deploy can be a *....insert proper word yourself*)

After every update run
```sh
$ sudo systemctl restart museum_database.socket museum_database.service
```