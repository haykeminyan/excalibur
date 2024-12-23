#!/bin/bash

# Start Nginx in the background and capture the process ID
echo "Starting Nginx..."
nginx &

# Capture the Nginx process PID so we can wait on it later
NGINX_PID=$!

# Wait for Nginx to start fully (adjust time if necessary)
echo "Waiting for Nginx to start..."
sleep 5

# Obtain SSL certificates via Certbot
echo "Obtaining SSL certificates..."
certbot --nginx -d pmsolution-facture.org -d www.pmsolution-facture.org --email ibhayk@gmail.com --agree-tos --no-eff-email --non-interactive

# Ensure certificates were successfully obtained
if [ $? -eq 0 ]; then
  echo "Certificates successfully obtained."
else
  echo "Failed to obtain certificates."
  exit 1
fi

# Reload Nginx to apply the new certificates
echo "Reloading Nginx..."
nginx -s reload

# Log the Nginx reload result
if [ $? -eq 0 ]; then
  echo "Nginx reloaded successfully."
else
  echo "Failed to reload Nginx."
  exit 1
fi

# Keep the Nginx process running in the foreground
echo "Keeping Nginx running in the foreground..."
wait $NGINX_PID
