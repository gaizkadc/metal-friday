FROM python:3.8-slim-buster

WORKDIR /metal-friday

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "metal-friday.py"]