class CSPMiddleware:
    """
    Minimal CSP middleware to set Content-Security-Policy header.
    Adjust directives as needed for external resources.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.csp = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault('Content-Security-Policy', self.csp)
        return response
