FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# Install pip for Python 3.13
RUN python -m pip install --upgrade pip

# Install DevTunnel CLI
RUN curl -sL https://aka.ms/DevTunnelCliInstall | bash && \
    cp /root/bin/devtunnel /usr/local/bin/devtunnel

# Install the packages required to run the workshop as a student
COPY ../src/python/workshop/requirements.txt .
RUN pip install -r requirements.txt

# Install the packages required for development
COPY ../requirements-dev.txt .
RUN pip install -r requirements-dev.txt

ENV ENVIRONMENT=container