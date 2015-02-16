#Blackberry - A black box for my raspberry

##Installation

The following assumes that you are running Arch linux for the Raspberry Pi

1. Install Python script: `./setup.py install`
2. Create /etc directory: 

        mkdir /etc/blackberry
        cp etc/config.json.example /etc/blackberry/config.json
        
4. Create and enable systemd service:

        cp blackberry.service /usr/lib/systemd/system/
        systemctl enable blackberry.service

5. Create rules for /run directory and log file:
    Create a new file named /usr/lib/tmpfiles.d/blackberry.conf, containing the following line:

        D /run/blackberry 0700 blackberry blackberry -
        f /var/log/blackberry.log 0644 blackberry blackberry

6. Create logrotate config file, /etc/logrotate.d/blackberry.conf

        /var/log/blackberry.log {
          compress
          delaycompress
          copytruncate
          size 1M
          rotate 5
          monthly
          missingok
          create 0644 blackberry blackberry
        }
