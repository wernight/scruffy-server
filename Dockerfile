FROM alpine:3.8

MAINTAINER Werner Beroux <werner@beroux.com>

COPY . /opt/scruffy-server

RUN set -x \
    && apk add --update \
        graphviz \
        libjpeg \
        librsvg \
        python \
        py-pillow \
        zlib \
    && apk add -t .build-deps \
        make \
        g++ \
        git \
        python-dev \
        py-pip \
        py-setuptools \
        zlib-dev \

    && mkdir -p /usr/share/fonts/opentype/dion \
    && cd /usr/share/fonts/opentype/dion \
    && wget -O dion.zip 'http://dl.dafont.com/dl/?f=dion' \
    && unzip dion.zip \
    && rm dion.zip \
    && fc-cache -f -v \

    && wget -O- https://mirrors.kernel.org/gnu/plotutils/plotutils-2.6.tar.gz | tar -xz -C /tmp \
    && cd /tmp/plotutils-2.6 \
    && ./configure \
    && make install \
    && make installcheck \
    && cd pic2plot \
    && make install \
    && cd - \
    && rm -rf /tmp/plotutils-2.6 \

    && cd /opt/scruffy-server \
    && pip install -r requirements.txt \

    && apk del --purge .build-deps \
    && rm /var/cache/apk/* \

    && adduser -S -u 35726 -s /sbin/nologin scruffy

# Run as non-root user
USER scruffy

WORKDIR /opt/scruffy-server
EXPOSE 8080
CMD ["python", "server.py"]
