# cors-proxy
[![Publish Release and Build Docker](https://github.com/reon04/cors-proxy/actions/workflows/release.yml/badge.svg)](https://github.com/reon04/cors-proxy/actions/workflows/release.yml)

```
Simple CORS Proxy

Usage:  
  /        Shows help  
  /<url>   Create a request to <url> (must include scheme)

Features:
  - Adds Access-Control-Allow-Origin: *
  - Supports redirects
  - Strips cookies from request
  - Blocks local/private network targets
  - Supports GET, POST, PUT, PATCH and DELETE
```

### Example Deployment

Deploy the container using docker compose:

```
services:
  cors-proxy:
    container_name: cors-proxy
    image: "ghcr.io/reon04/cors-proxy:latest"
    restart: unless-stopped
    environment:
      ALLOWED_ORIGINS: "YOUR_ORIGINS"
```

### Envirionment Variables

Env  | Default | Description
---- | ------- | -----------
ALLOWED_ORIGINS | | If set, requests whose origin is not listed are blocked.<br>If this list is empty, all origins are allowed.<br>Comma separated. Example: `https://good.example.com,http://good.example.com`

## LICENSE

This project is licensed under [MIT](LICENSE).