# Medical Expert System Using Rule-Based Inference

An educational Artificial Intelligence college mini-project demonstrating classical rule-based expert systems using **Python** and **Streamlit**.

---

> ⚠️ **Educational & Safety Disclaimer**  
> This project is designed **strictly for academic and demonstration purposes** to illustrate classical AI reasoning (Knowledge Bases, Working Memory, and Forward Chaining).  
> - It does **NOT** provide medical diagnosis or clinical decision-making.  
> - It does **NOT** prescribe medications or treatments.  
> - Symptom patterns demonstrated in rules are simplified textbook examples and must not be used for real healthcare decisions. For real medical concerns, always consult a qualified healthcare professional. For medical emergencies, contact emergency services immediately.

---

## 📌 Project Overview

An **Expert System** is a foundational branch of Artificial Intelligence designed to emulate human expert decision-making using formalized domain knowledge.

This project implements:
1. **Knowledge Base (KB):** Predefined IF-THEN rules stored in `rules.json`.
2. **Working Memory (Fact Base):** Dynamic storage for known facts (initially patient symptoms, expanded with inferred facts).
3. **Inference Engine (Forward Chaining):** Data-driven reasoning that evaluates rule conditions, fires matching rules, asserts new facts into working memory, and continues across multiple cycles until a fixed point is reached.
4. **Explanation Facility:** A step-by-step audit trail showing which rules fired, their conditions, and why a conclusion was drawn.
5. **Interactive UI:** A simple, clean web interface built with Streamlit including viva presets and a reset feature.

---

## 📁 Project Structure

```text
Medical-expert-system-miniproject/
├── app.py                # Streamlit user interface & visualization
├── inference_engine.py   # Forward chaining engine & standalone test suite
├── rules.json            # Knowledge base with explicit IF-THEN rules
├── requirements.txt      # Project dependencies (Streamlit)
└── README.md             # Project documentation & viva explanation
```

---

## 🛠️ Technology Stack

- **Language:** Python 3.x
- **User Interface:** Streamlit
- **Data Storage:** JSON (human-readable Knowledge Base)
- **External Dependencies:** No complex ML models, databases, or external APIs.

---

## 🚀 Setup & Execution

### 1. Install Dependencies
Ensure you have Python installed, then install Streamlit:
```bash
pip install -r requirements.txt
```

### 2. Run Standalone Inference Engine Tests
You can verify the rule-based inference engine independently of the user interface:
```bash
python inference_engine.py
```
This runs automated test cases for single-step inference, multi-step forward chaining, emergency rules, and negative (no-match) cases.

### 3. Launch the Web Application
Start the Streamlit application:
```bash
python -m streamlit run app.py
```
The app will open automatically in your browser (usually at `http://localhost:8501`).

---

## 🎓 Viva Guide & AI Concepts Explained

| Concept | Explanation in this Project |
| :--- | :--- |
| **Knowledge Base (KB)** | Represented in `rules.json`. Each rule contains an antecedent (`if_all`) and a consequent (`then_add`). |
| **Working Memory** | A Python set tracking current known facts. It begins with user-selected symptoms and dynamically expands as rules fire. |
| **Forward Chaining** | Data-driven inference: starts from known facts and applies rules to deduce new facts until no further rules can fire. |
| **Multi-Step Chaining** | Example: Rule `R1` fires from `fever + cough` to produce `respiratory_involvement`. In the next cycle, `R2` fires from `respiratory_involvement + sore_throat` to produce `upper_respiratory_pattern`. |
| **Explanation Facility** | Explains *how* and *why* conclusions were reached, fulfilling a key requirement of classical expert systems. |
| **Handling No-Match** | If no rule conditions are satisfied, the system safely reports that no rule matched instead of hallucinating answers. |

---

## 🧪 Quick Test Scenarios for Demonstration

1. **Multi-Step Chaining Demo:** Select `Fever`, `Cough`, `Sore Throat`, and `Fatigue`.
   - *Result:* Cycle 1 fires `R1`, Cycle 2 fires `R2`, Cycle 3 fires `R6` (demonstrating true multi-cycle forward chaining).
2. **Gastrointestinal Pattern:** Select `Nausea` and `Vomiting`.
   - *Result:* Fires Rule `R4`.
3. **Emergency Alert Flag:** Select `Chest Pain`.
   - *Result:* Fires Rule `R8` (Critical Red-Flag Advisory).
4. **Negative Case:** Select only `Runny or Stuffy Nose`.
   - *Result:* Safe notification that no predefined rule matched the selected symptoms.
