from preprocessing.text_normalizer import TextNormalizer
from evaluators.exact_match import ExactMatchEvaluator
from evaluators.semantic_similarity import SemanticSimilarityEvaluator
from evaluators.grammar_checker import GrammarCheckerEvaluator
from evaluators.redundancy_checker import RedundancyCheckerEvaluator
from evaluators.context_evaluator import ContextEvaluator
from evaluators.nli_checker import NLIChecker
from evaluators.structure_analyzer import StructureAnalyzer
from evaluators.theme_evaluator import ThemeEvaluator
from evaluators.syntax_analyzer import SyntaxAnalyzer
from scoring.score_aggregator import ScoreAggregator
from feedback.feedback_generator import FeedbackGenerator


class ScoringPipeline:
    """
    A pipeline for scoring sentences against reference sentences.
    
    This class orchestrates the entire scoring process, from preprocessing
    to final score aggregation, using multiple evaluation layers.
    """
    
    def __init__(self):
        """
        Initialize ScoringPipeline with all necessary components.
        """
        # Initialize all components
        self.text_normalizer = TextNormalizer()
        self.exact_match_evaluator = ExactMatchEvaluator()
        self.semantic_similarity_evaluator = SemanticSimilarityEvaluator()
        self.grammar_checker_evaluator = GrammarCheckerEvaluator()
        self.redundancy_checker_evaluator = RedundancyCheckerEvaluator()
        self.context_evaluator = ContextEvaluator()
        self.nli_checker = NLIChecker()
        self.structure_analyzer = StructureAnalyzer()
        self.theme_evaluator = ThemeEvaluator()
        self.syntax_analyzer = SyntaxAnalyzer()
        self.score_aggregator = ScoreAggregator()
        self.feedback_generator = FeedbackGenerator()
    
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
                'context_score': 1.0,
                'nli_score': 1.0,
                'structure_score': 1.0,
                'theme_score': 1.0,
                'redundancy_score': 0.0,
                'breakdown': {
                    'semantic_contribution': 40.0,
                    'nli_contribution': 20.0,
                    'context_contribution': 10.0,
                    'structure_contribution': 15.0,
                    'grammar_contribution': 10.0,
                    'syntax_contribution': 7.0,
                'theme_contribution': 5.0,
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
        
        context_score = self.context_evaluator.evaluate(
            normalized_user, normalized_reference
        )
        
        nli_score = self.nli_checker.evaluate(
            normalized_reference, normalized_user
        )
        
        structure_analysis = self.structure_analyzer.analyze(
            normalized_user, normalized_reference
        )
        structure_score = structure_analysis['score']
        
        theme_score = self.theme_evaluator.get_score(
            semantic_score
        )
        
        syntax_analysis = self.syntax_analyzer.analyze(
            normalized_user, normalized_reference
        )
        syntax_score = syntax_analysis['score']
        
        # Step 4: Aggregate scores
        final_score = self.score_aggregator.get_final_score(
            semantic_score, nli_score, context_score, structure_score, grammar_score, syntax_score, theme_score, redundancy_score
        )
        
        # Step 5: Get detailed breakdown
        breakdown = self.score_aggregator.get_score_breakdown(
            semantic_score, nli_score, context_score, structure_score, grammar_score, syntax_score, theme_score, redundancy_score
        )
        
        return {
            'final_score': final_score,
            'is_exact_match': False,
            'semantic_score': semantic_score,
            'grammar_score': grammar_score,
            'context_score': context_score,
            'nli_score': nli_score,
            'structure_score': structure_score,
            'theme_score': theme_score,
            'redundancy_score': redundancy_score,
            'syntax_score': syntax_score,
            'structure_details': structure_analysis['details'],
            'syntax_details': syntax_analysis['details'],
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