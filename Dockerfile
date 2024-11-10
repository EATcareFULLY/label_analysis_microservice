FROM python:3.9-slim


# install redis server
RUN apt-get update && apt-get install -y redis-server redis-tools 
RUN apt-get install -y bash

WORKDIR /code

# copy files for initial configuration
COPY ./requirements.txt /code/requirements.txt
COPY ./redis_init.sh /code/redis_init.sh

# copy app files
COPY ./app /code/app


# populate redis with data
RUN chmod +x /code/redis_init.sh

# install required python libraries
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# expose port
EXPOSE 80

# run app on uvicorn server
CMD ["bash", "-c", "redis-server --daemonize yes && bash ./redis_init.sh && uvicorn app.main:app --host 0.0.0.0 --port 80"]
