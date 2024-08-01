# Use Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Set environment variables to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    nano

# Add Microsoft repository and install ODBC Driver and SQL Server tools
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools

# Install Python packages
RUN python3 -m venv /venv && \
    /venv/bin/pip install pyodbc Faker pandas

# Set environment variable to use the Python virtual environment
ENV PATH="/venv/bin:$PATH"

# Create application directory and set it as the working directory
RUN mkdir /home/app
WORKDIR /home/app

# Copy application files into the container
COPY generate_order_data.py /home/app/generate_order_data.py
COPY requirements.txt /home/app/requirements.txt
COPY mssql.py /home/app/mssql.py
COPY /data /home/app/data