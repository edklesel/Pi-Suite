FROM alpine:latest

RUN apk add --update-cache python3 curl

RUN mkdir /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install pyyaml

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.9/supercronic-linux-arm \
    SUPERCRONIC=supercronic-linux-arm \
    SUPERCRONIC_SHA1SUM=47481c3341bc3a1ae91a728e0cc63c8e6d3791ad

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

RUN wget -q --no-check-certificate https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.py
RUN wget -q --no-check-certificate https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.cron
RUN wget -q --no-check-certificate https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.yml

CMD ["supercronic", "./dockmon.cron"]