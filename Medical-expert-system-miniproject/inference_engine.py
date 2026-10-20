"""
inference_engine.py
===================
Rule-Based Forward Chaining Inference Engine for Medical Expert System.

College AI Viva Concepts:
-------------------------
1. KNOWLEDGE BASE (KB):
   Stores domain knowledge as a collection of explicit IF-THEN rules
   and symptom definitions loaded from `rules.json`.

2. WORKING MEMORY (FACT BASE):
   Represents current known facts (initially the user's selected symptoms,
   and dynamically expanded as new conclusions are derived).

3. INFERENCE ENGINE (FORWARD CHAINING):
   A data-driven reasoning strategy:
   - Starts with known facts in Working Memory.
   - Searches for rules whose IF-conditions (antecedents) are fully satisfied.
   - Executes (fires) matching rules and asserts their THEN-conclusions (consequents)
     into Working Memory as new facts.
   - Repeats in cycles until no new rules can fire (fixed-point termination).

4. EXPLANATION FACILITY:
   Records the exact reasoning audit trail (which rule fired, in which cycle,
   what symptoms triggered it, and what conclusion it produced).

DISCLAIMER:
This is strictly an educational demonstration for artificial intelligence coursework.
It does not diagnose real diseases or replace qualified healthcare practitioners.
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Any


def load_knowledge_base(rules_file: str = "rules.json") -> Dict[str, Any]:
    """
    Loads rules and symptom definitions from a JSON file into memory.
    """
    rule_path = Path(rules_file)
    if not rule_path.exists():
        # Fallback to current script directory if relative path fails
        rule_path = Path(__file__).parent / rules_file

    with open(rule_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def run_forward_chaining(knowledge_base: Dict[str, Any], selected_symptoms: List[str]) -> Dict[str, Any]:
    """
    Executes forward chaining inference based on selected symptoms.

    Parameters:
    -----------
    knowledge_base : dict
        Contains 'rules' (list of IF-THEN rule dicts) and 'symptoms_dictionary'.
    selected_symptoms : list of str
        The initial facts provided by the user.

    Returns:
    --------
    dict:
        Detailed inference results containing working memory, fired rules,
        reasoning trace, and safety flags.
    """
    rules: List[Dict[str, Any]] = knowledge_base.get("rules", [])
    
    # 1. Initialize Working Memory with the initial known facts
    working_memory: Set[str] = set(selected_symptoms)
    
    # Track which rules have already fired so no rule fires more than once
    fired_rule_ids: Set[str] = set()
    
    # Audit trail of fired rules in order of execution
    fired_rules: List[Dict[str, Any]] = []
    
    cycle = 0
    
    # 2. Forward Chaining Loop (Data-Driven Reasoning)
    while True:
        cycle += 1
        new_fact_added_in_cycle = False
        
        for rule in rules:
            rule_id = rule["id"]
            
            # Rule has already fired; skip to prevent redundant or infinite loops
            if rule_id in fired_rule_ids:
                continue
                
            conditions: List[str] = rule.get("if_all", [])
            
            # Check if all IF-conditions are currently present in Working Memory
            if all(condition in working_memory for condition in conditions):
                # FIRE THE RULE!
                fired_rule_ids.add(rule_id)
                new_fact = rule["then_add"]
                
                # Check if this conclusion is brand new to Working Memory
                is_novel_fact = new_fact not in working_memory
                working_memory.add(new_fact)
                
                fired_record = {
                    "rule_id": rule_id,
                    "rule_name": rule.get("name", f"Rule {rule_id}"),
                    "cycle": cycle,
                    "matched_conditions": conditions,
                    "conclusion_fact": new_fact,
                    "conclusion_text": rule.get("conclusion_text", ""),
                    "explanation": rule.get("explanation", ""),
                    "is_intermediate": rule.get("is_intermediate", False),
                    "is_urgent": rule.get("is_urgent", False)
                }
                fired_rules.append(fired_record)
                
                if is_novel_fact:
                    new_fact_added_in_cycle = True
                    
        # Termination Condition: No new facts added in this cycle
        if not new_fact_added_in_cycle:
            break

    # Determine derived/inferred facts (excluding initial user symptoms)
    inferred_facts = working_memory - set(selected_symptoms)
    has_urgent_alert = any(r.get("is_urgent", False) for r in fired_rules)
    
    # Separate displayable final conclusions from internal intermediate facts
    final_conclusions = [r for r in fired_rules if not r.get("is_intermediate", False)]

    return {
        "initial_facts": sorted(list(selected_symptoms)),
        "final_working_memory": sorted(list(working_memory)),
        "inferred_facts": sorted(list(inferred_facts)),
        "fired_rules": fired_rules,
        "final_conclusions": final_conclusions,
        "total_cycles": cycle,
        "rules_fired_count": len(fired_rules),
        "has_urgent_alert": has_urgent_alert,
        "matched": len(fired_rules) > 0
    }


# ============================================================================
# STANDALONE TEST SUITE
# Allows testing the engine independently of the Streamlit UI.
# Run from terminal: python inference_engine.py
# ============================================================================

def run_standalone_tests():
    """Runs automated test cases to verify the inference engine."""
    print("=" * 70)
    print("RUNNING INFERENCE ENGINE STANDALONE VERIFICATION TESTS")
    print("=" * 70)

    kb = load_knowledge_base("rules.json")
    print(f"[*] Loaded Knowledge Base with {len(kb.get('rules', []))} rules.")

    tests = [
        {
            "name": "Test Case 1: Single-Step Rule (Gastrointestinal Pattern)",
            "inputs": ["nausea", "vomiting"],
            "expected_rule_id": "R4",
            "expected_fact": "gastrointestinal_distress_pattern"
        },
        {
            "name": "Test Case 2: Multi-Step Chaining (Respiratory -> Upper Respiratory)",
            "inputs": ["fever", "cough", "sore_throat"],
            "expected_rule_id": "R2",
            "expected_fact": "upper_respiratory_pattern"
        },
        {
            "name": "Test Case 3: Red-Flag Emergency Rule (Chest Pain)",
            "inputs": ["chest_pain"],
            "expected_rule_id": "R8",
            "expected_fact": "emergency_cardiovascular_alert"
        },
        {
            "name": "Test Case 4: Negative Case (No Rule Should Match)",
            "inputs": ["runny_nose"],
            "expected_rule_id": None,
            "expected_fact": None
        }
    ]

    all_passed = True

    for i, test in enumerate(tests, start=1):
        print(f"\n[{i}] {test['name']}")
        print(f"    Inputs: {test['inputs']}")
        result = run_forward_chaining(kb, test["inputs"])
        fired_ids = [r["rule_id"] for r in result["fired_rules"]]
        print(f"    Fired Rules: {fired_ids if fired_ids else 'None'}")
        print(f"    Inferred Facts: {result['inferred_facts'] if result['inferred_facts'] else 'None'}")

        if test["expected_rule_id"]:
            passed = (
                test["expected_rule_id"] in fired_ids
                and test["expected_fact"] in result["inferred_facts"]
            )
        else:
            # Negative test: expected 0 fired rules
            passed = len(fired_ids) == 0

        status = "PASSED" if passed else "FAILED"
        print(f"    Result: >>> {status} <<<")
        if not passed:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL STANDALONE TESTS PASSED SUCCESSFULLY! (4/4)")
    else:
        print("SOME TESTS FAILED! PLEASE REVIEW RULES.")
    print("=" * 70)
    return all_passed


if __name__ == "__main__":
    run_standalone_tests()
