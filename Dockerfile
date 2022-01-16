FROM python:3.10

# Copy local code to the container image
COPY . /app

# Sets the working directory
WORKDIR /app

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Upgrade PIP
RUN pip install --upgrade pip

#Install python libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP webscraper
ENV FLASK_ENV production
ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 3 --threads 8 --timeout 0 webscraper:app