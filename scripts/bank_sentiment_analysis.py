import pandas as pd
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

class BankSentimentAnalysis:
   def __init__(self, df:pd.DataFrame):
      self.df=df
      self.vader_analyzer = SentimentIntensityAnalyzer()
      # self.bert_analyzer = pipeline("sentiment-analysis",  model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")

   def apply_vader(self):
      def vader_sentiment(text):
          score= self.vader_analyzer.polarity_scores(str(text))['compound']
          if score >=0.05:
             return 'positive'
          elif score <= -0.05:
             return 'negative'
          else: 
             return 'neutral'
          
      self.df['vader_sentiment']= self.df['review'].apply(vader_sentiment)


   def apply_textblob(self):
       def textblob_sentiment(text):
          score =TextBlob(str(text)).sentiment.polarity
          if score > 0.1:
             return 'positive'
          elif score < -0.1:
             return 'negative'
          else: 
             return 'neutral'
          
       self.df['textblob_sentiment'] =self.df['review'].apply(textblob_sentiment)
      
   def apply_bert(self):
       def bert_sentiment(text):
            try:
                result = self.bert_analyzer(str(text)[:512])[0]
                label = result['label'].lower()  # 'positive' or 'negative'
                # Optional neutral approximation
                if result['score'] < 0.6:
                    return 'neutral'
                return label
            except:
                return 'neutral'
       self.df['bert_sentiment'] = self.df['review'].apply(bert_sentiment)

   def save_results(self, output_csv="bank_reviews_with_sentiments.csv"):
        if self.df is not None:
            self.df.to_csv(output_csv, index=False, encoding='utf-8-sig')
            print(f"✅ All sentiment scores saved to {output_csv}")
        else:
            print("❌ No data to save.")

   def apply_preprocess(self):
      def preprocess_text(text):
           # Download NLTK resources
         nltk.download('punkt')
         nltk.download('stopwords')
         nltk.download('wordnet')
         nltk.download('punkt_tab')
         tokens = word_tokenize(text.lower())
         lemmatizer = WordNetLemmatizer()
         stop_words = set(stopwords.words('english'))
         tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
         return ' '.join(tokens)
      
       # Apply preprocessing    
      self.df['processed_review'] = self.df['review'].apply(preprocess_text)      

   def keyword_extraction(self):
       # Vectorize the dataset
      vectorizer = TfidfVectorizer(max_features=100)
      X = vectorizer.fit_transform(self.df['processed_review'])
        # Get top keywords
      keywords = vectorizer.get_feature_names_out()
      print("Top Keywords:", keywords)
   
   def analysis_keyword(self):
    
       # Filter positive and negative reviews
       positive_reviews = self.df[self.df['textblob_sentiment'] == 'positive']['processed_review']
       negative_reviews = self.df[self.df['textblob_sentiment'] == 'negative']['processed_review']

      # Extract keywords from positive reviews
       vectorizer_pos = TfidfVectorizer(max_features=10)
       X_pos = vectorizer_pos.fit_transform(positive_reviews)
       print("Top Keywords in Positive Reviews:", vectorizer_pos.get_feature_names_out())

      # Extract keywords from negative reviews
       vectorizer_neg = TfidfVectorizer(max_features=10)
       X_neg = vectorizer_neg.fit_transform(negative_reviews)
       print("Top Keywords in Negative Reviews:", vectorizer_neg.get_feature_names_out())
 
