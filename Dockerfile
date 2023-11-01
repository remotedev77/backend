FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
#     libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

# RUN sudo apt update && apt -qy install gcc python3 python3-pip libmysqlclient-dev

# RUN useradd -rms /bin/bash rem && chmod 777 /opt /run
RUN wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
     --output-document /usr/local/share/ca-certificates/root.crt && \
chmod 0600 /usr/local/share/ca-certificates/root.crt

# ADD ./root.crt /usr/local/share/ca-certificates/foo.crt
RUN chmod 644 /usr/local/share/ca-certificates/root.crt && update-ca-certificates

WORKDIR /app
ENV SECRET_KEY="django-insecure-0z6#tj6pz*b$k1#v8of)1h@mdd+&q-bqthjad#9((zm5y=a=w+"
ENV OPTIONS=/usr/local/share/ca-certificates/root.crt
ENV HOST=rc1b-jxy7jxw137n43syc.mdb.yandexcloud.net
ENV PORT=3306
ENV USER=nok_trenazher_user
ENV PASSWORD=7yr.d::964jZbcM
ENV NAME=nok_trenazher_db
# RUN mkdir /app/static && mkdir /app/media && chown -R yt:yt /yt && chmod 755 /yt
RUN mkdir /app/static && mkdir /app/media
COPY requirements.txt .
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
COPY admin_app admin_app
COPY my_app my_app
COPY myproject myproject
COPY users users
COPY manage.py .
COPY requirements.txt .

CMD ["gunicorn", "-b", "0.0.0.0:8000", "myproject.wsgi:application"]