"""Send push notifications to APNS
This module is used as a proxy server
"""
import socket
import ssl
import json
import struct
import binascii

from flask import Flask
from flask import Response

app = Flask(__name__)


@app.route("/send/<device_token>", methods=['GET'])
def get_results(device_token):
    """
    Send a push notification to APN
    (Apple Push Notification service)
    """

    pay_load = {}

    cert = 'certificate.pem'

    host = ('gateway.push.apple.com', 2195)

    pay_load = json.dumps(pay_load, separators=(',', ':'))

    device_token = binascii.unhexlify(device_token)
    fmt = "!BH32sH{}s".format(len(pay_load))

    msg = struct.pack(
        fmt,
        0,
        32,
        device_token,
        len(pay_load),
        bytes(pay_load, "utf-8")
    )

    ssl_sock = ssl.wrap_socket(
        socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ),
        certfile=cert,
    )
    ssl_sock.connect(host)

    ssl_sock.write(msg)
    ssl_sock.close()

    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
