"""
Text Analysis Module (Simplified)
Author: Emilbek
Last Modified by: Emilbek
Date Last Modified: 04..03.2025
Description: Analyzes text statistics using only NLTK
Revision History: Initial version 1.0
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

class TextAnalyzer:
    """Analyzes text to provide statistics"""
    
    def __init__(self):
        """Initialize text analyzer and download required NLTK data"""
        nltk.download('punkt', quiet=True)
        
    def analyze_text(self, text):
        """
        Perform simple text analysis
        
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
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': avg_sentence_length,
            'estimated_reading_time': reading_time,
            'readability': readability
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