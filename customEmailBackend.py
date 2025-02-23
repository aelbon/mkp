
import ssl

from django.core.mail.backends.smtp import EmailBackend
from django.utils.functional import cached_property
from django.conf import settings as django_settings
import os
class CustomEmailBackend(EmailBackend):
    @cached_property
    def ssl_context(self):
        if self.ssl_certfile or self.ssl_keyfile:
            ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
        else:
            ssl_context = ssl.create_default_context()
        ssl_context.verify_flags -= ssl.VERIFY_X509_STRICT
        if hasattr(django_settings, 'EMAIL_CA_PATH') and django_settings.EMAIL_CA_PATH is not None:
            cert_path = os.path.abspath(django_settings.EMAIL_CA_PATH)
            oldSize = len(ssl_context.get_ca_certs())
            for filename in os.listdir(cert_path): 
                ssl_context.load_verify_locations(os.path.join(cert_path,filename),None, None)
            if len(ssl_context.get_ca_certs()) == oldSize:
                raise ValueError(f"Could not load any CA certificates from {cert_path}")
# We want to load the certificate and key files only if they are provided after the CA certificate is loaded because some of the CA certificates may be required to verify the certificate and key files.
        if self.ssl_certfile and self.ssl_keyfile:
            ssl_context.load_cert_chain(self.ssl_certfile, self.ssl_keyfile)
        return ssl_context
      