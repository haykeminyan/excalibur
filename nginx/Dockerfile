FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages, including Nginx and Certbot
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-certbot-nginx nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* || { echo "Installation failed"; exit 1; }


RUN mkdir -p /etc/nginx/ssl && \
    openssl genpkey -algorithm RSA -out /etc/nginx/ssl/selfsigned.key && \
    openssl req -new -key /etc/nginx/ssl/selfsigned.key -out /etc/nginx/ssl/selfsigned.csr && \
    openssl req -x509 -key /etc/nginx/ssl/selfsigned.key -in /etc/nginx/ssl/selfsigned.csr -out /etc/nginx/ssl/selfsigned.crt -days 365

# Copy Nginx configuration and SSL certificates
COPY nginx.conf /etc/nginx/nginx.conf



# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Set stop signal
STOPSIGNAL SIGTERM

# Command to run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
