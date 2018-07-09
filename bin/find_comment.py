#!/usr/bin/python3 

import os
import re
import datetime
import argparse
import json
import glob
import prawcore
import lib.login


def parse_args():
    parser = argparse.ArgumentParser(description="Help Text")
    parser.add_argument('-u', '--user', required=True, help='Author of comment')
    parser.add_argument('-p', '--pattern', action='append', required=True, help='Pattern to look for')
    parser.add_argument('-s', '--subreddit', action='append', default=[], help='Pattern to look for')
    args = parser.parse_args()
    lowercase_subreddit = []
    for s in args.subreddit:
        lowercase_subreddit.append(s.lower())
    args.subreddit = lowercase_subreddit
        
    return args
    

def found_comment(comment_fn):
    print('*************************************************************')
    with open(comment_fn, 'r') as f:
        comment = json.loads(f.read())
        print(comment[u'body'])
        print('\n\nURL: https://reddit.com/{0}'.format(comment[u'permalink']))
        print('In {0}: {1}'.format(comment[u'subreddit_name_prefixed'].encode('ascii', 'ignore'), comment[u'link_title'].encode('ascii', 'ignore')))
        print('Ups: {0}, Downs: {1}, Total: {2}'.format(comment[u'ups'],comment[u'downs'],comment[u'score']))
        print(os.path.join(os.getcwd(), comment_fn))
    

def find_comments(username, patterns_re, arg_subreddit):
    patterns_rec = []
    for pattern_re in patterns_re:
        patterns_rec.append(re.compile('.*{0}'.format(pattern_re), re.MULTILINE | re.IGNORECASE))
    my_reddit = lib.login.Reddit()
    path = os.path.join(my_reddit.comment_cache, username)
    os.chdir(path)
    
    for folder in sorted(os.listdir(path)):
        fn = os.path.join(folder, 'comment.json')
        with open(fn, 'r') as commentf:
            comment = json.loads(commentf.read())
            subreddit = comment[u'subreddit_name_prefixed'][2:].lower()
            if arg_subreddit and subreddit.lower() not in arg_subreddit:
                continue
            
            found = True
            for pattern_rec in patterns_rec:
                if not found:
                    break
                found = False
                for line in comment[u'body'].splitlines():
                    m = pattern_rec.match(line)
                    if m:
                        found = True
                        break
            if found:
                found_comment(fn)

def main():
    args = parse_args()
    print(args.pattern)
    print(args.subreddit)
    find_comments(args.user, args.pattern, args.subreddit)
    
    
if __name__ == "__main__":
    main()
