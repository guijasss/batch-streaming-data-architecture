FROM alpine:latest

RUN wget -P /tmp https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.9.1.1-1_amd64.apk

RUN apk update && \
    apk add --allow-untrusted --no-cache curl gnupg python3 python3-dev py3-pip bash unixodbc-dev build-base nano /tmp/msodbcsql17_17.9.1.1-1_amd64.apk

RUN case $(uname -m) in \
        x86_64)   architecture="amd64" ;; \
        arm64)   architecture="arm64" ;; \
        *) architecture="unsupported" ;; \
    esac && \
    if [[ "unsupported" == "$architecture" ]]; then \
        echo "Alpine architecture $(uname -m) is not currently supported."; \
        exit 1; \
    fi && \
    curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_$architecture.apk && \
    curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_$architecture.apk && \
    curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_$architecture.sig && \
    curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_$architecture.sig && \
    curl https://packages.microsoft.com/keys/microsoft.asc  | gpg --import - && \
    gpg --verify msodbcsql18_18.3.2.1-1_$architecture.sig msodbcsql18_18.3.2.1-1_$architecture.apk && \
    gpg --verify mssql-tools18_18.3.1.1-1_$architecture.sig mssql-tools18_18.3.1.1-1_$architecture.apk && \
    apk add --allow-untrusted msodbcsql18_18.3.2.1-1_$architecture.apk && \
    apk add --allow-untrusted mssql-tools18_18.3.1.1-1_$architecture.apk

RUN mkdir /home/app
WORKDIR /home/app

COPY insert_data.py /home/app/insert_data.py
COPY requirements.txt /home/app/requirements.txt

RUN python3 -m venv venv && source venv/bin/activate && pip install pyodbc Faker