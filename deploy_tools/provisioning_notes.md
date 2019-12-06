Provisioning a new site
=======================

## Required packages:
* nginx
* Python 3.7
* virtualenv + poetry
* Git

eg, On Ubuntu:
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install nginx git python37 python2.7-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure
Assume we have a user account at /home/username
```bash
/home/username
├── sites
    ├── SITENAME
        ├── database
        ├── source
        ├── static
        ├── virtualenv
```