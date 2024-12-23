FROM nginx:latest

# Reinstall Nginx and install necessary build dependencies
RUN apt-get update -y && \
    apt-get install -y \
    build-essential \
    curl \
    git \
    libpcre3-dev \
    libssl-dev \
    zlib1g-dev \
    wget \
    libtool \
    automake \
    libevent-dev \
    pkg-config \
    gcc \
    g++ \
    ca-certificates \
    cargo \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Rust 1.67 or newer (required by quiche)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    rustup update stable

# Install QUICHE (QUIC and HTTP/3 support for Nginx)
RUN git clone --recursive https://github.com/cloudflare/quiche /tmp/quiche && \
    cd /tmp/quiche && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    cargo build --release && \
    cp target/release/libquiche.so /usr/local/lib/ && \
    ldconfig

# Manually download the nginx-quic module from Cloudflare or the appropriate source
RUN cd /usr/local/src && \
    wget https://nginx.org/download/nginx-1.27.3.tar.gz && \
    tar -xzvf nginx-1.27.3.tar.gz && \
    cd nginx-1.27.3 && \
    # Download and apply nginx-quic module directly from Cloudflare or other sources
    wget https://github.com/cloudflare/nginx-quic/releases/download/v1.27.3/nginx-quic-v1.27.3.patch && \
    patch -p1 < nginx-quic-v1.27.3.patch && \
    # Configure Nginx with QUIC and HTTP/3 support
    ./configure \
    --with-http_v2_module \
    --with-http_ssl_module \
    --with-http_quic_module \
    --with-cc-opt="-I/usr/local/src/quiche/include" \
    --with-ld-opt="-L/usr/local/src/quiche/lib" && \
    make && \
    make install

# Install Certbot and Nginx plugin for Certbot
RUN apt-get update -y && \
    apt-get install -y certbot python3-certbot-nginx cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories for SSL certificates and the challenge
RUN mkdir -p /etc/nginx/ssl /var/www/certbot

# Copy Nginx configuration and your HTML directory
COPY nginx.conf /etc/nginx/nginx.conf
COPY html/ /var/www/html/

# Copy mime.types if needed (or use the default Nginx one)
COPY mime.types /etc/nginx/mime.types

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the custom entrypoint script to manage Nginx and Certbot
ENTRYPOINT ["/entrypoint.sh"]

# Ensure that Nginx runs in the foreground (entrypoint script will handle reloading)
CMD ["nginx", "-g", "daemon off;"]
