'''Joins Coarse-Discourse annotations with Reddit data via Reddit API.'''
# Copyright 2017 Google Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import praw
import json
import time

'''
Requirements: PRAW python library - https://praw.readthedocs.io/en/latest/index.html
              current version: 4.4.0

Date: 04/02/2017

This script adds fields to the coarse-discourse dataset for each comment including the 
text of the comment and the author. The information is taken from the Reddit API.

You can augment this script to gather other information about the comment such as upvote 
or downvote count or about the comment author, such as their karma, from the fields
that the Reddit API provides.


Note:

There may be discrepancies due to changes made between when the coarse-discourse
data was collected (August 2016) and when you are accessing the API, such as missing 
comments or comment text.

You should be able to overcome discrepancies by downloading the full Reddit dump from 
the beginning up until 09/2016 found in various places such as: 

https://www.reddit.com/r/datasets/comments/3bxlg7/i_have_every_publicly_available_reddit_comment/
https://archive.org/details/2015_reddit_comments_corpus
https://bigquery.cloud.google.com/dataset/fh-bigquery:reddit_posts

and using that data instead of the Reddit API to collect the comment texts and author names.
'''


# Replace below with information provided to you by Reddit when registering your script
reddit = praw.Reddit(client_id='my client id',
                     client_secret='my client secret',
                     user_agent='my user agent')

with open('coarse_discourse_dataset.json') as jsonfile:
    lines = jsonfile.readlines()
    dump_with_reddit = open('coarse_discourse_dump_reddit.json', 'w')
    
    for line in lines:
        reader = json.loads(line)
        print reader['url']
        
        submission = reddit.submission(url=reader['url'])
        
        # Annotators only annotated the 40 "best" comments determined by Reddit
        submission.comment_sort = 'best'
        submission.comment_limit = 40
        
        post_id_dict = {}
        
        for post in reader['posts']:
            post_id_dict[post['id']] = post
        
        full_submission_id = 't3_' + submission.id
        if full_submission_id in post_id_dict:
            post_id_dict[full_submission_id]['body'] = submission.selftext
            
            # For a self-post, this URL will be the same URL as the thread.
            # For a link-post, this URL will be the link that the link-post is linking to.
            post_id_dict[full_submission_id]['url'] = submission.url
            if submission.author:
                post_id_dict[full_submission_id]['author'] = submission.author.name
        
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            full_comment_id = 't1_' + comment.id
            if full_comment_id in post_id_dict:
                post_id_dict[full_comment_id]['body'] = comment.body
                if comment.author:
                    post_id_dict[full_comment_id]['author'] = comment.author.name
        
        found_count = 0
        for post in reader['posts']:
            if not post.has_key('body'):
                print "Can't find %s in URL: %s" % (post['id'], reader['url'])
            else:
                found_count += 1
                
        print 'Found %s posts out of %s' % (found_count, len(reader['posts']))

        dump_with_reddit.write(json.dumps(reader) + '\n')
        
        # To keep within Reddit API limits
        time.sleep(2)
        
