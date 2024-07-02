FROM python:3.9-alpine

WORKDIR /app/transaksi

COPY ./transaksi /app/transaksi/
COPY ./.env /restapi/.env

RUN apk add postgresql-libs
RUN apk add --virtual .build-deps gcc musl-dev postgresql-dev 
RUN python3 -m pip install -r /app/transaksi/requirements.txt
RUN apk --purge del .build-deps

EXPOSE 8000

CMD [ "uvicorn", "main:app" , "--host", "0.0.0.0", "--port", "8000", "--reload"]