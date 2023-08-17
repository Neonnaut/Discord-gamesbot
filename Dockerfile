FROM python:3.10
WORKDIR /bot
COPY REQUIREMENTS.txt /bot/
RUN pip install -r REQUIREMENTS.txt
COPY . /bot
CMD python gamebot