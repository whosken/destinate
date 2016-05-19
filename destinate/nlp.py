import textblob
import math

def summarize(text, max_sentence_count=20):
    blob = textblob.TextBlob(text)
    
    def score_sentence(sentence):
        return sum(normalized_doc_diff(s.words, sentence.words) for s in blob.sentences if s != sentence)
    
    sentence_scores = [(score_sentence(s),s) for s in blob.sentences if len(s.words) > 3]
    return u'\n'.join(unicode(s) for _,s in sorted(sentence_scores, reverse=True)[:max_sentence_count])
    
def normalized_doc_diff(words_one, words_two):
    shared_words = set(words_one).intersection(words_two)
    similarity = sum(words_one.count(w) + words_two.count(w) for w in shared_words)
    return similarity * 2.0 / (len(words_one) + len(words_two))
