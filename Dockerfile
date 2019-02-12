
FROM python:3.7-alpine

# Set working directory
WORKDIR /opt

# Set environment variables
ENV DEPS g++ gcc libc-dev  libxml2-dev libxslt-dev libffi libffi-dev jpeg-dev zlib-dev
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/opt/
ENV TZ=Europe/Madrid

# Install SO dependencies
RUN apk --update add --no-cache $DEPS

# Install app dependencies
COPY requirements.txt requirements.txt
COPY requirements-test.txt requirements-test.txt
ARG INCLUDE_TEST=0
RUN if [ $INCLUDE_TEST == 1 ]; then                                 \
        REQUIREMENTS_FILE="/opt/requirements-test.txt";             \
    else                                                            \
        REQUIREMENTS_FILE="/opt/requirements.txt";                  \
    fi;                                                             \
    pip install -r $REQUIREMENTS_FILE