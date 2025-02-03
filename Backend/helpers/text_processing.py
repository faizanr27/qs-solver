import re

def extract_questions(text):
    """
    Extracts potential questions from the given text using an expanded set of patterns.
    """
    question_patterns = [
        r'^\d+\.',  # Matches: 1. 2. 3.
        r'^\(?[Qq]\d+\)?',  # Matches: Q1, (Q2), Q3
        r'^\d+\)',  # Matches: 1) 2) 3)
        r'^[ivxlcdm]+\.',  # Matches: i. ii. iii. iv. (Roman numerals)
        r'^[a-zA-Z]\.',  # Matches: a. b. c. d.
        r'^[ivxlcdm]+\)',  # Matches: i) ii) iii) iv) (Roman numerals)
        r'^[a-zA-Z]\)',  # Matches: a) b) c) d)
    ]

    # Common question starters (customizable for better matching)
    question_starters = [
        "What", "Why", "How", "Explain", "Define", "Describe", "List", "Discuss", "Compare", "Differentiate",
    "State", "Prove", "Show", "Derive", "Illustrate", "Analyze", "Evaluate", "Summarize", "Outline",
    "Justify", "Examine", "Identify", "Interpret", "Criticize", "Contrast", "Assess", "Construct",
    "Predict", "Demonstrate", "Solve", "Elaborate", "Clarify", "Enumerate"
    ]

    # Create a regex pattern for question starters
    question_starters_pattern = rf"^({'|'.join(question_starters)})\b"
    question_patterns.append(question_starters_pattern)

    # Combine all patterns into one regex
    combined_pattern = re.compile("|".join(question_patterns), re.MULTILINE)

    # Split text into lines and filter only questions
    lines = text.split('\n')
    questions = [line.strip() for line in lines if combined_pattern.search(line.strip())]

    return questions
