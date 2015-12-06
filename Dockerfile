FROM debian:jessie

MAINTAINER Werner Beroux <werner@beroux.com>

COPY . /opt/scruffy-server

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        fonts-tlwg-purisa \
        git \
        graphviz \
        libjpeg-dev \
        librsvg2-bin \
        plotutils \
        python-dev \
        python-pil \
        python-pip \
        python-setuptools \
        zlib1g-dev \

    && git clone https://github.com/aivarsk/scruffy.git /opt/scruffy \
    && cd /opt/scruffy \
    && python setup.py install \
    && cd - \
    && rm -rf scruffy \

    && cd /opt/scruffy-server \
    && pip install -r requirements.txt \

    && apt-get purge --auto-remove -y \
        git \
        python-dev \
        python-pip \
        python-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \

    && useradd --system --uid 35726 -m --shell /usr/sbin/nologin scruffy

# Run as non-root user
USER scruffy

WORKDIR /opt/scruffy-server
EXPOSE 8080
CMD ["python", "server.py"]
