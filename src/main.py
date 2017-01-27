#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
from flask import Flask, request

PORT = int(os.environ.get('PORT', '5000'))
GITHUB_KEY = os.environ.get('GITHUB_SECRET')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def activate_bot():
    main(request.get_json())
    return '', 200


def main(received_json):
    print(received_json)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(PORT))
