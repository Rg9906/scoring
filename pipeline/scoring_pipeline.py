from preprocessing.text_normalizer import TextNormalizer
from evaluators.exact_match import ExactMatchEvaluator
from evaluators.semantic_similarity import SemanticSimilarityEvaluator
from evaluators.grammar_checker import GrammarCheckerEvaluator
from evaluators.redundancy_checker import RedundancyCheckerEvaluator
from scoring.score_aggregator import ScoreAggregator


class ScoringPipeline:
    """
    A pipeline for scoring sentences against reference sentences.
    
    This class orchestrates the entire scoring process, from preprocessing
    to final score aggregation, using multiple evaluation layers.
    """
    
    def __init__(self):
        """
        Initialize the ScoringPipeline with all necessary components.
        """
        # Initialize all components
        self.text_normalizer = TextNormalizer()
        self.exact_match_evaluator = ExactMatchEvaluator()
        self.semantic_similarity_evaluator = SemanticSimilarityEvaluator()
        self.grammar_checker_evaluator = GrammarCheckerEvaluator()
        self.redundancy_checker_evaluator = RedundancyCheckerEvaluator()
        self.score_aggregator = ScoreAggregator()
    
    def score_sentence(self, user_sentence, reference_sentence):
        """
        Score a user sentence against a reference sentence.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            dict: Dictionary containing the final score and detailed breakdown
        """
        # Step 1: Check exact match first (fast path)
        is_exact_match, exact_match_score = self.exact_match_evaluator.evaluate(
            user_sentence, reference_sentence
        )
        
        if is_exact_match:
            return {
                'final_score': exact_match_score,
                'is_exact_match': True,
                'semantic_score': 1.0,
                'grammar_score': 1.0,
                'redundancy_score': 0.0,
                'breakdown': {
                    'semantic_contribution': 70.0,
                    'grammar_contribution': 20.0,
                    'redundancy_penalty': 0.0
                }
            }
        
        # Step 2: Normalize both sentences
        normalized_user = self.text_normalizer.normalize_text(user_sentence)
        normalized_reference = self.text_normalizer.normalize_text(reference_sentence)
        
        # Step 3: Compute individual scores
        semantic_score = self.semantic_similarity_evaluator.evaluate(
            normalized_user, normalized_reference
        )
        
        grammar_score = self.grammar_checker_evaluator.evaluate(
            normalized_user
        )
        
        redundancy_score = self.redundancy_checker_evaluator.evaluate(
            normalized_user
        )
        
        # Step 4: Aggregate scores
        final_score = self.score_aggregator.get_final_score(
            semantic_score, grammar_score, redundancy_score
        )
        
        # Step 5: Get detailed breakdown
        breakdown = self.score_aggregator.get_score_breakdown(
            semantic_score, grammar_score, redundancy_score
        )
        
        return {
            'final_score': final_score,
            'is_exact_match': False,
            'semantic_score': semantic_score,
            'grammar_score': grammar_score,
            'redundancy_score': redundancy_score,
            'breakdown': breakdown,
            'normalized_user_sentence': normalized_user,
            'normalized_reference_sentence': normalized_reference
        }
    
    def get_simple_score(self, user_sentence, reference_sentence):
        """
        Get just the final score without detailed breakdown.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            float: Final score between 0 and 100
        """
        result = self.score_sentence(user_sentence, reference_sentence)
        return result['final_score']
    
    def evaluate_batch(self, user_sentences, reference_sentences):
        """
        Evaluate multiple sentence pairs.
        
        Args:
            user_sentences (list): List of user sentences
            reference_sentences (list): List of reference sentences
            
        Returns:
            list: List of scoring results for each pair
        """
        if len(user_sentences) != len(reference_sentences):
            raise ValueError("Number of user sentences and reference sentences must match")
        
        results = []
        for user_sent, ref_sent in zip(user_sentences, reference_sentences):
            result = self.score_sentence(user_sent, ref_sent)
            results.append(result)
        
        return results