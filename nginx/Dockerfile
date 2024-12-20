FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-certbot-nginx nginx openssl && \
    apt-get upgrade -y openssl nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* || { echo "Installation failed"; exit 1; }

# Create SSL directory and generate self-signed certificate with OpenSSL
RUN mkdir -p /etc/nginx/ssl && \
    openssl genpkey -algorithm RSA -out /etc/nginx/ssl/selfsigned.key && \
    openssl req -new -key /etc/nginx/ssl/selfsigned.key \
    -out /etc/nginx/ssl/selfsigned.csr \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN=pmsolution-facture.org" && \
    openssl req -x509 -key /etc/nginx/ssl/selfsigned.key \
    -in /etc/nginx/ssl/selfsigned.csr \
    -out /etc/nginx/ssl/selfsigned.crt -days 365

# Copy Nginx configuration and HTML files
COPY nginx.conf /etc/nginx/nginx.conf
COPY html/ /var/www/html/

RUN apt-get update -y && \
    apt-get install -y cron

# Ensure permissions are correct for Certbot and Nginx
RUN chmod -R 755 /var/www/html && \
    chmod -R 755 /etc/nginx/ssl

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Set stop signal
STOPSIGNAL SIGTERM

# Command to run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
