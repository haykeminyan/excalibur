#!/bin/bash

# Start Nginx in the background
nginx &

# Wait for Nginx to start fully
sleep 5

# Request SSL certificates using Certbot and the Nginx plugin (this will not prompt for input)
certbot --nginx -d pmsolution-facture.org -d www.pmsolution-facture.org --email ibhayk@gmail.com --agree-tos --no-eff-email --non-interactive

# Reload Nginx to apply the new SSL certificates
nginx -s reload

# Keep the Nginx process running in the foreground
wait $(cat /var/run/nginx.pid)
