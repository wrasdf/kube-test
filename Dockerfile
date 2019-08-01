FROM python:alpine3.7

WORKDIR /app
RUN apk --update add build-base gcc abuild binutils linux-headers libffi-dev libxml2 libxml2-dev libxslt-dev \
    make bash jq curl && \
  rm -rf /tmp/* /var/cache/apk/*

ENV KUBECTL_VERSION="v1.15.0"
RUN echo "Installing kubectl $KUBECTL_VERSION" \
 && curl -sL https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \
 && chmod +x /usr/local/bin/kubectl

ENV ISTIOCTL_VERSION="1.1.3"
RUN echo "Installing istioctl $ISTIOCTL_VERSION" \
 && curl -fsSLo istio.tar.gz https://github.com/istio/istio/releases/download/$ISTIOCTL_VERSION/istio-$ISTIOCTL_VERSION-linux.tar.gz \
 && tar -xzf istio.tar.gz \
 && mv istio-$ISTIOCTL_VERSION/bin/istioctl /usr/local/bin/ \
 && chmod +x /usr/local/bin/istioctl \
 && rm -rf istio.tar.gz istio-$ISTIOCTL_VERSION

COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app
