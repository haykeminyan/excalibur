#!/bin/bash

# Start Nginx in the background
nginx &

# Capture the Nginx process PID so we can wait on it later
NGINX_PID=$!

# Wait for Nginx to start fully
sleep 5

# Request SSL certificates using Certbot and the Nginx plugin (this will not prompt for input)
certbot --nginx -d pmsolution-facture.org -d www.pmsolution-facture.org --email ibhayk@gmail.com --agree-tos --no-eff-email --non-interactive

# Reload Nginx to apply the new SSL certificates
nginx -s reload

# Wait for Nginx to stop gracefully
wait $NGINX_PID
