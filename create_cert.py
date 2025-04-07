from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import os

# Generate our key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Write the key to disk for safe keeping
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Various details about who we are
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
])

# Certificate is valid for 1 year
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.utcnow()
).not_valid_after(
    datetime.utcnow() + timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
    critical=False,
).sign(key, hashes.SHA256())

# Write the certificate out to disk
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

# Now create a combined PEM file (server.pem) with both key and certificate
with open("server.pem", "wb") as outfile:
    with open("key.pem", "rb") as keyfile:
        outfile.write(keyfile.read())
    with open("cert.pem", "rb") as certfile:
        outfile.write(certfile.read())

print("Certificate files created successfully:")
print(f"  - Private key: {os.path.abspath('key.pem')}")
print(f"  - Certificate: {os.path.abspath('cert.pem')}")
print(f"  - Combined file: {os.path.abspath('server.pem')}")