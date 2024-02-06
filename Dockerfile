FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app
# RUN mkdir /app/static && mkdir /app/media && chown -R yt:yt /yt && chmod 755 /yt
RUN mkdir /app/static && mkdir /app/media
RUN apt-get update && apt-get install -y telnet
# COPY requirements.txt .
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
# COPY admin_app admin_app
# COPY my_app my_app
# COPY myproject myproject
# COPY users users
# COPY manage.py .
# COPY requirements.txt .

CMD ["gunicorn", "-b", "0.0.0.0:8000", "myproject.wsgi:application"]


# RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
#     libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

# RUN sudo apt update && apt -qy install gcc python3 python3-pip libmysqlclient-dev

# RUN useradd -rms /bin/bash rem && chmod 777 /opt /run
# RUN wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
#      --output-document /usr/local/share/ca-certificates/root.crt && \
# chmod 0600 /usr/local/share/ca-certificates/root.crt

# # ADD ./root.crt /usr/local/share/ca-certificates/foo.crt
# RUN chmod 644 /usr/local/share/ca-certificates/root.crt && update-ca-certificates