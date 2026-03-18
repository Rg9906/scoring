from models.embedding_model import EmbeddingModel


class SemanticSimilarityEvaluator:
    """
    A class for evaluating semantic similarity between sentences.
    
    This evaluator uses sentence embeddings to compute the semantic
    similarity between two sentences, focusing on meaning rather than exact wording.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the SemanticSimilarityEvaluator.
        
        Args:
            model_name (str): The name of the sentence transformer model to use
        """
        self.embedding_model = EmbeddingModel(model_name)
    
    def evaluate(self, user_sentence, reference_sentence):
        """
        Evaluate the semantic similarity between two sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            float: Semantic similarity score between 0 and 1
        """
        if user_sentence is None or reference_sentence is None:
            return 0.0
        
        if user_sentence.strip() == "" or reference_sentence.strip() == "":
            return 0.0
        
        # Compute semantic similarity using the embedding model
        similarity_score = self.embedding_model.compute_similarity(
            user_sentence, 
            reference_sentence
        )
        
        return similarity_score
    
    def get_score(self, user_sentence, reference_sentence):
        """
        Get the semantic similarity score between two sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            float: Semantic similarity score between 0 and 1
        """
        return self.evaluate(user_sentence, reference_sentence)