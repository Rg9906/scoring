class FeedbackGenerator:
    """
    A class for generating human-readable feedback for sentence scoring.
    
    This class creates detailed explanations of scores and provides
    suggestions for improvement.
    """
    
    def __init__(self):
        """
        Initialize the FeedbackGenerator.
        """
        pass
    
    def generate_feedback(self, scoring_result):
        """
        Generate comprehensive feedback for a scoring result.
        
        Args:
            scoring_result (dict): Dictionary containing all scoring components
            
        Returns:
            dict: Dictionary containing formatted feedback
        """
        feedback = {
            'final_score': scoring_result.get('final_score', 0.0),
            'score_level': self._get_score_level(scoring_result.get('final_score', 0.0)),
            'breakdown': self._generate_breakdown(scoring_result),
            'issues_detected': self._detect_issues(scoring_result),
            'suggestions': self._generate_suggestions(scoring_result)
        }
        
        return feedback
    
    def format_feedback(self, scoring_result):
        """
        Format feedback as readable text.
        
        Args:
            scoring_result (dict): Dictionary containing all scoring components
            
        Returns:
            str: Formatted feedback text
        """
        feedback = self.generate_feedback(scoring_result)
        
        output = []
        output.append(f"Final Score: {feedback['final_score']:.1f}/100 ({feedback['score_level']})")
        output.append("")
        
        # Breakdown
        output.append("Breakdown:")
        for component, score in feedback['breakdown'].items():
            output.append(f"  • {component}: {score:.3f}")
        output.append("")
        
        # Issues
        if feedback['issues_detected']:
            output.append("Issues Detected:")
            for issue in feedback['issues_detected']:
                output.append(f"  • {issue}")
            output.append("")
        
        # Suggestions
        if feedback['suggestions']:
            output.append("Suggestions:")
            for suggestion in feedback['suggestions']:
                output.append(f"  • {suggestion}")
        
        return "\n".join(output)
    
    def _get_score_level(self, score):
        """
        Get the performance level based on score.
        
        Args:
            score (float): Final score between 0 and 100
            
        Returns:
            str: Performance level description
        """
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Very Good"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 50:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def _generate_breakdown(self, scoring_result):
        """
        Generate a breakdown of all component scores.
        
        Args:
            scoring_result (dict): Dictionary containing all scoring components
            
        Returns:
            dict: Dictionary of component names and scores
        """
        breakdown = {}
        
        # Add main components
        components = [
            ('semantic_score', 'Semantic Similarity'),
            ('grammar_score', 'Grammar Quality'),
            ('context_score', 'Context Appropriateness'),
            ('nli_score', 'Logical Consistency'),
            ('structure_score', 'Sentence Structure'),
            ('theme_score', 'Thematic Consistency'),
            ('redundancy_score', 'Redundancy (Penalty)')
        ]
        
        for key, name in components:
            if key in scoring_result:
                breakdown[name] = scoring_result[key]
        
        return breakdown
    
    def _detect_issues(self, scoring_result):
        """
        Detect issues based on component scores.
        
        Args:
            scoring_result (dict): Dictionary containing all scoring components
            
        Returns:
            list: List of detected issues
        """
        issues = []
        
        # Grammar issues
        grammar_score = scoring_result.get('grammar_score', 1.0)
        if grammar_score < 0.8:
            issues.append("Grammar errors detected")
        elif grammar_score < 0.9:
            issues.append("Minor grammar issues")
        
        # Redundancy issues
        redundancy_score = scoring_result.get('redundancy_score', 0.0)
        if redundancy_score > 0.3:
            issues.append("High word repetition")
        elif redundancy_score > 0.1:
            issues.append("Some word repetition")
        
        # Semantic issues
        semantic_score = scoring_result.get('semantic_score', 1.0)
        if semantic_score < 0.5:
            issues.append("Low semantic similarity to reference")
        
        # Context issues
        context_score = scoring_result.get('context_score', 1.0)
        if context_score < 0.5:
            issues.append("Context may be inappropriate")
        
        # NLI issues
        nli_score = scoring_result.get('nli_score', 1.0)
        if nli_score < 0.5:
            issues.append("May contradict the reference meaning")
        
        # Structure issues
        if 'structure_details' in scoring_result:
            structure_details = scoring_result['structure_details']
            if structure_details.get('subject_match', True) == False:
                issues.append("Subject does not match reference")
            if structure_details.get('verb_match', True) == False:
                issues.append("Verb/action does not match reference")
            if structure_details.get('object_match', True) == False:
                issues.append("Object does not match reference")
        
        # Syntax issues
        if 'syntax_details' in scoring_result:
            syntax_details = scoring_result['syntax_details']
            if syntax_details.get('tense_issue', False):
                issues.append("Tense mismatch detected")
            if syntax_details.get('agreement_issue', False):
                issues.append("Subject-verb agreement error")
            if syntax_details.get('preposition_issue', False):
                issues.append("Incorrect preposition usage")
            if syntax_details.get('structure_issue', False):
                issues.append("Sentence structure issue")
        
        return issues
    
    def _generate_suggestions(self, scoring_result):
        """
        Generate suggestions for improvement based on scores.
        
        Args:
            scoring_result (dict): Dictionary containing all scoring components
            
        Returns:
            list: List of improvement suggestions
        """
        suggestions = []
        
        # Grammar suggestions
        grammar_score = scoring_result.get('grammar_score', 1.0)
        if grammar_score < 0.8:
            suggestions.append("Review grammar rules and proofread carefully")
        
        # Redundancy suggestions
        redundancy_score = scoring_result.get('redundancy_score', 0.0)
        if redundancy_score > 0.2:
            suggestions.append("Use more diverse vocabulary to avoid repetition")
        
        # Semantic suggestions
        semantic_score = scoring_result.get('semantic_score', 1.0)
        if semantic_score < 0.6:
            suggestions.append("Focus on expressing the same core meaning as the reference")
        
        # Context suggestions
        context_score = scoring_result.get('context_score', 1.0)
        if context_score < 0.6:
            suggestions.append("Consider the emotional tone and context of the situation")
        
        # NLI suggestions
        nli_score = scoring_result.get('nli_score', 1.0)
        if nli_score < 0.5:
            suggestions.append("Ensure your answer doesn't contradict the reference meaning")
        
        # Structure suggestions
        if 'structure_details' in scoring_result:
            structure_score = scoring_result.get('structure_score', 1.0)
            if structure_score < 0.7:
                suggestions.append("Maintain the same subject-verb-object structure as the reference")
        
        # Syntax suggestions
        if 'syntax_details' in scoring_result:
            syntax_details = scoring_result['syntax_details']
            if syntax_details.get('tense_issue', False):
                suggestions.append("Check verb tense consistency with the reference")
            if syntax_details.get('agreement_issue', False):
                suggestions.append("Ensure subject-verb agreement in number and tense")
            if syntax_details.get('preposition_issue', False):
                suggestions.append("Review preposition usage for common temporal expressions")
            if syntax_details.get('structure_issue', False):
                suggestions.append("Check sentence structure for missing subjects or verbs")
        
        # General suggestions
        final_score = scoring_result.get('final_score', 0.0)
        if final_score < 70:
            suggestions.append("Review all aspects: meaning, grammar, context, structure, and syntax")
        
        return suggestions
