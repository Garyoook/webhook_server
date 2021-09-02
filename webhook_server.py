from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import os

import requests

getEnv = os.environ.get


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

        ignored_keys = ['UnsubscribeURL',
                        'Signature',
                        'SigningCertURL',
                        'SignatureVersion']

        for k in ignored_keys:
            data.pop(k, None)
            data.pop(k.lower(), None)

        msg = '\r\n'.join(["【MINIEYE-WebHook】", json.dumps(data, indent=2)])

        if self.path.startswith('/api/webhook/dingtalk/?access_token='):
            webhook_prefix = 'https://oapi.dingtalk.com/robot/send?access_token='
            access_token = self.path.split('access_token=')[1]
            if access_token != '':
                addr = f"{webhook_prefix}{access_token}"
                send_message_dingtalk_feishu(msg, addr)
            else:
                logging.error('No access token is given. \n')

        # 重复代码， 可用dict优化， 为可读性在增加更多api前暂保持现状。
        if self.path.startswith('/api/webhook/feishu/?access_token='):
            webhook_prefix = 'https://open.feishu.cn/open-apis/bot/v2/hook/'
            access_token = self.path.split('access_token=')[1]
            if access_token != '':
                addr = f"{webhook_prefix}{access_token}"
                send_message_dingtalk_feishu(msg, addr)
            else:
                logging.error('No access token is given. \n')

        self._set_response()
        self.wfile.write(
            "POST request for {}".format(self.path).encode('utf-8'))


def send_message_dingtalk_feishu(message, webhook_addr):
    # content of data need to be modified based on different webhooks.
    # 飞书群组机器人webhook文档：https://www.feishu.cn/hc/zh-CN/articles/360024984973
    # 钉钉群组机器人webhook文档：https://developers.dingtalk.com/document/robots/message-types-and-data-format
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
        port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(
        'Starting the webhook message server at port {}...\n'.format(port))
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
