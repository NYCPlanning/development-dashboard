FROM python:3.6.7-slim-stretch

WORKDIR /app

COPY . .

RUN python3 -m venv venv

RUN pip3 install --no-cache-dir -r requirements.txt 

CMD [ "./entrypoint.sh" ]

EXPOSE 5000