import base64
import hashlib
import socket
import ssl
from urllib.parse import urlparse

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class SSLPinning:
    def __init__(self, config=None, url=None, proxy=None):
        self.config = config or {}
        self.url = url
        self.proxy = proxy
        self.allow = self.config.get('ssl', True) if isinstance(self.config, dict) else True
        self.get = self._server_pin

    def _server_pin(self, url=None):
        target = url or self.url
        if not target:
            return False
        parsed = urlparse(target if '://' in target else f'https://{target}')
        host = parsed.hostname
        port = parsed.port or 443
        if not host:
            return False
        pem = ssl.get_server_certificate((host, port))
        cert = x509.load_pem_x509_certificate(pem.encode('ascii'), default_backend())
        pubkey = cert.public_key().public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        digest = hashlib.sha256(pubkey).digest()
        return 'sha256/' + base64.b64encode(digest).decode('ascii')

    def check(self, url=None):
        if not self.allow:
            return True
        return bool(self._server_pin(url))
