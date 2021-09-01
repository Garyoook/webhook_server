from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import os

import requests


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path),
                     str(self.headers))
        self._set_response()
        self.wfile.write(
            "GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(
            self.headers['Content-Length'])
        post_data = self.rfile.read(
            content_length)

        data = eval(post_data.decode('utf-8'))

        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers),
                     post_data.decode('utf-8'))

        try:
            subject = data['Subject']
        except KeyError:
            subject = ''
        try:
            message = data['Message']
        except KeyError:
            message = ''
        try:
            timestamp = data['Timestamp']
        except KeyError:
            timestamp = ''
        try:
            unsubscrive_url = data['UnsubscribeURL']
        except KeyError:
            unsubscrive_url = ''

        msg = f"""
            Subject: {subject}
            
            Message: {message}
            
            Time: {timestamp}
            
            If you want to unsubscribe, click {unsubscrive_url}
        """

        if self.path == '/api/webhook/dingtalk/':
            webhook_addr = os.environ.get('DINGTALK_WEBHOOK_URL')
            msg = "[MINIEYE] " + msg
            send_message_dingtalk(msg, webhook_addr)

        self._set_response()
        self.wfile.write(
            "POST request for {}".format(self.path).encode('utf-8'))


def send_message_dingtalk(message, webhook_addr):
    # content of data need to be modified based on different webhooks.
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_addr, json.dumps(data), headers=headers)
    print(response)


def run(server_class=HTTPServer, handler_class=S,
        port=int(os.environ.get('WEBHOOK_LISTEN_PORT'))):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting the webhook message server at port {}...\n'.format(
        os.environ.get('WEBHOOK_LISTEN_PORT')))
    print(httpd)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping server...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
