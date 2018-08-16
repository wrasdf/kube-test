FROM python:alpine3.6

WORKDIR /app
RUN apk --update --no-cache add build-base python3-dev libffi-dev openssl-dev bash jq curl ca-certificates && \
  rm -rf /tmp/* /var/cache/apk/*

ENV KUBE_LATEST_VERSION="v1.11.2"

RUN echo "Installing kubectl $KUBE_LATEST_VERSION" \
 && curl -s -L curl -LO https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \
 && chmod +x /usr/local/bin/kubectl

COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app
