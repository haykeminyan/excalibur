# Use official Nginx image as the base
FROM nginx:latest

# Install Certbot and the Nginx plugin
RUN apt-get update -y && \
    apt-get install -y certbot python3-certbot-nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories for SSL certificates and the challenge
RUN mkdir -p /etc/nginx/ssl /var/www/certbot

# Copy Nginx configuration and your HTML directory
COPY nginx.conf /etc/nginx/nginx.conf
COPY html/ /var/www/html/

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Entry point: Start Nginx, request SSL certificates, and reload Nginx after fetching them
ENTRYPOINT ["sh", "-c", "nginx && certbot --nginx -d pmsolution-facture.org -d www.pmsolution-facture.org --email ibhayk@gmail.com --agree-tos --no-eff-email && nginx -s reload"]

# Ensure that Nginx runs in the foreground
CMD ["nginx", "-g", "daemon off;"]
