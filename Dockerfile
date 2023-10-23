FROM python:3.10.9
SHELL ["/bin/bash", "-c"]
ENV PYTHONUNBUFFERED 1

RUN mkdir /remote
WORKDIR /remote
ADD . /remote/
COPY requirements.txt /remote/
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "myproject.wsgi:application"]