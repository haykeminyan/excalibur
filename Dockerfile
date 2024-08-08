# pull official base image
FROM python:3.12

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# install dependencies
RUN pip install --upgrade pip

# Copy requirements.txt from cerberus-api directory
COPY requirements.txt .

# install dependencies from requirements.txt
RUN pip install -r requirements.txt

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Copy the rest of the application
COPY . .

# specify the command to run on container start
CMD ["./entrypoint.sh"]
