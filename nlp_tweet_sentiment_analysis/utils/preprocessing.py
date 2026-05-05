import re
import nltk

def cleaning(sentence):
    text = sentence.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("omw-1.4")
nltk.download("punkt")
nltk.download("punkt_tab")

lem=WordNetLemmatizer()
stop_words=set(stopwords.words('english'))

def wordnet_pos(tag):
  if tag.startswith("N"):
    return 'n'
  elif tag.startswith("V"):
    return 'v'
  elif tag.startswith("J"):
    return 'a'
  elif tag.startswith("R"):
    return 'r'
  else:
    return 'n'

def preprocessing(sentence):
  words=sentence.split()
  words=[word for word in words if word not in stop_words]
  words_tag=pos_tag(words)
  words=[lem.lemmatize(word,pos=wordnet_pos(tag)) for word,tag in words_tag]
  return " ".join(words)