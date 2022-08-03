# api_YaMDb
## API for YaMDb
API_YaMDb is the programming interface to access Yatube Database
## Tech
Python 3.8.10
Django 2.2.16
## Installation
- use this shell command to clone repository to your local computer:
```
git clone git@github.com:hopsent/api_final_yatube.git
```
- move to project directory:
```
cd api_final_yatube
```
- install virtual environment and turn it on:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
python3 -m pip install --upgrade pip
```
- set requirements from requirements.txt:
```
pip install -r requirements.txt
```
- also install rest_framework_simplejwt:
```
pip install djangorestframework-simplejwt
``` 
- in the manage.py directory to complete migrations use:
```
python3 manage.py migrate
```
- in the manage.py directory to start project use:
```
python3 manage.py runserver
```
## Authors
Aleksei Kulakov
Anastasia Borovik
Dmitri Martuza
