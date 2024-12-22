#!/bin/bash

# Start Nginx in the background
nginx &

# Capture the Nginx process PID so we can wait on it later
NGINX_PID=$!

# Wait for Nginx to start fully
sleep 5

# Try to request SSL certificates using Certbot, check if it succeeded
certbot --nginx -d pmsolution-facture.org -d www.pmsolution-facture.org --email ibhayk@gmail.com --agree-tos --no-eff-email --non-interactive

# Check if Certbot was successful
if [ $? -eq 0 ]; then
  echo "SSL certificates successfully obtained!"
  # Reload Nginx to apply the new SSL certificates
  nginx -s reload
else
  echo "Certbot failed. Not reloading Nginx."
  exit 1
fi

# Wait for Nginx to stop gracefully
wait $NGINX_PID
