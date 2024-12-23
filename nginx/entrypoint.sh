#!/bin/bash

# Start Nginx in the background
nginx &

# Capture the Nginx process PID so we can wait on it later
NGINX_PID=$!

# Wait for Nginx to start fully
sleep 5

# Run Certbot to obtain the SSL certificates and deploy them
certbot --nginx -d pmsolution-facture.org -d www.pmsolution-facture.org --email ibhayk@gmail.com --agree-tos --no-eff-email --non-interactive

# Keep the Nginx process running in the foreground
wait $NGINX_PID
