
TWITTER #TREND RECOMMENDATION USING TOPIC MODELS
================================================

Entities
--------

Tweet obj:
 * user_id
 * text
 * id_str
 * lang
 * coord
 * loc
 * created_at
 * trend_ids[]

User obj:
* id_str
* location
* name
* screen_name
* trend_ids []

Trend Obj:
* trend
* trendid


Roadmap
-------
* Represent a #trend accurately with an [LDA](http://machinelearning.wustl.edu/mlpapers/paper_files/BleiNJ03.pdf) topic model with [Gensim](https://github.com/piskvorky/gensim).

* Gensim still doesn't implement a purely online version of LDA, or of a Dynamic Topic Model which are the perfect model to represent a corpus which is temporally evolving in topics - thus suiting a twitter trending topic closely.
 * Neither could I come across a mature and maintained implementation of Dynamic Topic Models in Python at all.
 * Hence, as a prototype the current aim is to model a static corpus accurately and implement a bare-bones recommendation system with it, i.e. give a #trend, it could recommend you other trends on twitter at that given moment which are topically similar to this trend, or in other words, recommend other trends with similar topic distributions to the given trend.

* Ultimately,
 * Automate tweet collection and learning of the topic model online, perhaps this would enforce a migration to C++ or working something out with Gensim in the future
 * Make this recommendation system live! Probably exposed as a webapp.
