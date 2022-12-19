# Pull base image
FROM python:3.11-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y install curl
# Install Geometry libraries
RUN apt-get -y install binutils libproj-dev gdal-bin libgeos-dev
RUN apt-get -y install libgeos++ libgeos-c1v5 libgeos-3.9.0
#RUN apt-get -y install cmake wget tar bzip2 build-essential
#RUN wget https://download.osgeo.org/geos/geos-3.10.4.tar.bz2
#RUN tar xjf geos-3.10.4.tar.bz2
#RUN cd geos-3.10.4 && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && cmake --build . && cmake --build . --target install
# Set work directory
WORKDIR /code

# Install dependencies
COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
# Copy project
COPY . .