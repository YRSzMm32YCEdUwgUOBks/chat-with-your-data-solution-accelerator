# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.10-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.10

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# Ensure we are in the function app script root
WORKDIR /home/site/wwwroot

COPY requirements.txt /
RUN pip install -r /requirements.txt

# Copy the function app code into the script root
COPY . .
# Note: keep function_app.py in place for decorators to load correctly
