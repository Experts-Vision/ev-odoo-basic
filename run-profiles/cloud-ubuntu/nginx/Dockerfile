FROM nginx:stable


ARG DOMAIN

# Copy custom nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN apt-get update && apt-get install -y gettext-base && \
    envsubst '${DOMAIN}' < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf.tmp && \
    mv /etc/nginx/conf.d/default.conf.tmp /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80 443
