FROM lachlanevenson/k8s-kubectl:v1.11.2 as kubectlContainer

FROM python:alpine3.6
COPY --from=kubectlContainer /usr/local/bin/kubectl /usr/local/bin/kubectl

WORKDIR /app
RUN apk --update add gcc musl-dev libffi-dev linux-headers python3-dev openssl-dev make bash jq curl && \
  rm -rf /tmp/* /var/cache/apk/*

COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app
