#!/bin/bash
set -e

# User inputs
DOMAIN="odoo-demo.expertsvision.org"
EMAIL="mahmoud.aboelsoud.p@gmail.com"

# Fail if DOMAIN not set
if [ -z "$DOMAIN" ]; then
  echo "❌ ERROR: DOMAIN variable is not set! (export DOMAIN=yourdomain.com)"
  exit 1
fi

# Fail if EMAIL not set
if [ -z "$EMAIL" ]; then
  echo "❌ ERROR: EMAIL variable is not set! (export EMAIL=you@example.com)"
  exit 1
fi

echo "✅ Using DOMAIN=$DOMAIN and EMAIL=$EMAIL"

if [ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
  echo "✅ Generating SSL certificate ..."
  sudo certbot certonly --standalone -d $DOMAIN --agree-tos -m $EMAIL --non-interactive || {
      echo "❌ Certbot failed!"
      exit 1
  }
else
  echo "🔄 SSL certificate for $DOMAIN already exists, skipping generation."
fi