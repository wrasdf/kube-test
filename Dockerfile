FROM lachlanevenson/k8s-kubectl:v1.9.6 as kubectlContainer

FROM python:alpine3.6
COPY --from=kubectlContainer /usr/local/bin/kubectl /usr/local/bin/kubectl

RUN mkdir /app
WORKDIR /app

RUN apk add --update bash curl openssl jq make

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
