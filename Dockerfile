# Pull base image
FROM python:3.7.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



# Install dependencies
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

# Set work directory
WORKDIR /code

# Copy project
COPY . /code/
