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
      BLOCKED_NETWORKS: "YOUR_EXTERNAL_IP_NETWORK"
      ALLOWED_ORIGINS: "YOUR_ORIGINS"
    ports:
      - "80:80"
```

By default, the proxy blocks requests to local and private networks to help prevent SSRF attacks. BLOCKED_NETWORKS can be used to define additional target networks that should be denied (e.g. the external IP network of the server on which the proxy is deployed). ALLOWED_ORIGINS can be used to limit which browser origins are allowed to access the proxy.

### Environment Variables

Env  | Default | Description
---- | ------- | -----------
BLOCKED_NETWORKS | | If set, requests with targets in these networks are additionally blocked.<br>If this list is empty, only standard local networks are blocked.<br>Comma separated. Example: `1.2.3.4/32,12.34.56.0/24`
ALLOWED_ORIGINS | | If set, requests whose origin is not listed are blocked.<br>If this list is empty, all origins are allowed.<br>Comma separated. Example: `https://good.example.com,http://good.example.com`

## LICENSE

This project is licensed under [MIT](LICENSE).