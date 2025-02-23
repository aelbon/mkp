from urllib.parse import urlparse, urlunparse
from allauth.account.adapter import DefaultAccountAdapter

class ShopAccountAdapter(DefaultAccountAdapter):
    def _clean_host(self, host: str) -> str:
        """
        Cleans the host string to extract just the hostname, removing any ports.
        """
        return host.split(':')[0]

    def build_absolute_uri(self, request, url: str) -> str:
        """
        Builds absolute URI working both with and without Nginx proxy.
        Falls back to standard request attributes if proxy headers aren't present.
        """
        parsed_url = urlparse(url)
        
        # Get the hostname without any ports
        hostname = self._clean_host(request.get_host())
        
        # Get port - try forwarded port first, then fallback to request.get_port()
        port = request.META.get('HTTP_X_FORWARDED_PORT') or request.get_port()
        
        # Get scheme - try forwarded proto first, then fallback to request.scheme
        scheme = request.META.get('HTTP_X_FORWARDED_PROTO', request.scheme)
        
        # Build netloc with port if needed
        new_netloc = hostname
        if port and port not in ('80', '443'):
            new_netloc = f"{hostname}:{port}"
            
        return urlunparse((
            scheme,
            new_netloc,
            parsed_url.path,
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment
        ))