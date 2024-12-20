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

# Create a basic index.html file
RUN echo "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Welcome</title></head><body><h1>Success! Your Nginx server is running with SSL.</h1></body></html>" > /var/www/html/index.html

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Set stop signal
STOPSIGNAL SIGTERM

# Command to run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
