#!/usr/bin/python3 

import os
import datetime
import argparse
import json
import prawcore
import lib.login
import logging
logging.basicConfig(level=logging.DEBUG)

def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""
    return ''

def parse_args():
    parser = argparse.ArgumentParser(description="Get comments and cache locally")
    parser.add_argument('-u', '--user', required=True, help='Author of comment')
    args = parser.parse_args()
        
    return args

def get_comments(username, limit=None):
    reddit_login = lib.login.Reddit()
    reddit_login.login()
    reddit = reddit_login.reddit
    try:
        comments = reddit.redditor(username).comments.new(limit = 100)
        print("Comments dict:" + str(comments.__dict__))
        for comment in comments:
            time_stamp = str(datetime.datetime.fromtimestamp(comment.created_utc))
            time_stamp = time_stamp.replace(' ','_').replace(':','-')
            print(time_stamp)
            print(comment.body)
            path = os.path.join(reddit_login.comment_cache, username, time_stamp)
            if os.path.exists(path):
                continue
            os.makedirs(path)
            body_file_name = os.path.join(path, 'body.md')
            with open(body_file_name, 'w', encoding="utf-8") as f:
                f.write(comment.body)
            with open(os.path.join(path, 'perma_link'), 'w') as f:
                f.write(comment.permalink)
            with open(os.path.join(path, 'comment.json'), 'w') as f:
                f.write(json.dumps(comment.__dict__, indent=4, sort_keys=True, default=serialize))
    except prawcore.exceptions.ResponseException as e:
        print(e)

if __name__ == "__main__":
    args = parse_args()
    get_comments(args.user)
