FROM python:alpine3.7

WORKDIR /app
RUN apk --update add build-base gcc abuild binutils linux-headers libffi-dev libxml2 libxml2-dev libxslt-dev \
    make bash jq curl && \
  rm -rf /tmp/* /var/cache/apk/*

ENV KUBE_LATEST_VERSION="v1.13.7"

RUN echo "Installing kubectl $KUBE_LATEST_VERSION" \
 && curl -sL https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \
 && chmod +x /usr/local/bin/kubectl

COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app
