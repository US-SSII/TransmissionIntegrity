# base image
FROM python:3.9-slim

# setup environment variable
ENV DockerHOME=/home/app/webapp

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy config.ini
COPY ./src/main/python/config.ini $DockerHOME

# install dependencies
RUN pip install --upgrade pip

# Install necessary system libraries

# copy whole project to your docker home directory.
COPY . $DockerHOME

WORKDIR $DockerHOME

# run this command to install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# port where the Django app runs
EXPOSE 12345

# start server
CMD ["python", "run_server.py"]


# To build -> docker build -t my-django-app .
# To run -> docker run -p 12345:12345 my-django-app