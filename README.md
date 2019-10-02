# Georef

Georef is a georeferencing data tool originally created for the Museu de Ciencies Naturals de Barcelona - [MCNB](https://museuciencies.cat/). It allows the storage, indexing and querying of georeferencing data, including geometry, and supports multiple versions of the data. Georef is built using [Django](https://www.djangoproject.com/)

The application exposes an API which allows mainly querying the underlying data. The API is a separate project and can be found here: https://github.com/aescobarr/djangoref_api

## Getting Started

These instructions will help you set up a basic working development environment on a Ubuntu 18.04 LTS system. It assumes Git is installed and running in the host machine.

### Prerequisites

- Create a user which will own the project folder. Traditionally, the user is named djangoref but you can name it anything you want.

- Log on the machine as the djangoref user and clone this repo

```
git clone https://github.com/aescobarr/djangoref.git
```

#### General packages

First some basic general purpose packages:

```
sudo apt install libpq-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev
sudo apt install gcc
sudo apt install g++
```

#### Database

Georef uses a Postgresql + Postgis database. You can install it like this:

```
sudo apt install postgresql-10
sudo apt install postgresql-10-postgis-2.4
sudo apt install postgresql-10-postgis-scripts
```

We recommend to create a separate Postgresql user which will own the Georef database and not use the postgres super user. To create the user and the application database we would follow these steps (we will create a user called georef_app):

Log to Postgresql console using the postgres (admin) user. Then:
```
-- Create the georef_app user
CREATE ROLE georef_app LOGIN PASSWORD 'mypassword' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
```

With the user created, we now proceed to create the database which will host the application data. As the postgresql system user, from the shell we can create the database and make it belong to the application user which we named georef_app in the last step (in this example we call the database georef):

```
# As postgresql user
createdb georef -O georef_app
```

Finally, we enable the postgis extensions in the database. We connect as the postgres user to the georef database and we execute the commands:
```
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
```

Remember the name of the database, owner user and its password because we will have to put them in the database configuration file (adjusting config files section)

#### Python stuff

Python 3.6 should be installed in Ubuntu 18.04 by default. We also need pip for installing python packages:

```
sudo apt install python-pip
sudo apt install python3.6-dev
```

Georef relies heavily on GDAL/OGR libraries for certain spatial calculations. These are installed like this:

```
sudo add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt install gdal-bin python-gdal python3-gdal
sudo apt-get install libgdal-dev
```

It is strongly recommended to install Virtualenvwrapper to manage the app virtual environment:

```
pip install virtualenv
pip install virtualenvwrapper

# then, as the djangoref user or whatever you named it in prerequisites open ~/.bashrc with a text editor and add the line
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

#finally activate the virtualenvwrapper script
source ~/.bashrc
```

For additional info on virtualenvwrapper, go to the virtualenvwrapper [docs](https://virtualenvwrapper.readthedocs.io/en/latest/)


### Installing


#### Virtual environment
We will need a python virtual environment to run the app. Execute these commands as the user that owns the project folder. We assume that the environment name is 'georef' but you can name it however you want:
```
#Create a virtual env named 'georef'
mkvirtualenv --python=/usr/bin/python3.6 georef
```

The --python parameter ensures that the python interpreter used will be 3.6. Once the environment is active, its name in parentheses will appear before the command line in shell. To activate, simply type
```
#Activate the virtual env
workon georef
```
With the virtual environment active, let's load all the needed python packages into it. From the application folder, launch this command:
```
pip install -r requirements.txt
```
This will install all the packages listed in requirements.txt in the virtual environment. If all goes well, we proceed with the next step.

#### Adjusting config files

The cloned repository has a settings.py typical django config file. However, this file is not enough to run the app, as it points to a second settings_local.py file which must be created. This file is not Most parameters in settings.py are overwritten by this file. So it must be created and exist at the same level in the folder structure as settings.py.

The file settings_local.py contains the following (the comments give a brief description of each config key value):
```
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' # Long, complicated string that django uses internally for things like identifying sessions

DEBUG = False # In development, this can be set to True to visualize additional debug info. In production, always set to False

ALLOWED_HOSTS = []  # If DEBUG = False, put here a comma separated list of the host name/s. For a single name -> ['www.example.com']/ for multiple names, ['www.example1.com','www.example2.com']. If DEBUG = True, leave as it is.

# Postgresql connection parameters
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', #We use the Postgis extension for spatial queries
        'NAME': 'DATABASE_NAME', # Put here your database name
        'USER': 'USER_NAME', # Put here the user that connects with the database. This user must be able to read/write the database
        'PASSWORD': 'PASSWORD', # The above user password
        'HOST': 'localhost', # The IP address of the machine hosting the database
        'PORT': '5432', # The port in which Postgresql listens for connections
    }
}

#STATIC_ROOT = '/home/djangoref/djangoref/static/'
#Absolute path to static resources folder. In development, comment out this line

MEDIA_URL = "/media/" # Media URL, relative to the app root address. For example if our app is running in www.example.com, media files should be accessible at www.example.com/media/
UPLOAD_DIR = BASE_DIR + "/uploads" # Absolute Upload directory path, appended to BASE_DIR which points to the application root folder
MEDIA_ROOT = UPLOAD_DIR # The media path is the same as UPLOAD_DIR
LOCAL_DATAFILE_ROOT_DIRECTORY = 'helpfile_uploads'

# Geoserver params
GEOSERVER_WORKSPACE = 'SOME_WORKSPACE' # Workspace in which the layers will be stored
GEOSERVER_USER = 'GEOSERVER_USER' # Geoserver user
GEOSERVER_PASSWORD = 'GEOSERVER_USER_PASSWORD' # The password of the above user
GEOSERVER_BASE_URL = 'https://www.example.com/' # Root url of the geoserver install address. The trailing slash is important
GEOSERVER_WMS_URL_CLEAN = GEOSERVER_BASE_URL + 'geoserver/wms/' # Root url of the geoserver WMS services endpoint
GEOSERVER_REST_URL = GEOSERVER_BASE_URL + 'geoserver/rest/' # Root url of the geoserver restful api endpoint
GEOSERVER_WMS_URL = GEOSERVER_BASE_URL + 'geoserver/' + GEOSERVER_WORKSPACE + "/wms/?" # URL to wms services of the previously defined GEOSERVER_WORKSPACE
```

#### Starting the app in dev mode

Before starting up the app, we need to perform a couple of additional setup steps to prepare the database. First, we create the base tables for the app. To do this, we execute a script in the "scripts" subfolder in the app folder:

```
# We connect as the app user and create some tables in the app database
# A brief breakdown of the parameters:
# -h is the address of the machine that hosts the database. We assume here that is running in localhost
# -d is the name of the database which we created in the Database section
# -U is the user name of the owner of the database
# -f is the path to the djangoref_db_tables.sql script
psql -h localhost -d georef -U georef_app -W -f [path_to_app_folder]/scripts/djangoref_db_tables.sql
```

This should create a few tables, which we need for the next step. From the command shell, we activate the virtual environment (this is important) and we run the migrations which will create the basic django management tables and a few model tables.

```
# We assume that we have named the virtual env georef. To activate, we do:
workon georef
# From the application folder, we run the command
./manage.py migrate
```

At this point, we need to run a second sql script which contains some foreign key definitions. This is very similar to the first step in this section:
```
# We connect as the app user and create some foreign keys in the app database
# A brief breakdown of the parameters:
# -h is the address of the machine that hosts the database. We assume here that is running in localhost
# -d is the name of the database which we created in the Database section
# -U is the user name of the owner of the database
# -f is the path to the djangoref_db_constraints.sql script
psql -h localhost -d georef -U georef_app -W -f [path_to_app_folder]/scripts/djangoref_db_constraints.sql
```

This leaves us with a fully prepared empty database. Now we can create a superuser:
```
./manage.py createsuperuser
```

With the virtual environment active, from inside the app folder we run the script

```
./manage.py runserver
```

This should start a development server at http://127.0.0.1:8000

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

