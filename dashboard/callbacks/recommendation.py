import numpy as np
import pandas as pd
import re
import time
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from datasketch import MinHash, MinHashLSHForest

calculate_duration = lambda x: abs(x[0] - x[1])
print_message = lambda info: '\nIt took %s to %s.'%(info)

def _tokenized(text:str, language:str='en'):

    _stops = get_stop_words(language)
    _tokenizer = RegexpTokenizer(r'\w+')

    tokens = _tokenizer.tokenize(text)
    stopped_tokens = list(filter(lambda t: t not in _stops, tokens))

    return stopped_tokens

def _preprocess(self, text, language:str='en'):
    text = text.lower()
    tokens = _tokenized(text, language)
    return tokens
    
def _create_hashtex(text, perms, language:str='en'):
    shingles = _preprocess(text, language) # shingles are tokenized text
    min_hash = MinHash(num_perm=perms)
    for unigrams in shingles:
        min_hash.update(unigrams.encode('utf8'))
    return min_hash

def get_timing(obj):
    return obj.TIMING

class Forest(object):
    LANGUAGE:str
    DATABASE:object
    START_TIME:float
    END_TIME:float
    TIMING:list

    def __init__(self, database:object, language:str='en'):

        """
            Takes two(2) arguements with one(1) given default values;
            
        Args:
            database: A panda dataframe object.
            permutations: The number of permutations to be performed default is 128.
            language: The language of the text. This is required when creating tokens using the 'stop_word' library, default is english language
        """
        self.LANGUAGE = language
        self.DATABASE = database

    def _get_forest(self, data, perms):

        # START Time
        self.START_TIME = time.time()
        
        minhash_list = []
        
        for text in data['text']:
            min_hashtext = _create_hashtex(text=text, perms=perms, language=self.LANGUAGE)
            minhash_list.append(min_hashtext)
            
        forest = MinHashLSHForest(num_perm=perms)
        
        for item_index, list_item in enumerate(minhash_list):
            forest.add(item_index, list_item)
            
        forest.index()

        # END Time
        self.END_TIME = time.time()
        
        # TIMING LIST
        self.TIMING = [self.END_TIME, self.START_TIME]

        print('It took %s seconds to build forest.' %(calculate_duration(self.TIMING)))
        return forest

    def get_forest(self, permutations:int):
        database = self.DATABASE
        database['text'] = database['title'] + ' ' + database['abstract']
        return self._get_forest(database, permutations)
    

class Rengine(object):
    START_TIME:float
    END_TIME:float
    TIMING:list
    LANGUAGE:str
    DATABASE:object

    def __init__(self, database:object, language:str='en'):
        """
            Takes two(2) arguements with one(1) given default values;

        Attribs:
            LANGUAGE:str; 
            DATABASE:object; a panda dataframe object on which querry is performed.
            
        Args:
            text: The text to be querried for recommendation.
            language: The language of the text. This is required when creating tokens using the 'stop_word' library, default is english language
            database: A panda dataframe object.
            num_recommendation: The number of recommendations to be displayed default is five(5).
        """
        self.LANGUAGE = language
        self.DATABASE = database
        
    # Recommendation function
    def make_query(self, text:str, forest:object, permutations:int, num_recommendations:int=5):
        """
        Recommendation function, takes four(4) arguements with one(1) given default values;
                
        Args:
            text: The text to be querried for recommendation.
            num_recommendation: The number of recommendations to be displayed default is five(5).
            forest: a minhash object.
        """
        # Start timing
        self.START_TIME = time.time()
        
        # creating the MinHash
        min_hash = _create_hashtex(text=text, perms=permutations, language=self.LANGUAGE)
        idx_array = np.array(forest.query(min_hash, num_recommendations))
        if len(idx_array) == 0:
            return None # if your query is empty, return none
            
        result = self.DATABASE.iloc[idx_array]['title']
    
        # END Time
        self.END_TIME = time.time()

        # TIMING LIST
        self.TIMING = [self.END_TIME, self.START_TIME]

        print('It took %s seconds to make recommendation(find similar articles).' %(calculate_duration(self.TIMING)))
    
        return result
