from pipeline.scoring_pipeline import ScoringPipeline


def main():
    """
    Main function to run the sentence scoring system.
    
    This function prompts the user for input sentences and displays
    the scoring results with detailed breakdown.
    """
    print("=== Advanced Sentence Scoring System ===")
    print("Evaluate sentences based on semantic meaning, grammar, and redundancy")
    print()
    
    # Initialize the scoring pipeline
    pipeline = ScoringPipeline()
    
    while True:
        print("\n" + "="*50)
        print("Enter your sentences (or type 'quit' to exit):")
        
        # Get user input
        user_sentence = input("User sentence: ").strip()
        
        if user_sentence.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not user_sentence:
            print("Error: Please enter a valid sentence.")
            continue
        
        reference_sentence = input("Reference sentence: ").strip()
        
        if reference_sentence.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not reference_sentence:
            print("Error: Please enter a valid reference sentence.")
            continue
        
        try:
            # Score the sentences
            print("\nScoring...")
            result = pipeline.score_sentence(user_sentence, reference_sentence)
            
            # Display results
            print("\n" + "="*50)
            print("SCORING RESULTS")
            print("="*50)
            
            print(f"Final Score: {result['final_score']:.2f}/100")
            
            if result['is_exact_match']:
                print("Result: EXACT MATCH!")
                print("The sentences are identical after normalization.")
            else:
                print(f"Semantic Similarity: {result['semantic_score']:.3f}")
                print(f"Grammar Quality: {result['grammar_score']:.3f}")
                print(f"Redundancy Penalty: {result['redundancy_score']:.3f}")
                
                # Show detailed breakdown
                breakdown = result['breakdown']
                print("\nScore Breakdown:")
                print(f"  Semantic (70%): {breakdown['semantic_contribution']:.2f}")
                print(f"  Grammar (20%): {breakdown['grammar_contribution']:.2f}")
                print(f"  Redundancy (-10%): -{breakdown['redundancy_penalty']:.2f}")
                
                # Show normalized sentences
                print("\nNormalized Sentences:")
                print(f"  User:     {result['normalized_user_sentence']}")
                print(f"  Reference: {result['normalized_reference_sentence']}")
            
        except Exception as e:
            print(f"Error during scoring: {str(e)}")
            print("Please check your input and try again.")


def demo_mode():
    """
    Run a demonstration with predefined examples.
    """
    print("=== DEMO MODE ===")
    print("Testing the scoring system with predefined examples")
    print()
    
    pipeline = ScoringPipeline()
    
    # Test cases
    test_cases = [
        {
            'user': "I am happy today",
            'reference': "I am happy today",
            'description': "Exact match test"
        },
        {
            'user': "I feel joyful today",
            'reference': "I am happy today", 
            'description': "Semantic similarity test (synonyms)"
        },
        {
            'user': "The apple was eaten by him",
            'reference': "He ate the apple",
            'description': "Active/passive voice test"
        },
        {
            'user': "I is happy today",
            'reference': "I am happy today",
            'description': "Grammar error test"
        },
        {
            'user': "I am happy happy happy",
            'reference': "I am happy today",
            'description': "Redundancy test"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['description']} ---")
        print(f"User:     '{test_case['user']}'")
        print(f"Reference: '{test_case['reference']}'")
        
        result = pipeline.score_sentence(test_case['user'], test_case['reference'])
        print(f"Score: {result['final_score']:.2f}/100")
        
        if not result['is_exact_match']:
            print(f"  Semantic: {result['semantic_score']:.3f}")
            print(f"  Grammar:  {result['grammar_score']:.3f}")
            print(f"  Redundancy: {result['redundancy_score']:.3f}")


if __name__ == "__main__":
    print("Choose mode:")
    print("1. Interactive mode")
    print("2. Demo mode")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "2":
        demo_mode()
    else:
        main()