import pickle
import re

from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


class Model:
    
    def __init__(self):
        with open('models/title_clf.pickle', 'rb') as f:
            self.title_clf = pickle.load(f)
        with open('models/text_clf.pickle', 'rb') as f:
            self.text_clf = pickle.load(f)
            
    def predict(self, data):
        text_cleaned = self.clean(data['text'])

        predict_text = self.text_clf.predict([text_cleaned])[0]
        
        return predict_text
    
    def clean(self, tex): 
        tex = tex.lower()
        #clear at all

        # Urls
        tex = re.sub(r"https?:\/\/t.co\/[A-Za-z0-9]+", "", tex)
        tex = re.sub(r"http?:\/\/t.co\/[A-Za-z0-9]+", "", tex)

        # Words with punctuations and special characters
        punctuations = '@#!?+&*[]-%.—:,/();$=><|{}^' + '\"\'\’\‘\“\”'
        for p in punctuations:
            tex = tex.replace(p, ' ')

        # ... and ..
        tex = tex.replace('...', ' ... ')
        if '...' not in tex:
            tex = tex.replace('..', ' ... ')      

        tex = re.sub('','',tex)
        tex = re.sub(' didn ’ t ',' did not ',tex)
        tex = re.sub(' don t ',' do not ',tex)
        tex = re.sub('&',' and ',tex)

        tex = re.sub(' $ ',' dollar ',tex)
        tex = re.sub(' fbi ', ' federal bureau of investigation ', tex)
        tex = re.sub('w /','',tex)
        tex = re.sub('\"\'\’\‘\‘', '\'', tex)
        tex = re.sub(' u . s . ',' united states ',tex)
        tex = re.sub(' u s ',' united states ',tex)
        tex = re.sub(' m . i . t . ',' massachusetts institute of technology ',tex)
        tex = re.sub(' mit ',' massachusetts institute of technology ',tex)
        tex = re.sub(' n . y . u ',' new york university ',tex)
        tex = re.sub(' nyu ',' new york university ',tex)
        tex = re.sub(' eu ',' european union ',tex)
        tex = re.sub(' e . u . ',' european union ',tex)
        tex = re.sub('>','',tex)
        tex = re.sub('<','',tex)
        tex = re.sub('%',' percent ',tex)
        tex = re.sub(' nyc ',' new york city ',tex)
        tex = re.sub(' s ',' ',tex)

        tex = re.sub(' january ',' MONTH ',tex)
        tex = re.sub(' february ',' MONTH ',tex)
        tex = re.sub(' march ',' MONTH ',tex)
        tex = re.sub(' april ',' MONTH ',tex)
        tex = re.sub(' may ',' MONTH ',tex)
        tex = re.sub(' june ',' MONTH ',tex)
        tex = re.sub(' july ',' MONTH ',tex)
        tex = re.sub(' august ',' MONTH ',tex)
        tex = re.sub(' september ',' MONTH ',tex)
        tex = re.sub(' october ',' MONTH ',tex)
        tex = re.sub(' november ',' MONTH ',tex)
        tex = re.sub(' december ',' MONTH ',tex)

        tex = re.sub(' the ',' ',tex)
        tex = re.sub(' a ',' ',tex)
        tex = re.sub(' t ',' ',tex)
        tex = re.sub(' to ',' ',tex)
        tex = re.sub(' of ',' ',tex)
        tex = re.sub(' be ',' ',tex)
        tex = re.sub(' in ',' ',tex)

        tex = re.sub('  ',' ',tex)
        tex = re.sub('  ',' ',tex)
        tex = re.sub('  ',' ',tex)

        l = []
        for i in tex.split():
            if i.isdigit():
                l.append('NUM')
            else:
                l.append(i)

        tex = ' '.join(l)

        tex = re.sub(' MONTH NUM NUM ',' DATE ',tex)
        tex = re.sub(' NUM NUM NUM ',' DATE ',tex)

        return tex
