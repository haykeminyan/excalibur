#!/bin/bash

# Simple healthcheck to ensure the app is running
curl -f http://localhost:8000/healthz || exit 1
