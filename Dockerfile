# pull official base image
# Uses the official Python 3.11.9 slim image as the base.
#  The slim version is a lightweight variant of the Python image, which reduces the final container size.
FROM python:3.11.9-slim

# Sets /usr/src/app as the working directory where the application code will be stored and executed.
WORKDIR /usr/src/app

# set environment variables
# PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files, reducing unnecessary disk usage.
#  PYTHONUNBUFFERED=1: Ensures that the Python output (e.g., print statements) is immediately flushed to the terminal/logs, making debugging easier.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Updates the package list (apt-get update).
# Installs necessary system dependencies:
# software-properties-common: For managing repository dependencies.
# postgresql, postgresql-client, postgresql-contrib: PostgreSQL database and client tools.
# gcc: GNU Compiler Collection (needed for compiling certain Python packages).
# python3-dev: Header files and libraries needed for compiling Python packages.
# musl-dev: Minimal C standard library, useful for compatibility.
# libssl-dev, openssl: Required for secure connections and encryption.
# wget: Utility for downloading files.
RUN apt-get update \
    && apt-get install -y  \
        software-properties-common postgresql  \
        postgresql-client postgresql-contrib gcc \
        python3-dev musl-dev libssl-dev openssl wget \
        netcat-openbsd
        

# install dependencies
# Upgrades pip to the latest version.
# Copies requirements.txt (which contains the list of dependencies) into the container.
# Installs the required Python packages using pip.
# The flag --use-deprecated=legacy-resolver ensures compatibility with older dependency resolution behavior.
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --use-deprecated=legacy-resolver


# copy entrypoint.sh
# Copies the entrypoint.sh script into the container.
# Removes Windows-style carriage return characters (\r) to ensure the script runs properly in Linux environments.
# Makes the script executable (chmod +x).
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copies all project files from the host machine to the container.
COPY . .

# Specifies that the entrypoint.sh script should be executed when the container starts.
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]