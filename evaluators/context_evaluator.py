from models.embedding_model import EmbeddingModel


class ContextEvaluator:
    """
    A class for evaluating contextual appropriateness between sentences.
    
    This evaluator analyzes whether the user sentence maintains appropriate
    context and emotional tone compared to the reference sentence.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the ContextEvaluator.
        
        Args:
            model_name (str): The name of the sentence transformer model to use
        """
        self.embedding_model = EmbeddingModel(model_name)
    
    def evaluate(self, user_sentence, reference_sentence):
        """
        Evaluate the contextual appropriateness between two sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            float: Context appropriateness score between 0 and 1
        """
        if user_sentence is None or reference_sentence is None:
            return 0.0
        
        if user_sentence.strip() == "" or reference_sentence.strip() == "":
            return 0.0
        
        # Compute semantic similarity as base for context evaluation
        semantic_similarity = self.embedding_model.compute_similarity(
            user_sentence, 
            reference_sentence
        )
        
        # Analyze emotional tone consistency
        tone_score = self._analyze_tone_consistency(user_sentence, reference_sentence)
        
        # Combine semantic similarity and tone consistency
        # Weight tone consistency more heavily for context evaluation
        context_score = (semantic_similarity * 0.4) + (tone_score * 0.6)
        
        # Ensure result is between 0 and 1
        context_score = max(0.0, min(1.0, context_score))
        
        return context_score
    
    def get_score(self, user_sentence, reference_sentence):
        """
        Get the context appropriateness score between two sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            float: Context appropriateness score between 0 and 1
        """
        return self.evaluate(user_sentence, reference_sentence)
    
    def _analyze_tone_consistency(self, user_sentence, reference_sentence):
        """
        Analyze the emotional tone consistency between sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            float: Tone consistency score between 0 and 1
        """
        # Simple heuristic-based tone analysis
        positive_words = {
            'happy', 'joyful', 'excited', 'pleased', 'delighted', 'cheerful',
            'glad', 'satisfied', 'content', 'thrilled', 'ecstatic', 'elated'
        }
        
        negative_words = {
            'sad', 'angry', 'upset', 'disappointed', 'frustrated', 'annoyed',
            'worried', 'anxious', 'depressed', 'miserable', 'devastated', 'grieving'
        }
        
        # Extract tone from both sentences
        user_tone = self._extract_tone(user_sentence, positive_words, negative_words)
        reference_tone = self._extract_tone(reference_sentence, positive_words, negative_words)
        
        # Calculate tone consistency
        if user_tone == 'neutral' or reference_tone == 'neutral':
            # If either is neutral, be more lenient
            return 0.7
        elif user_tone == reference_tone:
            # Same emotional tone
            return 1.0
        else:
            # Opposite emotional tones
            return 0.2
    
    def _extract_tone(self, sentence, positive_words, negative_words):
        """
        Extract the emotional tone from a sentence.
        
        Args:
            sentence (str): The sentence to analyze
            positive_words (set): Set of positive emotion words
            negative_words (set): Set of negative emotion words
            
        Returns:
            str: 'positive', 'negative', or 'neutral'
        """
        words = sentence.lower().split()
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
