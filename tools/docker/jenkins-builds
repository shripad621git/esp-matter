ARG VERSION=latest
FROM espressif/esp-matter:${VERSION} as build

RUN set -x \
    && useradd -s /bin/bash -g root -u 1001 -m espressif \
    && usermod --password $(echo "espressif" | openssl passwd -1 -stdin) espressif \
    && chown -R espressif /opt/espressif/ \
    && : # last line

USER espressif



