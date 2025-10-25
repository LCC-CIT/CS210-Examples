# Medical Diagnosis Expert System

## Purpose

This program demonstrates how an expert system works. This simplified example has a knowledge base containing rules that are "forward chained" to derive conclusions from initial facts. **It is not a full-blown system, but just a demo** designed to illustrate some fundamental concepts of expert systems.

## Description

The Medical Diagnosis Expert System is a simple rule-based system that simulates the diagnostic reasoning process used in medical decision-making. Users input symptoms, and the system applies forward chaining inference to derive potential diagnoses and recommendations based on a predefined knowledge base of medical rules.

This system demonstrates:

- How expert systems encode domain knowledge as rules.
- How forward chaining inference derives new facts from existing ones.
- How intermediate facts can lead to final conclusions (diagnoses and recommendations).
- The separation of knowledge (rules) from reasoning (inference engine).

## Program Structure

### Main Components

#### 1. medical_diagnosis.py (Main Program)

The entry point for the application. This file provides the console-based user interface where:

- Users are shown a list of symptoms the knowledge base knows about.
- Users input their symptoms as a comma-separated list.
- The system processes the symptoms and displays diagnoses and recommendations.

#### 2. knowledge_base.py

Contains the medical rules that the system uses for diagnosis. The knowledge base can operate in two modes controlled by the `HARD_CODED_RULES` flag:

- **Hard-coded mode** (`HARD_CODED_RULES = True`): Uses a predefined list of rules embedded in the code.
- **CSV mode** (`HARD_CODED_RULES = False`): Loads rules dynamically from `medical_diagnosis.csv` file.

Each rule consists of:

- **IF conditions**: The facts that must be present (symptoms or intermediate conclusions).
- **THEN conclusion**: The new fact derived when conditions are met.
- **Result type**: Classification as INTERMEDIATE, DIAGNOSIS, or RECOMMENDATION.

#### 3. inference_engine.py

The reasoning component that processes rules and derives conclusions. Contains three main functions:

- `forward_chaining_inference()`: Applies forward chaining algorithm.
- `extract_goals()`: Identifies final diagnoses and recommendations.
- `get_diagnosis()`: High-level function that coordinates inference and result extraction.

#### 4. **medical_diagnosis_tests.py** (Test Suite)

Contains pre-written test scenarios that validate the system's behavior:

- Scenario 1: Influenza diagnosis chain
- Scenario 2: Common cold diagnosis
- Scenario 3: Migraine diagnosis
- Scenario 4: Food poisoning diagnosis
- Scenario 5: Empty symptoms (edge case)
- Scenario 6: Unknown symptoms (edge case)
- Scenario 7: Case insensitivity test
- Scenario 8: Symptom order independence
- Scenario 9: Duplicate symptom handling

Each test displays expected vs. actual results and shows PASS/FAIL status.

Run this file to verify the system works correctly without manual input.

#### 5. **medical_diagnosis.csv** (Knowledge Base Data)

CSV file containing rules in a tabular format with columns:

- `if`: Primary condition.
- `and`: Additional condition (optional).
- `then`: Derived conclusion
- `result_type`: Classification of the conclusion

### File Dependencies

```
medical_diagnosis.py
    ↓ imports from
inference_engine.py
    ↓ imports from
knowledge_base.py
    ↓ loads (if CSV mode)
medical_diagnosis.csv
```

## Forward Chaining Explained

*Forward chaining* is a data-driven inference method that starts with known facts and applies rules repeatedly to derive new facts until no more conclusions can be drawn.

### How It Works

1. Start with *initial facts* (user-provided symptoms).
2. Find rules whose conditions are satisfied by current facts.
3. When a rule's conditions are met, add its conclusion to the fact set.
4. Repeat steps 2-3 until no new facts can be derived.
5. Extract final diagnoses and recommendations from derived facts.

### Rule Chaining in This System

The following table shows how rules chain together in this system:

| Rule # | IF Conditions | THEN Conclusion | Result Type | Description |
|--------|--------------|-----------------|-------------|-------------|
| 1 | fever AND cough | suspect_flu | INTERMEDIATE | Initial flu suspicion |
| 2 | headache AND nausea | suspect_migraine | INTERMEDIATE | Initial migraine suspicion |
| 3 | suspect_flu AND body_aches | diagnosis:influenza | DIAGNOSIS | Confirms influenza |
| 4 | suspect_flu AND sore_throat | diagnosis:common_cold | DIAGNOSIS | Distinguishes cold from flu |
| 5 | suspect_migraine AND light_sensitivity | diagnosis:migraine | DIAGNOSIS | Confirms migraine |
| 6 | diagnosis:influenza | recommendation:rest | RECOMMENDATION | Treatment suggestion |
| 7 | diagnosis:migraine | recommendation:dark_room | RECOMMENDATION | Treatment suggestion |
| 8 | no_appetite AND stomach_pain | diagnosis:food_poisoning | DIAGNOSIS | Direct diagnosis |

