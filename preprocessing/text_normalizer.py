class TextNormalizer:
    """
    A class for normalizing text data.
    
    This class provides methods to convert text to lowercase,
    strip whitespace, and expand basic contractions.
    """
    
    def __init__(self):
        """
        Initialize the TextNormalizer with a dictionary of common contractions.
        """
        self.contractions = {
            "I'm": "I am",
            "don't": "do not",
            "can't": "cannot",
            "won't": "will not",
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "haven't": "have not",
            "hasn't": "has not",
            "hadn't": "had not",
            "didn't": "did not",
            "doesn't": "does not",
            "couldn't": "could not",
            "shouldn't": "should not",
            "wouldn't": "would not",
            "mustn't": "must not",
            "mightn't": "might not",
            "needn't": "need not",
            "let's": "let us",
            "there's": "there is",
            "here's": "here is",
            "what's": "what is",
            "that's": "that is",
            "who's": "who is",
            "where's": "where is",
            "when's": "when is",
            "why's": "why is",
            "how's": "how is"
        }
    
    def normalize_text(self, text):
        """
        Normalize the input text by applying all normalization steps.
        
        Args:
            text (str): The input text to normalize
            
        Returns:
            str: The normalized text
        """
        if text is None:
            return ""
        
        # Step 1: Convert to lowercase
        normalized_text = text.lower()
        
        # Step 2: Strip leading and trailing whitespace
        normalized_text = normalized_text.strip()
        
        # Step 3: Expand contractions
        normalized_text = self._expand_contractions(normalized_text)
        
        return normalized_text
    
    def _expand_contractions(self, text):
        """
        Expand common contractions in the text.
        
        Args:
            text (str): The input text with contractions
            
        Returns:
            str: The text with expanded contractions
        """
        words = text.split()
        expanded_words = []
        
        for word in words:
            if word in self.contractions:
                expanded_words.append(self.contractions[word])
            else:
                expanded_words.append(word)
        
        return ' '.join(expanded_words)