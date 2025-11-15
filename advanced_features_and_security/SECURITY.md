# Django HTTPS Security Configuration

## Security Settings Applied:
- SECURE_SSL_REDIRECT: True
- SECURE_HSTS_SECONDS: 31536000
- SECURE_HSTS_INCLUDE_SUBDOMAINS: True
- SECURE_HSTS_PRELOAD: True
- SESSION_COOKIE_SECURE: True
- CSRF_COOKIE_SECURE: True
- X_FRAME_OPTIONS: DENY
- SECURE_CONTENT_TYPE_NOSNIFF: True
- SECURE_BROWSER_XSS_FILTER: True

## Deployment:
- HTTPS enforced via SSL/TLS
- Nginx configured to redirect all HTTP requests to HTTPS

## Security Review:
- All traffic is encrypted
- Cookies are secure
- Clickjacking and XSS protections enabled
- HSTS applied for one year
