import spacy


class SyntaxAnalyzer:
    """
    A class for advanced syntax and tense analysis.
    
    This evaluator goes beyond basic grammar checking to analyze
    tense consistency, subject-verb agreement, and sentence structure.
    """
    
    def __init__(self, model_name='en_core_web_sm'):
        """
        Initialize SyntaxAnalyzer.
        
        Args:
            model_name (str): The name of spaCy model to use
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Warning: spaCy model '{model_name}' not found.")
            print(f"Please run: python -m spacy download {model_name}")
            self.nlp = None
    
    def analyze(self, user_sentence, reference_sentence):
        """
        Analyze syntax and tense consistency between two sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            dict: Dictionary containing syntax score and detailed issues
        """
        if self.nlp is None:
            return {
                'score': 0.7,  # Default score if spaCy is not available
                'details': {
                    'tense_issue': False,
                    'agreement_issue': False,
                    'preposition_issue': False,
                    'structure_issue': False,
                    'error': 'spaCy model not loaded'
                }
            }
        
        if user_sentence is None or reference_sentence is None:
            return {
                'score': 0.0,
                'details': {
                    'tense_issue': False,
                    'agreement_issue': False,
                    'preposition_issue': False,
                    'structure_issue': False
                }
            }
        
        # Parse both sentences
        user_doc = self.nlp(user_sentence)
        ref_doc = self.nlp(reference_sentence)
        
        # Extract linguistic features
        user_features = self._extract_linguistic_features(user_doc)
        ref_features = self._extract_linguistic_features(ref_doc)
        
        # Analyze issues
        tense_issue = self._check_tense_consistency(user_features, ref_features)
        agreement_issue = self._check_subject_verb_agreement(user_features)
        preposition_issue = self._check_preposition_usage(user_features)
        structure_issue = self._check_sentence_structure(user_features)
        
        # Calculate syntax score (start with 1.0, apply penalties)
        score = 1.0
        
        if tense_issue:
            score -= 0.3
        if agreement_issue:
            score -= 0.3
        if preposition_issue:
            score -= 0.2
        if structure_issue:
            score -= 0.2
        
        # Ensure score stays within bounds
        score = max(0.0, min(1.0, score))
        
        return {
            'score': score,
            'details': {
                'tense_issue': tense_issue,
                'agreement_issue': agreement_issue,
                'preposition_issue': preposition_issue,
                'structure_issue': structure_issue,
                'user_features': user_features,
                'reference_features': ref_features
            }
        }
    
    def get_score(self, user_sentence, reference_sentence):
        """
        Get syntax score between two sentences.
        
        Args:
            user_sentence (str): The user's input sentence
            reference_sentence (str): The reference sentence to compare against
            
        Returns:
            float: Syntax score between 0 and 1
        """
        result = self.analyze(user_sentence, reference_sentence)
        return result['score']
    
    def _extract_linguistic_features(self, doc):
        """
        Extract linguistic features from a parsed document.
        
        Args:
            doc: spaCy parsed document
            
        Returns:
            dict: Dictionary containing linguistic features
        """
        features = {
            'tenses': set(),
            'subjects': [],
            'verbs': [],
            'subject_verb_agreement': True,
            'prepositions': set(),
            'has_structure': True
        }
        
        for token in doc:
            # Extract tenses from verbs
            if token.pos_ == 'VERB' and token.tag_:
                tense = self._get_tense_from_tag(token.tag_)
                if tense:
                    features['tenses'].add(tense)
                features['verbs'].append({
                    'text': token.text.lower(),
                    'lemma': token.lemma_.lower(),
                    'tag': token.tag_
                })
            
            # Extract subjects
            elif token.dep_ in ('nsubj', 'nsubjpass'):
                features['subjects'].append({
                    'text': token.text.lower(),
                    'tag': token.tag_,
                    'number': self._get_number_from_tag(token.tag_)
                })
            
            # Extract prepositions
            elif token.pos_ == 'ADP':
                features['prepositions'].add(token.text.lower())
        
        # Check subject-verb agreement
        if features['subjects'] and features['verbs']:
            features['subject_verb_agreement'] = self._check_agreement_rules(
                features['subjects'], features['verbs']
            )
        
        return features
    
    def _get_tense_from_tag(self, tag):
        """
        Extract tense from Penn Treebank tag.
        
        Args:
            tag (str): Penn Treebank tag
            
        Returns:
            str: Tense name or None
        """
        if not tag:
            return None
        
        # Common tense patterns in Penn Treebank tags
        if tag.startswith('VB'):
            if tag == 'VBD':  # Past tense
                return 'past'
            elif tag == 'VBP':  # Present tense, non-3rd person singular
                return 'present'
            elif tag == 'VBZ':  # Present tense, 3rd person singular
                return 'present'
            elif tag == 'VBG':  # Present participle/gerund
                return 'present_participle'
            elif tag == 'VBN':  # Past participle
                return 'past_participle'
            elif tag == 'VB':  # Base form
                return 'base'
        
        return None
    
    def _get_number_from_tag(self, tag):
        """
        Extract number (singular/plural) from Penn Treebank tag.
        
        Args:
            tag (str): Penn Treebank tag
            
        Returns:
            str: 'singular' or 'plural' or None
        """
        if not tag:
            return None
        
        # Singular patterns
        if tag in ('NN', 'NNP', 'VBZ'):
            return 'singular'
        # Plural patterns
        elif tag in ('NNS', 'NNPS', 'VBP'):
            return 'plural'
        
        return None
    
    def _check_tense_consistency(self, user_features, ref_features):
        """
        Check if tenses are consistent between sentences.
        
        Args:
            user_features (dict): User sentence linguistic features
            ref_features (dict): Reference sentence linguistic features
            
        Returns:
            bool: True if tense mismatch detected
        """
        user_tenses = user_features.get('tenses', set())
        ref_tenses = ref_features.get('tenses', set())
        
        # If both have no clear tense, consider as consistent
        if not user_tenses and not ref_tenses:
            return False
        
        # Check for tense conflicts
        if user_tenses and ref_tenses:
            # Past vs present conflict
            if ('past' in user_tenses and 'present' in ref_tenses) or \
               ('present' in user_tenses and 'past' in ref_tenses):
                return True
        
        return False
    
    def _check_subject_verb_agreement(self, features):
        """
        Check subject-verb agreement in a sentence.
        
        Args:
            features (dict): Linguistic features of a sentence
            
        Returns:
            bool: True if agreement issue detected
        """
        subjects = features.get('subjects', [])
        verbs = features.get('verbs', [])
        
        for subject in subjects:
            subject_number = subject.get('number')
            if subject_number:
                for verb in verbs:
                    verb_tag = verb.get('tag')
                    if verb_tag and self._get_number_from_tag(verb_tag):
                        verb_number = self._get_number_from_tag(verb_tag)
                        # Check singular/plural mismatch
                        if subject_number == 'singular' and verb_number == 'plural':
                            return True
                        elif subject_number == 'plural' and verb_number == 'singular':
                            return True
        
        return False
    
    def _check_agreement_rules(self, subjects, verbs):
        """
        Apply basic subject-verb agreement rules.
        
        Args:
            subjects (list): List of subject tokens
            verbs (list): List of verb tokens
            
        Returns:
            bool: True if agreement is correct
        """
        # Simple heuristic check
        for subject in subjects:
            subject_text = subject['text']
            for verb in verbs:
                verb_text = verb['text']
                
                # Common agreement patterns
                if (subject_text.endswith('s') and verb_text.startswith('is')) or \
                   (subject_text.endswith('s') and verb_text.startswith('are')):
                    continue  # Likely correct
                elif (not subject_text.endswith('s') and verb_text.startswith('is')) or \
                     (not subject_text.endswith('s') and verb_text.startswith('are')):
                    continue  # Likely correct
                else:
                    # Potential mismatch
                    if subject_text in ('he', 'she', 'it') and verb_text.startswith('are'):
                        return False
                    elif subject_text in ('they', 'we') and verb_text.startswith('is'):
                        return False
        
        return True
    
    def _check_preposition_usage(self, features):
        """
        Check for common preposition errors.
        
        Args:
            features (dict): Linguistic features of a sentence
            
        Returns:
            bool: True if preposition issue detected
        """
        prepositions = features.get('prepositions', set())
        
        # Common error patterns
        error_patterns = [
            'on yesterday',  # Should be 'yesterday', not 'on yesterday'
            'in today',    # Should be 'today', not 'in today'
            'at tomorrow',  # Should be 'tomorrow', not 'at tomorrow'
        ]
        
        sentence_text = ' '.join(prepositions)
        for pattern in error_patterns:
            if pattern in sentence_text:
                return True
        
        return False
    
    def _check_sentence_structure(self, features):
        """
        Check for basic sentence structure validity.
        
        Args:
            features (dict): Linguistic features of a sentence
            
        Returns:
            bool: True if structure issue detected
        """
        # Check if sentence has both subject and verb
        has_subject = len(features.get('subjects', [])) > 0
        has_verb = len(features.get('verbs', [])) > 0
        
        if not has_subject or not has_verb:
            return True  # Missing essential components
        
        return False
