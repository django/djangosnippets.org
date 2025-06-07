# Pull base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements /requirements
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

# Set work directory
WORKDIR /code

# Copy project
COPY . /code/

# Set the default command (if your application has a main entry point)
# CMD ["python", "your_main_script.py"]
