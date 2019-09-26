# Use Alpine as base
FROM alpine:latest

# Maintainer
MAINTAINER jas.atwal@docker.com

# Install python and pip
RUN apk add --no-cache --update python3

# Upgrade pip
RUN pip3 install --upgrade pip

# Install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# Copy files required for the app to run
COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/

# Expose the app on Flask default (5000)
EXPOSE 5000

# Run the application
CMD ["python3", "/usr/src/app/app.py"]
