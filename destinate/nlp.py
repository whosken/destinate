import textblob
import math

def summarize(text, max_sentence_count=20):
    '''Extract the sentences with the highest shared information with others'''
    blob = textblob.TextBlob(text)
    
    def score_sentence(sentence):
        return sum(mutual_information(s.words, sentence.words) for s in blob.sentences if s != sentence)
    
    sentence_scores = [(score_sentence(s),s) for s in blob.sentences if len(s.words) > 3]
    return u'\n'.join(unicode(s) for _,s in sorted(sentence_scores, reverse=True)[:max_sentence_count])
    
def translate(text, to=None):
    blob = textblob.TextBlob(text)
    try:
        blob = blob.translate(to=to or'en')
    except (textblob.exceptions.TranslatorError, textblob.exceptions.NotTranslated) as error:
        print error
    return unicode(blob)
    
def mean_shared_words(words_one, words_two):
    shared_words = set(words_one).intersection(words_two)
    similarity = sum(words_one.count(w) + words_two.count(w) for w in shared_words)
    return similarity * 2.0 / (len(words_one) + len(words_two))

def mutual_information(words_one, words_two):
    '''See: https://en.wikipedia.org/wiki/Mutual_information'''
    total_one, total_two = float(len(words_one)), float(len(words_two))
    total_joint = total_one + total_two
    
    def pmi(word):
        count_one = words_one.count(word)
        count_two = words_two.count(word)
        p_joint = (count_one + count_two) / total_joint
        p_one = count_one / total_one
        p_two = count_two / total_two
        return math.log(p_joint / p_one / p_two)
        
    shared_words = set(words_one).intersection(words_two)
    return sum(pmi(w) for w in shared_words)
    