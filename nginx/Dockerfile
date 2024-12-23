# Use the latest Nginx image
FROM nginx:latest

# Install required dependencies for building Nginx with HTTP/3 support
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
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (Required for Quiche and ngtcp2)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    rustup update stable

# Install ngtcp2 (QUIC transport library) and quiche (QUIC and HTTP/3 library)
RUN git clone --recursive https://github.com/ngtcp2/ngtcp2 /tmp/ngtcp2 && \
    cd /tmp/ngtcp2 && \
    mkdir build && cd build && \
    cmake .. && make && make install && \
    cd / && rm -rf /tmp/ngtcp2

RUN git clone --recursive https://github.com/cloudflare/quiche /tmp/quiche && \
    cd /tmp/quiche && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    cargo build --release && \
    cp target/release/libquiche.so /usr/local/lib/ && \
    ldconfig && \
    rm -rf /tmp/quiche

# Clone the Nginx source code
RUN cd /usr/local/src && \
    wget https://nginx.org/download/nginx-1.27.3.tar.gz && \
    tar -xzvf nginx-1.27.3.tar.gz && \
    cd nginx-1.27.3

# Patch Nginx to include QUIC and HTTP/3 support from the Nginx QUIC module
RUN cd /usr/local/src/nginx-1.27.3 && \
    git clone --single-branch --branch main https://github.com/nginx/nginx-quic.git && \
    cd nginx-quic && \
    ./configure \
    --with-http_v2_module \
    --with-http_ssl_module \
    --with-http_quic_module \
    --with-openssl=/usr/local/src/nginx-1.27.3/openssl \
    --with-ngtcp2=/usr/local/lib \
    --with-quiche=/usr/local/lib && \
    make && \
    make install

# Install Certbot and Nginx plugin for Certbot to handle SSL certificates
RUN apt-get update -y && \
    apt-get install -y certbot python3-certbot-nginx cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories for SSL certificates and the challenge directory for Certbot
RUN mkdir -p /etc/nginx/ssl /var/www/certbot

# Copy custom Nginx configuration and your HTML directory
COPY nginx.conf /etc/nginx/nginx.conf
COPY html/ /var/www/html/

# Copy mime.types (optional, or use default Nginx one)
COPY mime.types /etc/nginx/mime.types

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Copy and set permissions for the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script to manage Nginx and Certbot
ENTRYPOINT ["/entrypoint.sh"]

# Ensure Nginx runs in the foreground
CMD ["nginx", "-g", "daemon off;"]
