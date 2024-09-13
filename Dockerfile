# Download Python, uWSGI, and Nginx to serve the Flask app
FROM tiangolo/uwsgi-nginx-flask:python3.8

# Set environment variables for the uWSGI configuration
ENV LISTEN_PORT=8081

# Expose the desired port (8081)
EXPOSE 8081

#Install modules
RUN pip3 install requests
RUN pip3 install pillow
RUN pip3 install flask
RUN pip3 install flask_caching


# Copy your Flask app code to the /app directory
COPY ./app /app


COPY ./arsewards.py /app/arsewards.py


# The base image already takes care of running uWSGI and Nginx
