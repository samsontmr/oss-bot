#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
import os
from flask import Flask, request

PORT = int(os.environ.get('PORT', '5000'))
GITHUB_KEY = os.environ.get('GITHUB_SECRET')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/pull_req', methods=['POST'])
def receive_pull_request_event():
    parse_pull_request_json(request.get_json())
    return '', 200


def parse_pull_request_json(received_json):
    title = received_json['pull_request']['title']
    body = received_json['pull_request']['body']
    username = received_json['pull_request']['user']['login']
    logger.info('Received PR "' + title + '" from: ' + username +
                '\n Description: ' + body)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(PORT))
