FROM alpine:3.12

COPY files/ /

RUN apk update && \
    apk upgrade && \
    apk add --update nginx && \
    chown -R root:nginx /etc/nginx && \
    chmod -R a+rX /etc/nginx && \
    chmod -R a+rwX /var/lib/nginx && \
    rm -rf /etc/nginx/conf.d/default.conf /var/cache/apk/*

EXPOSE 8080
CMD ["/usr/sbin/nginx", "-c", "/etc/nginx/override.conf"]
USER nginx:nginx
