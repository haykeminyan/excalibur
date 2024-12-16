FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Debugging: Run apt-get update and check repositories
RUN apt-get update -y || { cat /var/log/apt/term.log && exit 1; }

# Install required packages with error checking
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-certbot-nginx nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* || { echo "Installation failed"; exit 1; }

EXPOSE 80 443

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]
