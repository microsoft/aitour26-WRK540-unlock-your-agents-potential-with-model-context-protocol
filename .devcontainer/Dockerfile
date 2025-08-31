FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# Install pip for Python 3.13
RUN python -m pip install --upgrade pip

# Install DevTunnel CLI
RUN curl -sL https://aka.ms/DevTunnelCliInstall | bash && \
    cp /root/bin/devtunnel /usr/local/bin/devtunnel

# Install Aspire CLI
RUN curl -sSL https://aspire.dev/install.sh | bash && \
    cp /root/.aspire/bin/* /usr/local/bin/ 2>/dev/null || true

# Install the packages required to run the workshop as a student
COPY requirements.lock.txt .
RUN pip install -r requirements.lock.txt
