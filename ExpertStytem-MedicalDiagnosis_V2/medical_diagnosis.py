# medical_diagnosis.py
# Console interface for the medical diagnosis expert system.
# Code by Brian Bird using GitHub Copilot with GPT-4.1, 10/11/2025

from inference_engine import get_diagnosis
from knowledge_base import KNOWLEDGE_BASE, IF_KEY, AND_KEY

# Constants for result dictionary keys
DIAGNOSES_KEY = 'diagnoses'
RECOMMENDATIONS_KEY = 'recommendations'

def main():
    """
    Main entry point for the medical diagnosis expert system.
    
    This function provides an interactive console interface that:
    1. Displays all possible symptoms from the knowledge base
    2. Prompts the user to enter their symptoms as a comma-separated list
    3. Processes the symptoms through the inference engine
    4. Displays the resulting diagnoses and recommendations
    
    The function extracts all symptoms from both the 'if' and 'and' keys in the
    knowledge base rules to show users what symptoms the system recognizes.
    
    Args:
        None
        
    Returns:
        None
        
    Side Effects:
        - Prints welcome message and available symptoms to console
        - Prompts user for input via console
        - Prints diagnostic results to console
    """
    # Collect all possible symptoms from the 'IF' and 'AND' properties in the knowledge base
    possible_symptoms = set()
    for rule in KNOWLEDGE_BASE:
        if IF_KEY in rule and rule[IF_KEY]:
            # Handle both set and string values for IF_KEY
            if isinstance(rule[IF_KEY], set):
                possible_symptoms.update(rule[IF_KEY])
            else:
                possible_symptoms.add(rule[IF_KEY])
        if AND_KEY in rule and rule[AND_KEY]:
            # Handle both set and string values for AND_KEY
            if isinstance(rule[AND_KEY], set):
                possible_symptoms.update(rule[AND_KEY])
            else:
                possible_symptoms.add(rule[AND_KEY])
    print("Welcome to the Medical Diagnosis Expert System!")
    print("Possible symptoms:")
    print(", ".join(sorted(possible_symptoms)))
    print("Enter your symptoms, separated by commas (case-insensitive):")
    print("Examples: fever,cough OR Fever, Cough, Body_Aches")
    user_input = input("Symptoms: ")
    # Split input by comma, strip whitespace, and filter out empty strings
    symptoms = [s.strip().lower() for s in user_input.split(',') if s.strip()]
    if not symptoms:
        print("No symptoms entered. Exiting.")
        return
    results = get_diagnosis(symptoms)
    diagnoses = results.get(DIAGNOSES_KEY) or ['None']
    recommendations = results.get(RECOMMENDATIONS_KEY) or ['None']
    print("\n--- Results ---")
    print("Diagnoses:", ", ".join(diagnoses))
    print("Recommendations:", ", ".join(recommendations))

if __name__ == "__main__":
    main()
