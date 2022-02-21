from rake_nltk import Rake
import pandas as pd
import numpy as np
import re
import emoji


class KeyPhrases:

  def __init__(self):
    self.rake_nltk_var = Rake()

  def english_preprocessing(self,x):
      try:
        x = emoji.demojize(x)
        x = re.sub(r'http\S+', '', x)
        x = re.sub('@[^\s]+', '', x)
        x= re.sub(r'\b\d+(?:\.\d+)?\s+', '', x)
        x = x.replace('#', '')
        x = x.replace('@', '')
        x = re.sub((r"^[\W]*"), "", x)
        x = re.sub((r"\s[\W]\s"), ", ", x)
        x = re.sub(r"[^A-Z/a-z0-9(),!?\'\`.]", " ", x)
        x = [i for i in x.split() if len(i)<16]
        x = " ".join(x)
        
        return x
      except Exception as e:
        print("Something wrong in the English preprocessing",e)

  def keyword_extraction(self,text):
    try:
      text = self.english_preprocessing(text)
      self.rake_nltk_var.extract_keywords_from_text(text)
      k_extracted = self.rake_nltk_var.get_ranked_phrases()[:8]
      return k_extracted
    except Exception as e:
      print("There's someting wrong in the keyword extraction function",e)
