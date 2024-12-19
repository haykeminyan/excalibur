FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages, including Nginx and Certbot
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-certbot-nginx nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* || { echo "Installation failed"; exit 1; }

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Copy Nginx configuration and SSL certificates
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./ssl/cert.crt /etc/nginx/ssl/cert.crt
COPY ./ssl/privkey.pem /etc/nginx/ssl/privkey.pem

# Set stop signal
STOPSIGNAL SIGTERM

# Command to run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
