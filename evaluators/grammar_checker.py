import language_tool_python


class GrammarCheckerEvaluator:
    """
    A class for evaluating grammar quality in sentences.
    
    This evaluator uses language_tool_python to detect grammar errors
    and converts the error count into a normalized score.
    """
    
    def __init__(self, language='en-US'):
        """
        Initialize the GrammarCheckerEvaluator.
        
        Args:
            language (str): The language code for grammar checking
        """
        self.language = language
        self.tool = language_tool_python.LanguageTool(language)
    
    def evaluate(self, sentence):
        """
        Evaluate the grammar quality of a sentence.
        
        Args:
            sentence (str): The sentence to evaluate
            
        Returns:
            float: Grammar quality score between 0 and 1
        """
        if sentence is None or sentence.strip() == "":
            return 0.0
        
        # Check for grammar errors
        matches = self.tool.check(sentence)
        error_count = len(matches)
        
        # Convert error count to normalized score
        # score = 1 - (error_count * 0.1)
        # Ensure score does not go below 0
        score = 1.0 - (error_count * 0.1)
        score = max(0.0, score)
        
        return score
    
    def get_score(self, sentence):
        """
        Get the grammar quality score for a sentence.
        
        Args:
            sentence (str): The sentence to evaluate
            
        Returns:
            float: Grammar quality score between 0 and 1
        """
        return self.evaluate(sentence)
    
    def get_error_count(self, sentence):
        """
        Get the number of grammar errors in a sentence.
        
        Args:
            sentence (str): The sentence to check
            
        Returns:
            int: Number of grammar errors found
        """
        if sentence is None or sentence.strip() == "":
            return 0
        
        matches = self.tool.check(sentence)
        return len(matches)
    
    def get_error_details(self, sentence):
        """
        Get detailed information about grammar errors in a sentence.
        
        Args:
            sentence (str): The sentence to check
            
        Returns:
            list: List of grammar error details
        """
        if sentence is None or sentence.strip() == "":
            return []
        
        matches = self.tool.check(sentence)
        error_details = []
        
        for match in matches:
            error_info = {
                'message': match.message,
                'rule_id': match.ruleId,
                'replacements': [str(replacement) for replacement in match.replacements],
                'offset': match.offset,
                'error_length': match.errorLength
            }
            error_details.append(error_info)
        
        return error_details