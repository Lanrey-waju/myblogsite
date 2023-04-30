FROM nginx:1.23.4-alpine

LABEL maintainer="lanreywaju97@gmail.com"

COPY ./nginx/* /etc/nginx/
COPY ./run.sh /run.sh

ENV APP_HOST=web
ENV APP_PORT=9000

RUN apk add --no-cache openssl bash
RUN chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

CMD [ "/run.sh" ]
