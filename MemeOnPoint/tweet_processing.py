# Import spacy and English models
import spacy
nlp = spacy.load('en_core_web_sm')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS


tweet_text = '@MemeOnPoint I have to do everything #work I am upset @usuario10203049 Fuck you'

def get_tokens(tweet_nlp):
  tokens = []
  for w in tweet_nlp:
    if not w.is_stop and not w.is_punct:
      tokens.append(w.lemma_)
  return tokens

def get_key_words(tweet_text):
  words = tweet_text.split(" ")
  new_words = []
  #Take out @
  for w in words:
    if len(w)>1 and w[0]!="@":
      new_words.append(w)
      
    
  words = ' '.join(list(new_words))
  tweet_nlp = nlp(words)
  tokens = get_tokens(tweet_nlp)
      
  return(tokens)
  

