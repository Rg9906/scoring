from transformers import pipeline
import torch


class NLIChecker:
    """
    A class for Natural Language Inference checking.
    
    This evaluator uses a pretrained NLI model to detect entailment,
    contradiction, or neutrality between sentences.
    """
    
    def __init__(self, model_name='facebook/bart-large-mnli'):
        """
        Initialize the NLIChecker with a pretrained NLI model.
        
        Args:
            model_name (str): The name of the NLI model to use
        """
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1
        self.classifier = None
        self._load_model()
    
    def _load_model(self):
        """
        Load the NLI model pipeline.
        """
        try:
            self.classifier = pipeline(
                "zero-shot-classification",
                model=self.model_name,
                device=self.device
            )
        except Exception as e:
            print(f"Warning: Could not load NLI model {self.model_name}: {e}")
            self.classifier = None
    
    def evaluate(self, reference_sentence, user_sentence):
        """
        Evaluate the relationship between reference and user sentences.
        
        Args:
            reference_sentence (str): The reference sentence (premise)
            user_sentence (str): The user sentence (hypothesis)
            
        Returns:
            float: NLI score between 0 and 1
                   (1.0 = entailment, 0.5 = neutral, 0.0 = contradiction)
        """
        if reference_sentence is None or user_sentence is None:
            return 0.0
        
        if reference_sentence.strip() == "" or user_sentence.strip() == "":
            return 0.0
        
        if self.classifier is None:
            # Fallback to semantic similarity if NLI model fails to load
            return self._fallback_similarity(reference_sentence, user_sentence)
        
        try:
            # Define the candidate labels for NLI
            candidate_labels = ["entailment", "neutral", "contradiction"]
            
            # Perform NLI classification
            result = self.classifier(
                user_sentence,
                candidate_labels,
                hypothesis_template="This text {} the reference: {}"
            )
            
            # Extract probabilities
            scores = result['scores']
            labels = result['labels']
            
            # Create a mapping of label to score
            score_map = dict(zip(labels, scores))
            
            # Convert to NLI score
            entailment_score = score_map.get('entailment', 0.0)
            neutral_score = score_map.get('neutral', 0.0)
            contradiction_score = score_map.get('contradiction', 0.0)
            
            # Calculate weighted NLI score
            nli_score = (
                entailment_score * 1.0 +
                neutral_score * 0.5 +
                contradiction_score * 0.0
            )
            
            return nli_score
            
        except Exception as e:
            print(f"Warning: NLI evaluation failed: {e}")
            return self._fallback_similarity(reference_sentence, user_sentence)
    
    def get_score(self, reference_sentence, user_sentence):
        """
        Get the NLI score between reference and user sentences.
        
        Args:
            reference_sentence (str): The reference sentence (premise)
            user_sentence (str): The user sentence (hypothesis)
            
        Returns:
            float: NLI score between 0 and 1
        """
        return self.evaluate(reference_sentence, user_sentence)
    
    def get_detailed_analysis(self, reference_sentence, user_sentence):
        """
        Get detailed NLI analysis with individual probabilities.
        
        Args:
            reference_sentence (str): The reference sentence (premise)
            user_sentence (str): The user sentence (hypothesis)
            
        Returns:
            dict: Dictionary containing detailed NLI analysis
        """
        if reference_sentence is None or user_sentence is None:
            return {
                'nli_score': 0.0,
                'entailment': 0.0,
                'neutral': 0.0,
                'contradiction': 0.0,
                'prediction': 'neutral'
            }
        
        if self.classifier is None:
            fallback_score = self._fallback_similarity(reference_sentence, user_sentence)
            return {
                'nli_score': fallback_score,
                'entailment': fallback_score,
                'neutral': 1.0 - fallback_score,
                'contradiction': 0.0,
                'prediction': 'neutral',
                'fallback': True
            }
        
        try:
            candidate_labels = ["entailment", "neutral", "contradiction"]
            result = self.classifier(
                user_sentence,
                candidate_labels,
                hypothesis_template="This text {} the reference: {}"
            )
            
            scores = result['scores']
            labels = result['labels']
            score_map = dict(zip(labels, scores))
            
            entailment_score = score_map.get('entailment', 0.0)
            neutral_score = score_map.get('neutral', 0.0)
            contradiction_score = score_map.get('contradiction', 0.0)
            
            # Determine prediction
            prediction = max(score_map, key=score_map.get)
            
            # Calculate NLI score
            nli_score = (
                entailment_score * 1.0 +
                neutral_score * 0.5 +
                contradiction_score * 0.0
            )
            
            return {
                'nli_score': nli_score,
                'entailment': entailment_score,
                'neutral': neutral_score,
                'contradiction': contradiction_score,
                'prediction': prediction,
                'fallback': False
            }
            
        except Exception as e:
            print(f"Warning: Detailed NLI analysis failed: {e}")
            fallback_score = self._fallback_similarity(reference_sentence, user_sentence)
            return {
                'nli_score': fallback_score,
                'entailment': fallback_score,
                'neutral': 1.0 - fallback_score,
                'contradiction': 0.0,
                'prediction': 'neutral',
                'fallback': True
            }
    
    def _fallback_similarity(self, reference_sentence, user_sentence):
        """
        Fallback method using semantic similarity when NLI model fails.
        
        Args:
            reference_sentence (str): The reference sentence
            user_sentence (str): The user sentence
            
        Returns:
            float: Similarity-based score between 0 and 1
        """
        from models.embedding_model import EmbeddingModel
        
        embedding_model = EmbeddingModel()
        similarity = embedding_model.compute_similarity(reference_sentence, user_sentence)
        return similarity
