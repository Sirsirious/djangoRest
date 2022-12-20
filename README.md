# Django Rest
Welcome to this simple Django REST Project.

This project showcases the use of a Django REST Framework to create a simple API to manage
and locate designated area service providers.

We use a GIST index with PostGIS to locate the service providers that match a provided point.
While this might not be the most efficient (space-wise) way to do this, it is the most straitghtforward
to implement - using any other indexing method won't work and will produce
full table scans due to the geographic nature of the problem.

This causes the need to do some extra installs, so the containers
are not baremetal. Check the Important! section below to see what you need to install.

<!-- TOC -->
* [Django Rest](#django-rest)
  * [Installation](#installation)
    * [Important - OS dependencies!](#important---os-dependencies-)
      * [MAC](#mac)
      * [Linux/Debian](#linuxdebian)
      * [Windows](#windows)
  * [API](#api)
    * [Swagger](#swagger)
  * [Tests](#tests)
<!-- TOC -->

## Installation
1. Clone the repository
2. Run docker-compose up -d --build
3. This will bring the API on port 80. Feel free to modify accordingly.

### Important - OS dependencies!

To run baremetal, you need to make sure that the libraries are installed on your system.

You'll need to:
1. Install PostGIS
2. Install GDAL
3. Install GEOS

#### MAC

In mac, you can do this with homebrew:
```
brew install postgis
brew install gdal
brew install geos
```

#### Linux/Debian
For debian, you'll need to install the following packages (apt-get):
```
apt-get -y install binutils libproj-dev gdal-bin libgeos-dev
apt-get -y install libgeos++ libgeos-c1v5 libgeos-3.9.0
```

#### Windows

Good luck 😭

---

Installing the libraries will make gdal and geos libraries available to the system.

The baremetal ENV was setup for a mac device, so if you're using a different OS, you might need to
change the ENV variables that are read in settings.py.

## API

The available endpoints are:

* GET/POST /providers
* GET/POST/PUT/PATCH/DELETE /providers/{id}
* GET/POST /service-area/
* GET/POST/PUT/PATCH/DELETE /service-area/{id}
* POST /service-area-match/


### Swagger

This project was setup with Swagger, so you can access the API documentation at http://IP.ADDRESS/swagger

## Tests

The tests were written using pytest-django. We have a few tests that test the API and the models.

To run the tests, you'll need to run the following command:
```
docker-compose run --rm web pytest
```

### Side notes

Some lines were changed on the docker-compose file in the deployment to make it work with EC2.


