# DEMO PROJECT

## **PROJECT SETUP**

1. **Clone this repository:**
    * git clone https://github.com/siddharth-999/demo.git
2. **Create virtual environment:**
    * sudo apt install virtualenv
    * virtualenv --python='/usr/bin/python3.6' demo-env
    * source demo-env/bin/activate
    * cd demo/
3. **Install dependencies**:
    * pip install -r requirements.txt
4. **create postgres** install postgres database **/** create db if already install
    * **install postgresql**
        * wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
        * sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" >
          /etc/apt/sources.list.d/PostgreSQL.list'
        * sudo apt update
        * sudo apt-get install postgresql-10
    * **create database**
        * sudo su - postgres
            * postgres@xxx:~$ psql
            * create database <bd_name>;
            * create user <admin_name> password <password>;
            * grant all privileges on database <bd_name> to <admin_name>;
            * postgres=# \q
            * postgres@xxx:~$ exit
5. **create local.py** in demo/demo/
    * local.py content:
        ```
        DEBUG = True
        # DATABASE CONNECTION
        DATABASES = {
            'default':
                {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': '<bd_name>',
                    'USER': '<admin_name>',
                    'PASSWORD': '<password>',
                    'HOST': 'localhost',
                    'PORT': '<db_port>'
                }
        }
        ```
6. **Run migrations:**
    * ./manage.py migrate
7. **Create superuser:**
    * ./manage.py createsuperuser
8. **Run the server:**
    * ./manage.py runserver
9. **Browse below url:**
    * Swagger url:- `http://localhost:8000/api/docs`
    * Admin url: - `http://localhost:8000/admin/`