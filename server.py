import os
import ssl
from http import server
import ssl
import subprocess
import sys


def make_cert():
    subprocess.run(
        'openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost" && type key.pem cert.pem > server.pem',
        shell=True,
        check=True,
    )


def cert_exists():
    return os.path.exists("./server.pem")


while not cert_exists():
    try:
        make_cert()
    except Exception as e:
        print(
            f"[-] Something went wrong making the certificate. Check your openssl install.",
            file=sys.stderr,
        )
        print(f"[-] {e.with_traceback(e.__traceback__)}", file=sys.stderr)
        sys.exit(1)

httpd = server.HTTPServer(("0.0.0.0", 4443), server.SimpleHTTPRequestHandler)

# Create an SSL context and configure it
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="./server.pem")

# Wrap the socket with the context
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
