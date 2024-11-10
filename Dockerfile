FROM python:3.9

WORKDIR /code

# copy files for initial configuration
COPY ./requirements.txt /code/requirements.txt
COPY ./redis_init.sh /code/redis_init.sh

# copy app files
COPY ./app /code/app

# install required python libraries
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# expose port
EXPOSE 80

# run app on uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80" ]