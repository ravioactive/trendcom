from model import mongomodel


class corpus_iter:
    def __init__(self, hashtag, db):
        self.hashtag = hashtag
        self.cursor = mongomodel.getTweetsCursor(hashtag, db)


    def __iter__(self):
        for doc in self.cursor:
            yield doc['tokens']


class corpus_bow_iter:
    def __init__(self, *args):
        if len(args) < 1:
            self.corpusIterator = None
            self.dictionary = None
        elif len(args) == 1:
            if isinstance(args[0], corpus_bow_iter):
                self.corpusIterator = args[0].corpusIterator
                self.corpusIterator.cursor.rewind()
                self.len = self.corpusIterator.cursor.count()
                self.dictionary = args[0].dictionary
            else:
                raise TypeError
        elif len(args) == 2:
            self.corpusIterator = args[0]
            self.corpusIterator.cursor.rewind()
            self.len = self.corpusIterator.cursor.count()
            self.dictionary = args[1]
        elif len(args) >= 3:
            # pymongo.database.Database
            self.corpusIterator = corpus_iter(args[0], args[1])
            self.corpusIterator.cursor.rewind()
            self.len = self.corpusIterator.cursor.count()
            self.dictionary = args[2]

    def __iter__(self):
        for doc in self.corpusIterator.cursor:
            yield self.dictionary.doc2bow(doc['tokens'])

    def __len__(self):
        return self.len
