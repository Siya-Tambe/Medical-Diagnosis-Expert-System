# Medical Expert System Using Rule-Based Inference

## About the Project
The **Medical Expert System** is a mini-project developed using Python and Streamlit to demonstrate the working of a rule-based Artificial Intelligence system.

It accepts user-selected symptoms and applies predefined IF–THEN rules using **Forward Chaining** to generate educational conclusions. It also displays the rules fired, inferred facts, and an explanation of the reasoning process.

**Note:** This project is strictly for educational purposes. It does not provide medical diagnosis or treatment recommendations.

## Features
- Interactive symptom selection interface
- Rule-based knowledge base stored in JSON
- Forward-chaining inference engine
- Explanation of fired rules and inferred facts
- Predefined demonstration test cases
- No-rule-matched handling
- Safety warnings for selected urgent symptoms
- Reset functionality

## Technologies Used
- Python
- Streamlit
- JSON
- Python standard libraries

## Project Structure

```text
Medical-expert-system-miniproject/
├── app.py
├── inference_engine.py
├── rules.json
├── requirements.txt
├── README.md
└── .venv/   # Local virtual environment (not required in GitHub)
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Medical-expert-system-miniproject
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser, usually at `http://localhost:8501`.

## How It Works

1. The user selects symptoms from the interface.
2. The selected symptoms are stored as initial facts.
3. The inference engine evaluates the rules in `rules.json`.
4. Matching rules fire and add new facts to working memory.
5. Forward chaining continues until no new facts can be inferred.
6. The application displays the conclusions, fired rules, and reasoning trace.

## AI Concepts Demonstrated
- Expert Systems
- Knowledge Representation
- IF–THEN Rules
- Working Memory
- Inference Engine
- Forward Chaining
- Explanation Facility

## Limitations
- Uses predefined educational rules.
- Does not use machine learning or a trained model.
- Does not connect to external medical databases or APIs.
- Has not been established as a clinically validated diagnostic system.

## Disclaimer
This application is intended only for academic demonstration of rule-based Artificial Intelligence. It must not be used for medical diagnosis, treatment decisions, or emergencies. Consult a qualified healthcare professional for medical concerns.

## Author
Developed as a college Artificial Intelligence mini-project.
