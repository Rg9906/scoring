import spacy


class StructureAnalyzer:
    """
    A class for analyzing sentence structure and comparing semantic roles.
    
    This evaluator uses spaCy for dependency parsing to extract and compare
    subject, verb, and object roles between sentences.
    """
    
    def __init__(self, model_name='en_core_web_sm'):
        """
        Initialize the StructureAnalyzer.
        
        Args:
            model_name (str): The name of the spaCy model to use
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Warning: spaCy model '{model_name}' not found.")
            print(f"Please run: python -m spacy download {model_name}")
            self.nlp = None
    
    def analyze(self, user_sentence, reference_sentence):
        """
        Analyze and compare the structure of two sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            dict: Dictionary containing structure score and details
        """
        if self.nlp is None:
            return {
                'score': 0.5,  # Default score if spaCy is not available
                'details': {
                    'subject_match': False,
                    'verb_match': False,
                    'object_match': False,
                    'error': 'spaCy model not loaded'
                }
            }
        
        if user_sentence is None or reference_sentence is None:
            return {
                'score': 0.0,
                'details': {
                    'subject_match': False,
                    'verb_match': False,
                    'object_match': False
                }
            }
        
        # Parse both sentences
        user_doc = self.nlp(user_sentence)
        ref_doc = self.nlp(reference_sentence)
        
        # Extract semantic roles from both sentences
        user_structure = self._extract_structure(user_doc)
        ref_structure = self._extract_structure(ref_doc)
        
        # Compare structures
        subject_match = self._compare_tokens(user_structure['subject'], ref_structure['subject'])
        verb_match = self._compare_tokens(user_structure['verb'], ref_structure['verb'])
        object_match = self._compare_tokens(user_structure['object'], ref_structure['object'])
        
        # Calculate structure score
        matches = sum([subject_match, verb_match, object_match])
        total_components = 3
        
        # Handle cases where some components might be missing
        if total_components == 0:
            structure_score = 0.5
        else:
            structure_score = matches / total_components
        
        # Apply partial scoring for similar but not exact matches
        if structure_score > 0 and structure_score < 1:
            structure_score = 0.5 + (structure_score * 0.5)  # Range: 0.5-0.75
        
        return {
            'score': structure_score,
            'details': {
                'subject_match': subject_match,
                'verb_match': verb_match,
                'object_match': object_match,
                'user_structure': user_structure,
                'reference_structure': ref_structure
            }
        }
    
    def get_score(self, user_sentence, reference_sentence):
        """
        Get the structure score between two sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            float: Structure similarity score between 0 and 1
        """
        result = self.analyze(user_sentence, reference_sentence)
        return result['score']
    
    def _extract_structure(self, doc):
        """
        Extract subject, verb, and object from a parsed document.
        
        Args:
            doc: spaCy parsed document
            
        Returns:
            dict: Dictionary containing subject, verb, and object tokens
        """
        structure = {
            'subject': [],
            'verb': [],
            'object': []
        }
        
        for token in doc:
            # Subject (nominal subject)
            if token.dep_ in ('nsubj', 'nsubjpass'):
                structure['subject'].append(token.lemma_.lower())
            
            # Main verb (ROOT)
            elif token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                structure['verb'].append(token.lemma_.lower())
            
            # Object (direct object, prepositional object)
            elif token.dep_ in ('dobj', 'pobj', 'obj'):
                structure['object'].append(token.lemma_.lower())
        
        return structure
    
    def _compare_tokens(self, user_tokens, ref_tokens):
        """
        Compare two lists of tokens for similarity.
        
        Args:
            user_tokens (list): List of user tokens
            ref_tokens (list): List of reference tokens
            
        Returns:
            bool: True if tokens match, False otherwise
        """
        if not user_tokens and not ref_tokens:
            return True  # Both empty - consider as match
        
        if not user_tokens or not ref_tokens:
            return False  # One empty, one not - no match
        
        # Check for any overlap between token sets
        user_set = set(user_tokens)
        ref_set = set(ref_tokens)
        
        # If there's any overlap, consider it a partial match
        overlap = user_set.intersection(ref_set)
        
        if overlap:
            # Full match if all tokens overlap
            if len(overlap) == len(user_set) and len(overlap) == len(ref_set):
                return True
            else:
                # Partial match - will be handled in scoring
                return False
        
        return False
