#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
import os
import re
from flask import Flask, request
from github import Github

gh = Github(os.environ.get('GITHUB_API_TOKEN'))

PORT = int(os.environ.get('PORT', '5000'))

logging.basicConfig(format=('%(asctime)s - %(name)s' +
                            ' - %(levelname)s - %(message)s'),
                    level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/pull_req', methods=['POST'])
def receive_pull_request_event():
    parsed_pr = parse_pull_request_json(request.get_json())
    if (is_pull_request_to_check(parsed_pr) and
       not is_valid_pull_request(parsed_pr)):
        comment_on_pull_request(parsed_pr['repo'], parsed_pr['pr_id'],
                                'Hi @' + parsed_pr['username'] +
                                ', please follow the naming' +
                                ' conventions for PRs.')
        logger.info('Check Failed!')
    return '', 200


def parse_pull_request_json(received_json):
    repo = received_json['pull_request']['base']['repo']['full_name']
    action = received_json['action']
    pr_id = received_json['pull_request']['number']
    title = received_json['pull_request']['title']
    body = received_json['pull_request']['body']
    username = received_json['pull_request']['user']['login']
    logger.info('Received PR "' + title + '" from: ' + username +
                '\n Description: "' + body + '"')
    return {'repo': repo, 'pr_id': pr_id, 'title': title, 'body': body,
            'username': username, 'action': action}


def is_pull_request_to_check(parsed_pr):
    return (parsed_pr['action'] == 'opened' or parsed_pr['action'] == 'edited'
            or parsed_pr['action'] == 'reopened'
            or parsed_pr['action'] == 'review_requested')


def is_valid_pull_request(parsed_pr):
    return (is_valid_pull_request_title(parsed_pr['title'])
            and is_valid_pull_request_body(parsed_pr['body']))


def is_valid_pull_request_title(pull_request_title):
    REGEX_PULL_REQ_TITLE = os.environ.get('REGEX_PULL_REQ_TITLE')
    return re.match(REGEX_PULL_REQ_TITLE, pull_request_title)


def is_valid_pull_request_body(pull_request_body):
    REGEX_PULL_REQ_BODY = os.environ.get('REGEX_PULL_REQ_BODY')
    return re.match(REGEX_PULL_REQ_BODY, pull_request_body)


def comment_on_pull_request(repo, pr_id, comment):
    logger.info('Commenting on PR ' + str(pr_id))
    gh.get_repo(repo).get_issue(pr_id).create_comment(comment)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(PORT))
