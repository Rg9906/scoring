class ExactMatchEvaluator:
    """
    A class for evaluating exact matches between sentences.
    
    This evaluator checks if two sentences are identical after
    basic normalization and returns a full score if they match.
    """
    
    def __init__(self):
        """
        Initialize the ExactMatchEvaluator.
        """
        pass
    
    def evaluate(self, user_sentence, reference_sentence):
        """
        Evaluate if the user sentence exactly matches the reference sentence.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            tuple: A tuple containing (is_exact_match, score)
                   is_exact_match (bool): True if sentences match exactly
                   score (float): 100.0 if exact match, 0.0 otherwise
        """
        if user_sentence is None or reference_sentence is None:
            return False, 0.0
        
        # Strip leading and trailing whitespace from both sentences
        normalized_user = user_sentence.strip()
        normalized_reference = reference_sentence.strip()
        
        # Check if the normalized sentences are exactly the same
        is_exact_match = normalized_user == normalized_reference
        
        if is_exact_match:
            return True, 100.0
        else:
            return False, 0.0
    
    def get_score(self, user_sentence, reference_sentence):
        """
        Get the exact match score between two sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            float: 100.0 if exact match, 0.0 otherwise
        """
        _, score = self.evaluate(user_sentence, reference_sentence)
        return score