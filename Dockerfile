FROM python:alpine3.7
RUN apk --update add build-base gcc abuild binutils linux-headers libffi-dev libxml2 libxml2-dev libxslt-dev \
    make bash jq curl && \
  rm -rf /tmp/* /var/cache/apk/*

ENV KUBECTL_VERSION="v1.15.0"
RUN echo "Installing kubectl $KUBECTL_VERSION" \
 && curl -sL https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \
 && chmod +x /usr/local/bin/kubectl

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app
