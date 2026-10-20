"""
app.py
======
Medical Expert System Using Rule-Based Inference
College AI Mini-Project - Streamlit User Interface

Key Features:
- Interactive symptom checklist
- Forward chaining rule execution via `inference_engine.py`
- Step-by-step reasoning audit trail (Explanation Facility)
- Preset demo cases for viva presentations
- Reset button to clear all inputs
- Comprehensive educational disclaimers and safety notices
"""

import streamlit as st
from inference_engine import load_knowledge_base, run_forward_chaining

# Set Streamlit page configuration
st.set_page_config(
    page_title="Medical Expert System | AI Mini-Project",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 1. LOAD KNOWLEDGE BASE (Cached for performance)
# -----------------------------------------------------------------------------
@st.cache_data
def get_kb():
    return load_knowledge_base("rules.json")

kb = get_kb()
symptoms_dict = kb.get("symptoms_dictionary", {})

# -----------------------------------------------------------------------------
# 2. SESSION STATE MANAGEMENT (For Reset and Presets)
# -----------------------------------------------------------------------------
# Preset scenarios designed for quick viva presentations
PRESET_CASES = {
    "-- Custom Selection --": [],
    "Demo 1: Common Cold / Rhinitis Pattern (R3)": ["runny_nose", "sore_throat", "cough"],
    "Demo 2: Multi-Step Chaining - Flu-like Presentation (R1 -> R2 -> R6)": ["fever", "cough", "sore_throat", "fatigue"],
    "Demo 3: Gastrointestinal Pattern (R4)": ["nausea", "vomiting"],
    "Demo 4: Urgent Alert - Breathing Difficulty (R1 -> R7)": ["fever", "cough", "shortness_of_breath"],
    "Demo 5: Emergency Alert - Chest Pain (R8)": ["chest_pain"],
    "Demo 6: Negative Case - No Rule Matches": ["runny_nose"]
}

# Initialize session state for symptoms
for symptom_key in symptoms_dict.keys():
    if symptom_key not in st.session_state:
        st.session_state[symptom_key] = False

if "selected_preset" not in st.session_state:
    st.session_state["selected_preset"] = "-- Custom Selection --"


def apply_preset():
    """Applies the symptoms defined in the chosen preset demo."""
    chosen = st.session_state["selected_preset"]
    target_symptoms = PRESET_CASES.get(chosen, [])
    for symptom_key in symptoms_dict.keys():
        st.session_state[symptom_key] = symptom_key in target_symptoms


def reset_all():
    """Resets all symptom checkboxes and preset selection."""
    st.session_state["selected_preset"] = "-- Custom Selection --"
    for symptom_key in symptoms_dict.keys():
        st.session_state[symptom_key] = False


# -----------------------------------------------------------------------------
# 3. SIDEBAR: PROJECT INFO & VIVA CONCEPTS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("🎓 AI Project Details")
    st.caption("**Topic:** Rule-Based Expert Systems")
    st.caption("**Inference Method:** Forward Chaining")
    
    st.markdown("---")
    st.subheader("💡 Viva Quick Guide")
    st.markdown(
        """
        - **Knowledge Base (KB):** Explicit IF-THEN rules stored in `rules.json`.
        - **Working Memory:** Currently known facts (user symptoms + newly inferred facts).
        - **Inference Engine:** Evaluates rule conditions in cycles until no more rules can fire.
        - **Explanation Facility:** Provides the reasoning trail showing which rule fired and why.
        """
    )
    
    st.markdown("---")
    st.subheader("🧪 Quick Viva Demos")
    st.selectbox(
        "Load a Test Case:",
        options=list(PRESET_CASES.keys()),
        key="selected_preset",
        on_change=apply_preset,
        help="Select a predefined combination to quickly demonstrate to an examiner."
    )
    
    st.button("🔄 Reset All Inputs", on_click=reset_all, use_container_width=True)


# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
st.title("🩺 Medical Expert System")
st.markdown("### *Demonstrating Rule-Based AI and Forward Chaining*")

# Mandatory Educational Disclaimer Banner
st.warning(
    """
    ⚠️ **EDUCATIONAL DEMONSTRATION ONLY**  
    This system is an academic artificial intelligence project built strictly for educational purposes 
    to demonstrate explicit IF-THEN rule evaluation and forward chaining.  
    - **It does NOT provide medical diagnosis or clinical evaluations.**
    - **It does NOT recommend medications or treatment plans.**
    - If you or someone you know is experiencing real symptoms, consult a qualified medical professional. 
      For severe symptoms or emergencies, call local emergency services immediately.
    """
)

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. SYMPTOM SELECTION (CHECKLIST)
# -----------------------------------------------------------------------------
st.subheader("1. Select Patient Symptoms (Working Memory Input)")
st.write("Check the symptoms observed in the patient to populate the initial Fact Base:")

# Display checkboxes neatly in three columns
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

symptom_items = list(symptoms_dict.items())
for idx, (symp_key, symp_label) in enumerate(symptom_items):
    col = columns[idx % 3]
    col.checkbox(
        label=symp_label,
        key=symp_key
    )

# Collect selected symptoms
selected_symptoms = [key for key in symptoms_dict.keys() if st.session_state[key]]

st.markdown("---")

# Action Buttons
btn_col1, btn_col2 = st.columns([1, 4])
with btn_col1:
    run_clicked = st.button("🚀 Run Inference", type="primary", use_container_width=True)
with btn_col2:
    st.button("🧹 Clear Selections", on_click=reset_all)

# -----------------------------------------------------------------------------
# 6. INFERENCE EXECUTION & RESULTS
# -----------------------------------------------------------------------------
if run_clicked:
    if not selected_symptoms:
        st.info("ℹ️ Please select at least one symptom from the checklist to run the inference engine.")
    else:
        # Execute Forward Chaining
        result = run_forward_chaining(kb, selected_symptoms)
        
        st.markdown("---")
        st.subheader("2. Inference Engine Results")

        # Top summary metrics
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Initial Symptoms", len(result["initial_facts"]))
        m_col2.metric("Rules Fired", result["rules_fired_count"])
        m_col3.metric("New Facts Inferred", len(result["inferred_facts"]))
        m_col4.metric("Inference Cycles", result["total_cycles"])

        # Urgent / Red-Flag Alert Notice
        if result["has_urgent_alert"]:
            st.error(
                """
                🚨 **CRITICAL ADVISORY (Rule-Generated Alert)**:  
                One or more rules flagged symptoms (e.g., chest pain or breathing difficulty) 
                that require **prompt emergency clinical medical attention**.  
                *Always seek immediate professional healthcare in emergency situations.*
                """
            )

        # 6A. Handle case where NO rules matched
        if not result["matched"]:
            st.info(
                """
                🔍 **No Predefined Rule Matched**:  
                The combination of selected symptoms did not satisfy the conditions of any explicit 
                IF-THEN rule in the knowledge base.

                **AI Note for Viva:**  
                In a classical rule-based expert system, the engine does not guess, hallucinate, or invent 
                conclusions. If no rule's antecedent is met, the system safely reports that no conclusion 
                can be derived.
                """
            )
        else:
            # 6B. Display Inferred Conclusions
            st.markdown("#### 📋 Inferred Conclusions (Consequents)")
            for concl in result["final_conclusions"]:
                alert_icon = "🚨" if concl.get("is_urgent") else "📌"
                with st.container():
                    st.markdown(
                        f"""
                        > **{alert_icon} {concl['rule_id']}: {concl['rule_name']}**  
                        > **Conclusion:** {concl['conclusion_text']}  
                        > *Rule Context:* {concl['explanation']}
                        """
                    )

            # 6C. Explanation Facility (Step-by-Step Reasoning Trace)
            st.markdown("#### 🔬 Explanation Facility (Forward Chaining Execution Trace)")
            st.caption(
                "This trace demonstrates how the inference engine applied data-driven forward chaining across cycles."
            )

            for step_num, rule_exec in enumerate(result["fired_rules"], start=1):
                rule_id = rule_exec["rule_id"]
                rule_name = rule_exec["rule_name"]
                cycle = rule_exec["cycle"]
                conditions = ", ".join([f"`{c}`" for c in rule_exec["matched_conditions"]])
                produced = f"`{rule_exec['conclusion_fact']}`"

                with st.expander(f"Step {step_num}: Cycle {cycle} ➔ Rule [{rule_id}] Fired: {rule_name}", expanded=True):
                    st.write(f"- **IF (Antecedent Conditions Satisfied):** {conditions}")
                    st.write(f"- **THEN (Consequent Fact Asserted):** {produced}")
                    st.write(f"- **Explanation:** {rule_exec['explanation']}")
                    if rule_exec.get("is_intermediate"):
                        st.info("ℹ️ *This is an intermediate fact used to chain into subsequent rules.*")

        # ---------------------------------------------------------------------
        # 7. SAFETY & MEDICAL ETHICS GUIDANCE
        # ---------------------------------------------------------------------
        st.markdown("---")
        st.subheader("3. Safety & General Health Guidance")
        st.markdown(
            """
            - **Professional Consultation:** Always consult a licensed physician or healthcare specialist for any medical symptoms or diagnosis.
            - **No Self-Medication:** This software does not provide medication recommendations, dosages, or treatment protocols.
            - **Emergency Care:** If you experience severe chest pain, extreme shortness of breath, sudden numbness, or loss of consciousness, seek immediate emergency medical services.
            """
        )

# -----------------------------------------------------------------------------
# 8. FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Medical Expert System | Built with Python & Streamlit | College Artificial Intelligence Mini-Project Demonstration"
)