**Note:** Diagnoses and recommendations use a colon-based naming convention (e.g., `diagnosis:influenza`, `recommendation:rest`). This allows the `extract_goals()` function to identify final results using prefix matching rather than relying on the `result_type` field.

### Example Chain

```text
Initial Facts: [fever, cough, body_aches]
    ↓ (Rule 1: fever + cough)
Derived: suspect_flu
    ↓ (Rule 3: suspect_flu + body_aches)
Derived: diagnosis:influenza
    ↓ (Rule 6: diagnosis:influenza)
Derived: recommendation:rest

Final Results:
- Diagnoses: [influenza]  (extracted from diagnosis:influenza)
- Recommendations: [rest]  (extracted from recommendation:rest)
```

## How the Inference Engine Works

The inference engine implements the forward chaining algorithm through the following process:

### 1. Initialization

- Convert initial facts (symptoms) to a set for efficient lookup.
- Prepare to track which rules have been applied.

### 2. Iterative Rule Application

```python
while new_fact_added:
    for each rule:
        if all rule conditions are in fact set:
            if rule conclusion not already in fact set:
                add conclusion to fact set
                mark that a new fact was added
```

### 3. **Termination**

The algorithm terminates when a complete pass through all rules produces no new facts, ensuring:

- All possible conclusions have been derived.
- No infinite loops occur.
- Efficient processing (stops when done).

### 4. Result Extraction

After inference completes:

- Filter derived facts using prefix matching: facts starting with `'diagnosis:'` or `'recommendation:'`
- Extract the meaningful part after the colon (e.g., `'diagnosis:influenza'` → `'influenza'`)
- Return structured results separating diagnoses from recommendations
- Exclude intermediate facts from final output

**Implementation Detail**: The `extract_goals()` function uses Python's `str.startswith()` and `str.split()` methods to identify and extract final results, making it independent of the `result_type` field in the knowledge base.

### Key Features

- **Monotonic reasoning**: Facts are only added, never removed
- **Order independence**: Rules can be in any order and produce the same results
- **Completeness**: All derivable conclusions are found
- **Efficiency**: Each rule fires at most once per iteration

## Running the Program

### Interactive Mode

```bash
python medical_diagnosis.py
```

Follow the prompts to enter symptoms and receive diagnoses.

### Test Mode

```bash
python medical_diagnosis_tests.py
```

Runs predefined test scenarios to validate system behavior.

### Switching Between Hard-coded and CSV Rules

Edit `knowledge_base.py`:

```python
HARD_CODED_RULES = False  # Use CSV file
# or
HARD_CODED_RULES = True   # Use hard-coded rules
```

## Future Enhancement Suggestions

### 1. Enhanced Knowledge Base

- Add more medical conditions and symptoms.
- Include confidence levels or probability scores for diagnoses.
- Implement rule priorities or weights.
- Add support for mutually exclusive diagnoses.
- Include severity indicators (mild, moderate, severe).

### 2. Backward Chaining

- Implement goal-driven reasoning to ask only relevant questions.
- Guide users through diagnostic process more efficiently.
- Reduce unnecessary symptom queries.

### 3. Uncertainty Handling

- Integrate fuzzy logic for symptoms that are not binary (e.g., "slight fever" vs "high fever").
- Implement Bayesian reasoning for probabilistic diagnoses.
- Handle partial or uncertain information.


### 4. Explanation Facility

- Show the reasoning chain that led to each diagnosis.
- Explain why certain questions are asked.
- Provide transparency in decision-making process.
- Display confidence levels with explanations.

### 5. Learning Capabilities

- Implement machine learning to refine rules based on outcomes
- Allow medical professionals to add/modify rules through interface
- Track and learn from diagnostic accuracy
- Adapt to new medical knowledge


### 6. Validation & Testing

- Create comprehensive test suite with edge cases.
- Implement continuous integration for rule validation.
- Add medical professional review workflow.
- Include regression testing for rule changes.


### 7. Safety & Compliance

- Add disclaimers about system limitations
- Implement data privacy protections (HIPAA compliance)
- Include emergency situation detection and referral
- Add audit logging for decision tracking

## Technical Requirements

- Python 3.7 or higher
- No external dependencies (uses only standard library)

## Disclaimer

This is an educational tool only. It should **NOT** be used for actual medical diagnosis. Always consult qualified healthcare professionals for medical advice and treatment.

## Authors

- Initial code generated by Gemini Flash 2.5 (10/6/2025)
- CSV loading and interface by GitHub Copilot with GPT-4.1 (10/11/2025)
- Extensively refactored and enhanced by Brian Bird (10/11/2025 and 10/25/2025)

## License

This code is available under the MIT License.

Educational use only. Not intended for real medical applications.
