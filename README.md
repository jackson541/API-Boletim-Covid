# API Boletins Covid Seridó

API em Djangorestframework para acompanhar o número de casos do Covid-19 na região do Seridó.

![Deploy](https://www.herokucdn.com/deploy/button.svg)

![](https://img.shields.io/badge/API--Boletim--Covid-v1.0-red?style=for-the-badge)


![](https://img.shields.io/static/v1?label=python&message=v3.5%20or%20Higher&color=blue&style=for-the-badge&logo=PYTHON)
![](https://img.shields.io/static/v1?label=django&message=v3.0.7&color=blue&style=for-the-badge&logo=DJANGO)
![](https://img.shields.io/static/v1?label=djangorest&message=v3.11.0&color=blue&style=for-the-badge&logo=DJANGO)


## How to Run:

Clone the project
```sh
git clone https://github.com/jackson541/API-Boletim-Covid.git
```

Go to Directory
```sh
cd API-Boletim-Covid
```

Install dependencies
```sh
pip3 install -r requirements.txt
```

Configure database
* Install [PostgreSQL](https://www.postgresql.org/)
* Go to the ```settings.py``` file in the ```ApiBoletimCovid``` folder
* Search for ```DATABASES``` in settings.py
* Configure your database information (name, password and port) in the option ```default```
* Create a table in your database with the name ```apicovid```

Apply Migrations
```sh
python3 manage.py makemigrations
python3 manage.py migrate
```

Run local server
```
python3 manage.py runserver
```


## Routes documentation
After running the project, go to the route:
```
http://localhost:8000/swagger/
```


## Contributors:

[<img  src="https://avatars3.githubusercontent.com/u/40877357?s=400&u=6be72f98bc5cc10dbb55fafc8f19c899658f8055&v=4" width="115"/>](https://github.com/jackson541)| [<img src="https://avatars2.githubusercontent.com/u/9680493?s=400&u=a7b309c2852e34ae9e1c88ff9133400c8a49ff11&v=4" width="115"/>](https://github.com/jonathantvrs)|
| ----- |----- |
| <p align="center">[Jackson Alves](https://github.com/jackson541) </p>| <p align="center">[Jonathan Tavares](https://github.com/jonathantvrs) </p> |
