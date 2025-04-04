"""
Text Analysis Module (Simplified)
Author: Emilbek
Last Modified by: Emilbek
Date Last Modified: 04..03.2025
Description: Analyzes text statistics using only NLTK
Revision History: 
    - Initial version 1.0
    - Modified by Qihang, 2025-04-04:
        * Added sentiment analysis using TextBlob
        * Integrated sentiment into analyze_text()
        * Expanded return value to include sentiment label, polarity, subjectivity
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob  

class TextAnalyzer:
    """Analyzes text to provide statistics and sentiment analysis"""

    def __init__(self):
        """Initialize text analyzer and download required NLTK data"""
        nltk.download('punkt', quiet=True)

    def analyze_text(self, text):
        """
        Perform simple text analysis along with sentiment analysis
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Dictionary with text analysis results
        """
        word_count = self._count_words(text)
        sentence_count = self._count_sentences(text)
        avg_sentence_length = word_count / max(1, sentence_count)
        reading_time = self._estimate_reading_time(word_count)

        readability = {
            'flesch_reading_ease': self._simple_readability_score(text),
            'grade_level': 'College level'
        }

        # Add sentiment analysis
        sentiment = self.analyze_sentiment(text)

        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': avg_sentence_length,
            'estimated_reading_time': reading_time,
            'readability': readability,
            'sentiment': sentiment  # Include sentiment analysis result
        }

    def _count_words(self, text):
        """Count the number of words in text"""
        words = word_tokenize(text)
        # Filter out punctuation
        words = [word for word in words if any(c.isalpha() for c in word)]
        return len(words)

    def _count_sentences(self, text):
        """Count the number of sentences in text"""
        sentences = sent_tokenize(text)
        return len(sentences)

    def _estimate_reading_time(self, word_count, wpm=250):
        """
        Estimate reading time in minutes
        
        Args:
            word_count (int): Number of words in text
            wpm (int): Words per minute reading speed (default 250)
            
        Returns:
            float: Estimated reading time in minutes
        """
        return word_count / wpm

    def _simple_readability_score(self, text):
        """
        Calculate a simple readability score
        
        Args:
            text (str): Text to analyze
            
        Returns:
            float: Simple readability score (0-100)
        """
        sentences = sent_tokenize(text)
        words = word_tokenize(text)

        # Filter out punctuation
        words = [word for word in words if any(c.isalpha() for c in word)]

        if not words or not sentences:
            return 0

        # Simple approximation: longer sentences and words = lower score
        avg_words_per_sentence = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)

        # Simple formula (not scientific): higher score = easier to read
        score = 100 - (avg_words_per_sentence * 0.5) - (avg_word_length * 5)

        # Ensure score is within bounds
        return max(0, min(100, score))

    def analyze_sentiment(self, text):
        """
        Perform sentiment analysis on the given text using TextBlob
        
        Args:
            text (str): Input text for sentiment analysis
        
        Returns:
            dict: Sentiment analysis result with polarity and subjectivity
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # [-1.0, 1.0]
        subjectivity = blob.sentiment.subjectivity  # [0.0, 1.0]

        # Simple sentiment categorization based on polarity
        if polarity > 0.2:
            label = "Positive"
        elif polarity < -0.2:
            label = "Negative"
        else:
            label = "Neutral"

        return {
            'label': label,
            'polarity': polarity,
            'subjectivity': subjectivity
        }
