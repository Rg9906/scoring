class ScoreAggregator:
    """
    A class for aggregating scores from different evaluators.
    
    This class combines semantic similarity, grammar quality, and redundancy
    scores using weighted scoring to produce a final score.
    """
    
    def __init__(self):
        """
        Initialize the ScoreAggregator with default weights.
        """
        # Define weights for different components
        self.semantic_weight = 0.7
        self.grammar_weight = 0.2
        self.redundancy_weight = 0.1
    
    def aggregate_scores(self, semantic_score, grammar_score, redundancy_score):
        """
        Aggregate individual scores into a final weighted score.
        
        Args:
            semantic_score (float): Semantic similarity score (0 to 1)
            grammar_score (float): Grammar quality score (0 to 1)
            redundancy_score (float): Redundancy penalty score (0 to 1)
            
        Returns:
            float: Final aggregated score between 0 and 100
        """
        # Validate input scores
        semantic_score = max(0.0, min(1.0, semantic_score))
        grammar_score = max(0.0, min(1.0, grammar_score))
        redundancy_score = max(0.0, min(1.0, redundancy_score))
        
        # Apply weighted scoring formula
        # score = (semantic * 0.7) + (grammar * 0.2) - (redundancy * 0.1)
        weighted_score = (
            (semantic_score * self.semantic_weight) +
            (grammar_score * self.grammar_weight) -
            (redundancy_score * self.redundancy_weight)
        )
        
        # Clamp final score between 0 and 1
        weighted_score = max(0.0, min(1.0, weighted_score))
        
        # Convert to 0-100 scale
        final_score = weighted_score * 100
        
        return final_score
    
    def get_final_score(self, semantic_score, grammar_score, redundancy_score):
        """
        Get the final score for the given component scores.
        
        Args:
            semantic_score (float): Semantic similarity score (0 to 1)
            grammar_score (float): Grammar quality score (0 to 1)
            redundancy_score (float): Redundancy penalty score (0 to 1)
            
        Returns:
            float: Final aggregated score between 0 and 100
        """
        return self.aggregate_scores(semantic_score, grammar_score, redundancy_score)
    
    def get_score_breakdown(self, semantic_score, grammar_score, redundancy_score):
        """
        Get a detailed breakdown of how the final score was calculated.
        
        Args:
            semantic_score (float): Semantic similarity score (0 to 1)
            grammar_score (float): Grammar quality score (0 to 1)
            redundancy_score (float): Redundancy penalty score (0 to 1)
            
        Returns:
            dict: Dictionary containing score breakdown details
        """
        # Validate input scores
        semantic_score = max(0.0, min(1.0, semantic_score))
        grammar_score = max(0.0, min(1.0, grammar_score))
        redundancy_score = max(0.0, min(1.0, redundancy_score))
        
        # Calculate weighted contributions
        semantic_contribution = semantic_score * self.semantic_weight * 100
        grammar_contribution = grammar_score * self.grammar_weight * 100
        redundancy_penalty = redundancy_score * self.redundancy_weight * 100
        
        # Calculate final score
        final_score = self.aggregate_scores(semantic_score, grammar_score, redundancy_score)
        
        return {
            'semantic_score': semantic_score,
            'grammar_score': grammar_score,
            'redundancy_score': redundancy_score,
            'semantic_contribution': semantic_contribution,
            'grammar_contribution': grammar_contribution,
            'redundancy_penalty': redundancy_penalty,
            'final_score': final_score,
            'weights': {
                'semantic': self.semantic_weight,
                'grammar': self.grammar_weight,
                'redundancy': self.redundancy_weight
            }
        }
    
    def set_weights(self, semantic_weight=None, grammar_weight=None, redundancy_weight=None):
        """
        Update the weights used for score aggregation.
        
        Args:
            semantic_weight (float, optional): Weight for semantic similarity
            grammar_weight (float, optional): Weight for grammar quality
            redundancy_weight (float, optional): Weight for redundancy penalty
        """
        if semantic_weight is not None:
            self.semantic_weight = max(0.0, min(1.0, semantic_weight))
        if grammar_weight is not None:
            self.grammar_weight = max(0.0, min(1.0, grammar_weight))
        if redundancy_weight is not None:
            self.redundancy_weight = max(0.0, min(1.0, redundancy_weight))