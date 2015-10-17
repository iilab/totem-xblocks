#! /bin/bash    
source venv/bin/activate
pip install -e totem-xblocks/
python xblock-sdk/manage.py runserver 213.108.108.223:18000
