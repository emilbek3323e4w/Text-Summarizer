"""
Extractive Summarization Module
Author: Emilbek
Last Modified by: Emilbek
Date Last Modified: 04.03.2025
Description: Implements extractive summarization using TextRank algorithm
Revision History: Initial version 1.0
"""

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
import networkx as nx

class ExtractiveSummarizer:
    """
    Implements extractive summarization using TextRank algorithm
    """
    
    def __init__(self):
        """Initialize the summarizer with required NLTK resources"""
        # Download necessary NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        self.stop_words = set(stopwords.words('english'))
        
    def summarize(self, text, ratio=0.3):
        """
        Generate extractive summary using TextRank algorithm
        
        Args:
            text (str): Input text to summarize
            ratio (float): Proportion of sentences to keep (0.0-1.0)
            
        Returns:
            str: Extractive summary
        """
        # Split text into sentences
        sentences = sent_tokenize(text)
        
        # Calculate number of sentences for summary
        num_sentences = max(1, int(len(sentences) * ratio))
        
        # If few sentences, return original text
        if len(sentences) <= num_sentences:
            return text
            
        # Create similarity matrix
        similarity_matrix = self._build_similarity_matrix(sentences)
        
        # Apply PageRank algorithm
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph)
        
        # Select top N sentences
        ranked_sentences = sorted([(scores[i], i, s) for i, s in enumerate(sentences)], 
                                 reverse=True)
        top_sentence_indices = [ranked_sentences[i][1] for i in range(num_sentences)]
        
        # Preserve original order
        top_sentence_indices.sort()
        
        # Construct summary
        summary = ' '.join([sentences[i] for i in top_sentence_indices])
        return summary
        
    def _build_similarity_matrix(self, sentences):
        """
        Build sentence similarity matrix
        
        Args:
            sentences (list): List of sentences
            
        Returns:
            numpy.ndarray: Similarity matrix
        """
        # Create empty similarity matrix
        n = len(sentences)
        similarity_matrix = np.zeros((n, n))
        
        # Calculate similarity for each sentence pair
        for i in range(n):
            for j in range(n):
                if i != j:  # Skip self-comparison
                    similarity_matrix[i][j] = self._sentence_similarity(
                        sentences[i], sentences[j])
                    
        # Normalize matrix
        for i in range(n):
            if np.sum(similarity_matrix[i]) != 0:
                similarity_matrix[i] = similarity_matrix[i] / np.sum(similarity_matrix[i])
                
        return similarity_matrix
        
    def _sentence_similarity(self, sent1, sent2):
        """
        Calculate cosine similarity between two sentences
        
        Args:
            sent1 (str): First sentence
            sent2 (str): Second sentence
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Tokenize and filter words
        words1 = [word.lower() for word in word_tokenize(sent1) 
                 if word.isalnum() and word.lower() not in self.stop_words]
        words2 = [word.lower() for word in word_tokenize(sent2) 
                 if word.isalnum() and word.lower() not in self.stop_words]
        
        # Find all unique words
        all_words = list(set(words1 + words2))
        
        # Skip if no meaningful words
        if not all_words:
            return 0
        
        # Create word frequency vectors
        vector1 = [1 if word in words1 else 0 for word in all_words]
        vector2 = [1 if word in words2 else 0 for word in all_words]
        
        # Calculate cosine similarity
        dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))
        magnitude1 = sum(v1 * v1 for v1 in vector1) ** 0.5
        magnitude2 = sum(v2 * v2 for v2 in vector2) ** 0.5
        
        if magnitude1 * magnitude2 == 0:
            return 0
            
        return dot_product / (magnitude1 * magnitude2)
        
    def keyword_extraction(self, text, num_keywords=10):
        """
        Extract important keywords from text
        
        Args:
            text (str): Input text
            num_keywords (int): Number of keywords to extract
            
        Returns:
            list: List of important keywords
        """
        # Tokenize and filter words
        words = [word.lower() for word in word_tokenize(text) 
                if word.isalnum() and word.lower() not in self.stop_words]
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
                
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Return top N keywords
        return [word for word, freq in sorted_words[:num_keywords]]