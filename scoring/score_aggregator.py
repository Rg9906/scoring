class ScoreAggregator:
    """
    A class for aggregating scores from different evaluators.
    
    This class combines semantic similarity, grammar quality, context appropriateness, NLI consistency, and redundancy
    scores using weighted scoring to produce a final score.
    """
    
    def __init__(self):
        """
        Initialize ScoreAggregator with updated weights for enhanced scoring.
        """
        # Define updated weights for different components
        self.semantic_weight = 0.35
        self.nli_weight = 0.2
        self.structure_weight = 0.15
        self.context_weight = 0.1
        self.grammar_weight = 0.08
        self.syntax_weight = 0.07
        self.theme_weight = 0.05
        self.redundancy_weight = 0.1
    
    def aggregate_scores(self, semantic_score, nli_score, context_score, structure_score, grammar_score, syntax_score, theme_score, redundancy_score):
        """
        Aggregate individual scores into a final weighted score.
        
        Args:
            semantic_score (float): Semantic similarity score (0 to 1)
            nli_score (float): NLI consistency score (0 to 1)
            context_score (float): Context appropriateness score (0 to 1)
            structure_score (float): Structure similarity score (0 to 1)
            grammar_score (float): Grammar quality score (0 to 1)
            syntax_score (float): Syntax quality score (0 to 1)
            theme_score (float): Theme consistency score (0 to 1)
            redundancy_score (float): Redundancy penalty score (0 to 1)
            
        Returns:
            float: Final aggregated score between 0 and 100
        """
        # Validate input scores
        semantic_score = max(0.0, min(1.0, semantic_score))
        nli_score = max(0.0, min(1.0, nli_score))
        context_score = max(0.0, min(1.0, context_score))
        structure_score = max(0.0, min(1.0, structure_score))
        grammar_score = max(0.0, min(1.0, grammar_score))
        syntax_score = max(0.0, min(1.0, syntax_score))
        theme_score = max(0.0, min(1.0, theme_score))
        redundancy_score = max(0.0, min(1.0, redundancy_score))
        
        # Apply updated weighted scoring formula
        # score = (semantic × 0.35) + (nli × 0.2) + (structure × 0.15) + (context × 0.1) + (grammar × 0.08) + (syntax × 0.07) + (theme × 0.05) - (redundancy × 0.1)
        weighted_score = (
            (semantic_score * self.semantic_weight) +
            (nli_score * self.nli_weight) +
            (context_score * self.context_weight) +
            (structure_score * self.structure_weight) +
            (grammar_score * self.grammar_weight) +
            (syntax_score * self.syntax_weight) +
            (theme_score * self.theme_weight) -
            (redundancy_score * self.redundancy_weight)
        )
        
        # Clamp final score between 0 and 1
        weighted_score = max(0.0, min(1.0, weighted_score))
        
        # Convert to 0-100 scale
        final_score = weighted_score * 100
        
        return final_score
    
    def get_final_score(self, semantic_score, nli_score, context_score, structure_score, grammar_score, syntax_score, theme_score, redundancy_score):
        """
        Get final score for the given component scores.
        
        Args:
            semantic_score (float): Semantic similarity score (0 to 1)
            nli_score (float): NLI consistency score (0 to 1)
            context_score (float): Context appropriateness score (0 to 1)
            structure_score (float): Structure similarity score (0 to 1)
            grammar_score (float): Grammar quality score (0 to 1)
            syntax_score (float): Syntax quality score (0 to 1)
            theme_score (float): Theme consistency score (0 to 1)
            redundancy_score (float): Redundancy penalty score (0 to 1)
            
        Returns:
            float: Final aggregated score between 0 and 100
        """
        return self.aggregate_scores(semantic_score, nli_score, context_score, structure_score, grammar_score, syntax_score, theme_score, redundancy_score)
    
    def get_score_breakdown(self, semantic_score, nli_score, context_score, structure_score, grammar_score, syntax_score, theme_score, redundancy_score):
        """
        Get a detailed breakdown of how the final score was calculated.
        
        Args:
            semantic_score (float): Semantic similarity score (0 to 1)
            nli_score (float): NLI consistency score (0 to 1)
            context_score (float): Context appropriateness score (0 to 1)
            structure_score (float): Structure similarity score (0 to 1)
            grammar_score (float): Grammar quality score (0 to 1)
            syntax_score (float): Syntax quality score (0 to 1)
            theme_score (float): Theme consistency score (0 to 1)
            redundancy_score (float): Redundancy penalty score (0 to 1)
            
        Returns:
            dict: Dictionary containing score breakdown details
        """
        # Validate input scores
        semantic_score = max(0.0, min(1.0, semantic_score))
        nli_score = max(0.0, min(1.0, nli_score))
        context_score = max(0.0, min(1.0, context_score))
        structure_score = max(0.0, min(1.0, structure_score))
        grammar_score = max(0.0, min(1.0, grammar_score))
        syntax_score = max(0.0, min(1.0, syntax_score))
        theme_score = max(0.0, min(1.0, theme_score))
        redundancy_score = max(0.0, min(1.0, redundancy_score))
        
        # Calculate weighted contributions
        semantic_contribution = semantic_score * self.semantic_weight * 100
        nli_contribution = nli_score * self.nli_weight * 100
        context_contribution = context_score * self.context_weight * 100
        structure_contribution = structure_score * self.structure_weight * 100
        grammar_contribution = grammar_score * self.grammar_weight * 100
        syntax_contribution = syntax_score * self.syntax_weight * 100
        theme_contribution = theme_score * self.theme_weight * 100
        redundancy_penalty = redundancy_score * self.redundancy_weight * 100
        
        # Calculate final score
        final_score = self.aggregate_scores(semantic_score, nli_score, context_score, structure_score, grammar_score, syntax_score, theme_score, redundancy_score)
        
        return {
            'semantic_score': semantic_score,
            'nli_score': nli_score,
            'context_score': context_score,
            'structure_score': structure_score,
            'grammar_score': grammar_score,
            'syntax_score': syntax_score,
            'theme_score': theme_score,
            'redundancy_score': redundancy_score,
            'semantic_contribution': semantic_contribution,
            'nli_contribution': nli_contribution,
            'context_contribution': context_contribution,
            'structure_contribution': structure_contribution,
            'grammar_contribution': grammar_contribution,
            'syntax_contribution': syntax_contribution,
            'theme_contribution': theme_contribution,
            'redundancy_penalty': redundancy_penalty,
            'final_score': final_score,
            'weights': {
                'semantic': self.semantic_weight,
                'nli': self.nli_weight,
                'context': self.context_weight,
                'structure': self.structure_weight,
                'grammar': self.grammar_weight,
                'syntax': self.syntax_weight,
                'theme': self.theme_weight,
                'redundancy': self.redundancy_weight
            }
        }
    
    def set_weights(self, semantic_weight=None, nli_weight=None, context_weight=None, structure_weight=None, grammar_weight=None, syntax_weight=None, theme_weight=None, redundancy_weight=None):
        """
        Update the weights used for score aggregation.
        
        Args:
            semantic_weight (float, optional): Weight for semantic similarity
            nli_weight (float, optional): Weight for NLI consistency
            context_weight (float, optional): Weight for context appropriateness
            structure_weight (float, optional): Weight for structure similarity
            grammar_weight (float, optional): Weight for grammar quality
            syntax_weight (float, optional): Weight for syntax quality
            theme_weight (float, optional): Weight for theme consistency
            redundancy_weight (float, optional): Weight for redundancy penalty
        """
        if semantic_weight is not None:
            self.semantic_weight = max(0.0, min(1.0, semantic_weight))
        if nli_weight is not None:
            self.nli_weight = max(0.0, min(1.0, nli_weight))
        if context_weight is not None:
            self.context_weight = max(0.0, min(1.0, context_weight))
        if structure_weight is not None:
            self.structure_weight = max(0.0, min(1.0, structure_weight))
        if grammar_weight is not None:
            self.grammar_weight = max(0.0, min(1.0, grammar_weight))
        if syntax_weight is not None:
            self.syntax_weight = max(0.0, min(1.0, syntax_weight))
        if theme_weight is not None:
            self.theme_weight = max(0.0, min(1.0, theme_weight))
        if redundancy_weight is not None:
            self.redundancy_weight = max(0.0, min(1.0, redundancy_weight))