# Use the official Azure Functions Python image
FROM mcr.microsoft.com/azure-functions/python:4-python3.10

# Copy project and dependency files
COPY pyproject.toml /
COPY poetry.lock /

# Install dependencies using Poetry
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Set the working directory to where the function code will reside
WORKDIR /home/site/wwwroot

# Don't copy the function code here - it will be mounted in the Docker Compose
# The following line is commented out to avoid duplication with volume mounts
# COPY ./code/backend/azure_function /home/site/wwwroot/
