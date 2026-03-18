class RedundancyCheckerEvaluator:
    """
    A class for evaluating redundancy in sentences.
    
    This evaluator detects unnatural repetition by analyzing the
    ratio of unique words to total words in a sentence.
    """
    
    def __init__(self):
        """
        Initialize the RedundancyCheckerEvaluator.
        """
        pass
    
    def evaluate(self, sentence):
        """
        Evaluate the redundancy level of a sentence.
        
        Args:
            sentence (str): The sentence to evaluate
            
        Returns:
            float: Redundancy penalty score between 0 and 1
                   (0 = no redundancy, 1 = maximum redundancy)
        """
        if sentence is None or sentence.strip() == "":
            return 0.0
        
        # Split sentence into words
        words = sentence.split()
        
        if len(words) == 0:
            return 0.0
        
        # Count total and unique words
        total_words = len(words)
        unique_words = len(set(words))
        
        # Calculate repetition ratio: (total - unique) / total
        # This gives us a measure of redundancy
        repetition_ratio = (total_words - unique_words) / total_words
        
        return repetition_ratio
    
    def get_score(self, sentence):
        """
        Get the redundancy penalty score for a sentence.
        
        Args:
            sentence (str): The sentence to evaluate
            
        Returns:
            float: Redundancy penalty score between 0 and 1
        """
        return self.evaluate(sentence)
    
    def get_word_statistics(self, sentence):
        """
        Get detailed word statistics for a sentence.
        
        Args:
            sentence (str): The sentence to analyze
            
        Returns:
            dict: Dictionary containing word statistics
        """
        if sentence is None or sentence.strip() == "":
            return {
                'total_words': 0,
                'unique_words': 0,
                'repetition_ratio': 0.0,
                'word_frequencies': {}
            }
        
        words = sentence.split()
        total_words = len(words)
        unique_words = len(set(words))
        repetition_ratio = (total_words - unique_words) / total_words if total_words > 0 else 0.0
        
        # Calculate word frequencies
        word_frequencies = {}
        for word in words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1
        
        return {
            'total_words': total_words,
            'unique_words': unique_words,
            'repetition_ratio': repetition_ratio,
            'word_frequencies': word_frequencies
        }
    
    def get_repeated_words(self, sentence):
        """
        Get a list of words that are repeated in the sentence.
        
        Args:
            sentence (str): The sentence to analyze
            
        Returns:
            list: List of words that appear more than once
        """
        if sentence is None or sentence.strip() == "":
            return []
        
        words = sentence.split()
        word_counts = {}
        repeated_words = []
        
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        for word, count in word_counts.items():
            if count > 1:
                repeated_words.append(word)
        
        return repeated_words