#!/bin/bash

# Ensure the logs directory exists
mkdir -p /usr/src/app/logs

# Start Nginx in the background and capture the process ID
echo "Starting Nginx..."
nginx &
NGINX_PID=$!

# Wait for Nginx to start fully
echo "Waiting for Nginx to start..."
sleep 5

# Test internet connectivity before attempting Certbot
if ! ping -c 3 e6.o.lencr.org; then
  echo "Cannot resolve e6.o.lencr.org. Check DNS or firewall settings."
  exit 1
fi

# Obtain SSL certificates via Certbot
echo "Obtaining SSL certificates..."
certbot --nginx -d pmsolution-facture.org -d www.pmsolution-facture.org --email ibhayk@gmail.com --agree-tos --no-eff-email --non-interactive

if [ $? -eq 0 ]; then
  echo "Certificates successfully obtained."
else
  echo "Failed to obtain certificates."
  exit 1
fi

# Reload Nginx to apply the new certificates
echo "Reloading Nginx..."
nginx -s reload

if [ $? -eq 0 ]; then
  echo "Nginx reloaded successfully."
else
  echo "Failed to reload Nginx."
  exit 1
fi

# Set up cron job for automatic SSL certificate renewal
echo "Setting up automatic SSL certificate renewal..."
(crontab -l; echo "0 0,12 * * * certbot renew --quiet && nginx -s reload") | crontab -

# Keep the Nginx process running in the foreground
echo "Keeping Nginx running in the foreground..."
wait $NGINX_PID
