IRC bot for a door.


Deployment
====

Create user doormon

    useradd doormon

Create working directory, put our project in it and grant ownership to our new user

    git clone https://github.com/NegativeK/doormon.git /srv/doormon
    chown -R doormon: /srv/doormon

You can take this opportunity to configure nick and channel settings in doormon.py, as well.

We can use pip to satisfy the requirements. In the repo directory:

    cd /srv/doormon
    apt-get install python3-venv
    sudo -u doormon python3 -m venv venv
    venv/bin/pip install irc
    gpasswd -a doormon audio
    # pip install -r requirements.txt

Copy our service file:

    cp /srv/doormon/doormon.service /etc/systemd/system

Enable and start the service:

    systemctl enable doormon.service
    systemctl start doormon.service


You should now be rocking and or rolling.
