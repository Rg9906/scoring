class ThemeEvaluator:
    """
    A class for evaluating thematic consistency between sentences.
    
    This evaluator provides partial credit for general topic similarity
    based on semantic similarity scores.
    """
    
    def __init__(self):
        """
        Initialize the ThemeEvaluator.
        """
        pass
    
    def evaluate(self, semantic_score):
        """
        Evaluate thematic consistency based on semantic similarity.
        
        Args:
            semantic_score (float): Semantic similarity score between 0 and 1
            
        Returns:
            float: Theme similarity score between 0 and 1
        """
        if semantic_score is None:
            return 0.0
        
        # Validate input
        semantic_score = max(0.0, min(1.0, semantic_score))
        
        # Apply theme evaluation logic
        if semantic_score > 0.6:
            theme_score = semantic_score
        else:
            theme_score = semantic_score * 0.5
        
        return theme_score
    
    def get_score(self, semantic_score):
        """
        Get the theme similarity score based on semantic similarity.
        
        Args:
            semantic_score (float): Semantic similarity score between 0 and 1
            
        Returns:
            float: Theme similarity score between 0 and 1
        """
        return self.evaluate(semantic_score)
    
    def get_theme_level(self, semantic_score):
        """
        Get the thematic consistency level description.
        
        Args:
            semantic_score (float): Semantic similarity score between 0 and 1
            
        Returns:
            str: Description of thematic consistency level
        """
        if semantic_score is None:
            return "Unknown"
        
        theme_score = self.evaluate(semantic_score)
        
        if theme_score >= 0.8:
            return "Strong thematic match"
        elif theme_score >= 0.6:
            return "Good thematic consistency"
        elif theme_score >= 0.4:
            return "Partial thematic similarity"
        elif theme_score >= 0.2:
            return "Weak thematic connection"
        else:
            return "No thematic similarity"
