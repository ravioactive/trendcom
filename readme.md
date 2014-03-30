
Twitter #trend Recommendation using Topic Models
================================================

Entities
--------

Tweet obj:
 * user_id: ID of the user who tweeted, as per twitter
 * text: content
 * id_str: ID of this tweet, as per twitter
 * lang: ISO Language Code, only 'en' right now
 * coord: (lat, long) of tweet's location, as per twitter
 * loc: of user, as per twitter
 * created_at: time of creation, as per twitter
 * trend_ids[ ]: a list of unique internal trend IDs being recorded where we saw this tweet
 * retweeted: YES/NO
 * retweet_id: ID of the tweet this tweet is a retweet of

User obj:
* id_str: ID of the user who tweeted, as per twitter
* location: location sepcified by this twitter account
* name: Name of the user on this twitter account
* screen_name: @handle of this twitter account
* trend_ids [ ]: A list of unique internal trend IDs being recorded, this user tweeted about
* tweets[ ]: A list of all tweets we have seen that belong to this user

Trend Obj:
* trend: name of trend
* trendid: unique number, auto-incr


Roadmap
-------
* Represent a #trend accurately with an [LDA](http://machinelearning.wustl.edu/mlpapers/paper_files/BleiNJ03.pdf) topic model with [Gensim](https://github.com/piskvorky/gensim).

* Gensim still doesn't implement a purely online version of LDA, or of a Dynamic Topic Model which are the perfect model to represent a corpus which is temporally evolving in topics - thus suiting a twitter trending topic closely.
 * Neither could I come across a mature and maintained implementation of Dynamic Topic Models in Python at all.
 * Hence, as a prototype the current aim is to model a static corpus accurately and implement a bare-bones recommendation system with it, i.e. give a #trend, it could recommend you other trends on twitter at that given moment which are topically similar to this trend, or in other words, recommend other trends with similar topic distributions to the given trend.

* Ultimately,
 * Automate tweet collection and learning of the topic model online, perhaps this would enforce a migration to C++ or working something out with Gensim in the future
 * Make this recommendation system live! Probably exposed as a webapp.
