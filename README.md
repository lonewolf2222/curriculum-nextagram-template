# Fork of Next Academy Flask Nextagram


## Production

**Full Stack Bootcamp final exercise on Python/Flask.**

**With some additional functions added**

- Pagination
- Facebook Login
- Reset Password
- Contact Form with Recaptcha v2

**Deployed and tested on Heroku and VPS running Debian 9**

**Steps to deploy on Debian 9 VPS**

1. SSH into VPS and run apt update && apt upgrade

2. apt install the following packages:
   - curl
   - postgresql and postgresql-contrib
   - gcc
   - redis-server
   - nginx
   - certbot and python-certbot-nginx
   - supervisor

3. Git clone app from repo to /home folder

4. Download and install Anaconda for Linux

5. Create and activate virtual env "nextagram"

6. Replace psycopg2-binary in requirements.txt with psycopg2-binary==2.8.5. 

7. $ pip install -r requirements.txt

8. $ su - postgres and run 

   $ psql -d template1 -c "ALTER USER postgres WITH PASSWORD 'newpassword';"

9. insert "postgres" newpassword in DATABASE_URL in .env and run

   $ source .env

10. while still su as user "postgres", run

      $ createdb /dev/nextagram_prod

      $ python migrate.py 

11. exit back to conda env

12. cd /etc/nginx/sites-enabled and delete the "default" file in the folder. create file "nextagram" with following content:

<pre><code>   
server {
      server_name webapp.leapnet.me;
      location / {
   proxy_pass http://127.0.0.1:8000;
   proxy_set_header Host $host;
   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header X-Forwarded-Proto $scheme;
    }
</code></pre>
13. run certbot to obtain let's encrypt ssl certs:

      $  certbot --nginx

      Allow certbot to redirect http to https

14. Restart nginx:

      $ systemctl restart nginx

15. fill in values for env vars in gunicorn_config.py

16. test run with command

    $ /home/anaconda3/envs/nextagram/bin/gunicorn --workers=3 -c /home/curriculum-nextagram-template/gunicorn_config.py start:app

17. cd /etc/supervisor/conf.d and create file nextagram.conf with following contents:
<pre><code>
      [program:start]
      command=/home/anaconda3/envs/nextagram/bin/gunicorn --workers=3 -c /home/curriculum
-nextagram-template/gunicorn_config.py start:app
      directory=/home/curriculum-nextagram-template
      autostart=true
      autorestart=true
      stopasgroup=true
      killasgroup=true
      stderr_logfile=/var/log/nextagram/nextagram.err.log
      stdout_logfile=/var/log/nextagram/nextagram.out.log
</code></pre>

18. Create the log files:

      $ mkdir /var/log/nextagram

      $ touch /var/log/nextagram/nextagram.err.log && touch /var/log/nextagram/nextagram.out.log


19. systemctl restart supervisor

---

This repository belongs to [NEXT Academy](https://www.nextacademy.com/?utm_source=github&utm_medium=student-challenge&utm_campaign=flask-nextagram) and is a part of NEXT Academy's coding bootcamps. You may find more information about our bootcamp at https://www.nextacademy.com

If you are already a student, you may find the challenge description at https://code.nextacademy.com/lessons/day-1--starting-template/479
