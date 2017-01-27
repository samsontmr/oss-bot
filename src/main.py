#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
import os
import re
from flask import Flask, request

PORT = int(os.environ.get('PORT', '5000'))
GITHUB_KEY = os.environ.get('GITHUB_SECRET')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/pull_req', methods=['POST'])
def receive_pull_request_event():
    parsed_pr = parse_pull_request_json(request.get_json())
    validate_pull_request(parsed_pr)
    return '', 200


def parse_pull_request_json(received_json):
    title = received_json['pull_request']['title']
    body = received_json['pull_request']['body']
    username = received_json['pull_request']['user']['login']
    logger.info('Received PR "' + title + '" from: ' + username +
                '\n Description: "' + body + '"')
    return {'title' : title, 'body' : body, 'username' : username}


def validate_pull_request(pull_request_info):
    if is_valid_pull_request_body(pull_request_info['body']):
        logger.info('Body: format check passed')

def is_valid_pull_request_body(pull_request_body):
    REGEX_PULL_REQ_BODY = os.environ.get('REGEX_PULL_REQ_BODY')
    return re.match(REGEX_PULL_REQ_BODY, pull_request_body, re.DOTALL)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(PORT))
