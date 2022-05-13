FROM python:buster AS base

WORKDIR /app

COPY ./main.py ./requirements.txt /app/

FROM base AS install-deps
ENV ACCEPT_EULA=Y

RUN apt-get update && \
    apt-get install -qq curl

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
    
RUN apt-get update && \
    apt-get install -qq msodbcsql18 && \
    apt-get install -y unixodbc-dev

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
