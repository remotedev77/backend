FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

# RUN useradd -rms /bin/bash rem && chmod 777 /opt /run

WORKDIR /remote

# RUN mkdir /remote/static && mkdir /remote/media && chown -R yt:yt /yt && chmod 755 /yt
RUN mkdir /remote/static && mkdir /remote/media

COPY admin_app admin_app
COPY my_app my_app
COPY myproject myproject
COPY users users
COPY manage.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

# EXPOSE 8000
# USER yt

CMD ["gunicorn","-b","0.0.0.0:8001","myproject.wsgi:application"]
