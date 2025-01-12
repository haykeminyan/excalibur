#!/bin/bash

# Ensure the logs directory exists
mkdir -p /usr/src/app/logs

# Start Nginx
echo "Starting Nginx..."
nginx -g "daemon off;" &

# Capture the Nginx process PID so we can wait on it later
NGINX_PID=$!

# Wait for Nginx to start fully (adjust time if necessary)
echo "Waiting for Nginx to start..."
sleep 5

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

# Set up automatic renewal cron job
echo "Setting up automatic SSL certificate renewal..."
cat <<EOL > /etc/cron.d/certbot-renew
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

0 0,12 * * * root certbot renew --quiet --deploy-hook "nginx -s reload" >> /usr/src/app/logs/certbot-renew.log 2>&1
EOL

chmod 0644 /etc/cron.d/certbot-renew
crontab /etc/cron.d/certbot-renew

# Start cron in the foreground
echo "Starting cron..."
cron -f &
CRON_PID=$!

# Wait for Nginx and cron processes
wait $NGINX_PID
wait $CRON_PID

# Keep the container running by running an infinite loop or dummy process
tail -f /dev/null
