## Coarse Discourse

A large corpus of discourse annotations and relations on ~10K forum threads.

Please refer to our paper for an indepth analysis and explanation of the data: [*Characterizing Online Discussion Using Coarse Discourse Sequences (ICWSM '17)*](https://research.google.com/pubs/pub46055.html). Also make sure to check out the companion python script for retrieving the full texts of the threads.


## Explanation of fields

### Thread fields
 * URL - reddit URL of the thread
* title - title of the thread, as written by the first poster
* is_self_post - True if the first post in the thread is a self-post (text addressed to the reddit community as opposed to an external link)
* subreddit - the subreddit of the thread
* posts - a list of all posts in the thread
 
### Post fields
* id - post ID, reddit ID of the current post
* in_reply_to - parent ID, reddit ID of the parent post, or the post that the current post is in reply to
* post_depth - the number of replies the current post is from the initial post
* is_first_post - True if the current post is the initial post
* annotations - a list of all annotations made to this post (see below)
* majority_type - the majority annotated type, if there is a majority type between the annotators, when considering only the main_type field
* majority_link - the majority annotated link, if there is a majority link between the annotators
 
### Annotation fields
* annotator - an unique ID for the annotator
* main_type - the main discourse act that describes this post
* secondary_type - if a post contains more than one discourse act in sequence, this is the second discourse act in the post
* link_to_post - the post that this post is linked to
 
## Data sampling and pre-processing

### Selecting Reddit threads
			
We randomly sampled from the full Reddit dataset starting from its inception to the end of May 2016, which is made available publicly as a dump on [Google BigQuery](https://bigquery.cloud.google.com/table/fh-bigquery:reddit_comments.2016_05). We chose to sample from the entire dataset as opposed to a set of subreddits to ensure a wide variety of communities within our dataset. The full dataset of Reddit from this time period contains 238 million threads. However, we performed several filters on the data before sampling as we were interested in collecting substantial back-and-forth discussion.
					
**Minimum Replies**: As our goal is to better understand discussion, we chose to only take threads that had at least two reply comments to the initial post, according to the _num_comments_ field in Google BigQuery, so that there was some amount of back-and-forth. Disqualifying these threads decreased the dataset to 87.5 million threads. We took a random sample of 50,000 threads from this dataset, and on this smaller set, we performed the following additional filters.
					
**Deleted Comments**: We disqualified any threads that contained a deleted comment or deleted portions of the initial post, as it would be difficult to interpret replies to deleted comments.
					
**Non-English**: As our annotators were English-speaking, we ignored any threads coming from subreddits primarily in a different language. We manually went through the most frequent several hundred subreddits in our dataset and added them to a blacklist if their homepage was primarily in a different language. Annotators were also instructed to skip any threads that were in a different language. The non-English blacklist is provided in this repository.
					
**NSFW**: In order to not subject our annotators to pornography, we additionally blacklisted 693 subreddits labeled Not Safe For Work (NSFW) during summer of 2016 by a third-party [subreddit categorization site](http://redditlist.com/nsfw) that is community-sourced. This does not include subreddits that discuss potentially illegal or explicit content, which are still included in our dataset.
					
**Trading**: We also wished to avoid subreddits that were primarily for trading or coordination, mostly in the context of gaming, because these subreddits have little to no actual discussion. We developed manual rules, such as if the subreddit name ends with the word “swap” or “trade”, as well as manually curated a short blacklist. The trading blacklist is provided in this repository.
					
After conducting filtering, we had 32,728 threads or 65% of our random sample. We chose to sample _link-post_ threads, or threads where the body of the post is a link to a picture, video, or webpage, at 10% of our sample, leaving 90% of our sample to be _self-post_ threads, or threads where the body of the post is a piece of text written to the community. This was so that we could collect a higher proportion of Q&A-related threads, since this data is particularly valuable in a search and information retrieval context.
					
In our filtered dataset, we had 10,145 self-post threads (31%) and 22,583 link-post threads (69%). From our filtered dataset, we sampled 9,000 self-post threads and 1,000 link-post threads. The field is_self_post in the data is set to True if the thread is a self-post. During the annotation process, some threads were discarded due to bugs that occurred so that in the end, 9,701 threads were fully annotated. After collecting annotations, in the data cleaning process, we additionally remove 107 threads with missing posts, 111 duplicate threads, and 10 threads containing only 1 reply. This leaves us with 9,473 threads comprised of 116,347 comments made available here.
			
 
### Annotation
		 	 	 		
Three annotators were assigned to each thread and were instructed to annotate each comment in the thread with its discourse act (main_type) as well as the relation of each comment to a prior comment (link_to_post), if it existed.
					
As comments sometimes perform multiple functions, we instructed crowd annotators to consider the content at the comment level as opposed to sentence or paragraph level to make the task simpler. We did allow annotators to add a second discourse category (secondary_type) to a comment when it was doing two separate actions in series, such as answering a question and then asking a new question. 
				
Finally, some threads on Reddit have hundreds of comments or more. As this is too much work for an annotator to perform in one sitting, we limited the thread length to 40 replies. This was done using Reddit’s default “best” sorting by appending ?limit=40 to every URL in our dataset. These threads represented less than 1% of our dataset. 
 
More details on the overall process can be found in our paper.


## How to retrieve original thread content

The data we are publishing do not contain the full content of the threads. It only includes a small number of metadata fields needed to identify the threads and to understand their structure. In order to help our readers retrieve the full texts and the rest of the meta-data, we are providing a python script that will pull the data from the public Reddit API and join it with our annotations data. The script is available in the join_forum_data sub-directory in this repository.


## Authors
**Amy X. Zhang**, MIT CSAIL, Cambridge, MA, USA. axz@mit.edu

**Ka Wong**, Google, Mountain View, CA, USA. kawong@google.com
 
**Bryan Culbertson**, Calthorpe Analytics, Berkeley, CA, USA. bryan.culbertson@gmail.com
 
**Praveen Paritosh**, Google, Mountain View, CA, USA. pkp@google.com
 
## Citation Guidelines

If you are using this data towards a research publication, please cite the following paper.
 
Amy X. Zhang, Bryan Culbertson, Praveen Paritosh. *Characterizing Online Discussion Using Coarse Discourse Sequences. In Proceedings of the International AAAI Conference on Weblogs and Social Media (ICWSM '17)*. Montreal, Canada. 2017. 
 
Bibtex:
@inproceedings{coarsediscourse,
  title={Characterizing Online Discussion Using Coarse Discourse Sequences},
  author={Zhang, Amy X. and Culbertson, Bryan and Paritosh, Praveen},
  booktitle={Proceedings of the 11th International AAAI Conference on Weblogs and Social Media},
  series={ICWSM '17},
  year={2017},
  location = {Montreal, Canada}
}
 
 
## Files in the directory:
 * *Characterizing Online Discussion Using Coarse Discourse Sequences (ICWSM '17)*
 * Coarse-discourse dataset
 * Rating guidelines
 * A python script to join Coarse-discourse data with Reddit data
 * No-en blacklist
 * Trade blacklist

## License
CC-by
 

