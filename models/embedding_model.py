from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingModel:
    """
    A wrapper class for sentence embedding models.
    
    This class provides methods to encode sentences into embeddings
    and compute similarity scores between them.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the embedding model.
        
        Args:
            model_name (str): The name of the sentence transformer model to use
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
    
    def encode_sentence(self, sentence):
        """
        Encode a single sentence into an embedding vector.
        
        Args:
            sentence (str): The sentence to encode
            
        Returns:
            numpy.ndarray: The embedding vector for the sentence
        """
        if sentence is None or sentence.strip() == "":
            # Return zero vector for empty input
            return np.zeros(self.model.get_sentence_embedding_dimension())
        
        embedding = self.model.encode(sentence)
        return embedding
    
    def compute_similarity(self, sentence1, sentence2):
        """
        Compute cosine similarity between two sentences.
        
        Args:
            sentence1 (str): The first sentence
            sentence2 (str): The second sentence
            
        Returns:
            float: Cosine similarity score between 0 and 1
        """
        # Get embeddings for both sentences
        embedding1 = self.encode_sentence(sentence1)
        embedding2 = self.encode_sentence(sentence2)
        
        # Reshape for cosine_similarity function
        embedding1 = embedding1.reshape(1, -1)
        embedding2 = embedding2.reshape(1, -1)
        
        # Compute cosine similarity
        similarity = cosine_similarity(embedding1, embedding2)[0][0]
        
        # Ensure the result is between 0 and 1
        similarity = max(0.0, min(1.0, similarity))
        
        return similarity
    
    def encode_multiple_sentences(self, sentences):
        """
        Encode multiple sentences into embedding vectors.
        
        Args:
            sentences (list): List of sentences to encode
            
        Returns:
            numpy.ndarray: Array of embedding vectors
        """
        if not sentences:
            return np.array([])
        
        embeddings = self.model.encode(sentences)
        return embeddings
