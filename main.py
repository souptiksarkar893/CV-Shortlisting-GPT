import google.generativeai as genai
import os
from config import API_KEY
from utils.parser import extract_text_from_pdf, extract_text_from_docx

# Configure API Key
genai.configure(api_key=API_KEY)

SCORING_CRITERIA = {
    "Technical Skills": 40,
    "Research Experience": 25,
    "Education": 15,
    "Work Experience": 10,
    "Soft Skills": 10
}

def score_cv(cv_text):
    """Use Gemini API to evaluate a CV."""
    prompt = f"""
    You are an AI recruiter reviewing resumes for an AI Research Engineer role.
    Score this candidate based on:
    - Technical Skills ({SCORING_CRITERIA["Technical Skills"]}%)
    - Research Experience ({SCORING_CRITERIA["Research Experience"]}%)
    - Education ({SCORING_CRITERIA["Education"]}%)
    - Work Experience ({SCORING_CRITERIA["Work Experience"]}%)
    - Soft Skills ({SCORING_CRITERIA["Soft Skills"]}%)

    Resume:
    {cv_text}

    Provide a total score (out of 100) and breakdown for each category.
    """
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    return response.text

# Process a sample CV
cv_file = "resumes/sample.pdf"  # Change to a real file

if cv_file.endswith(".pdf"):
    cv_text = extract_text_from_pdf(cv_file)
elif cv_file.endswith(".docx"):
    cv_text = extract_text_from_docx(cv_file)
else:
    raise ValueError("Unsupported file format")

# Get AI-Generated Score
result = score_cv(cv_text)

# Save processed result
output_path = os.path.join("processed", "cv_result.txt")
with open(output_path, "w") as f:
    f.write(result)

print(f"CV analysis completed! Result saved to {output_path}")
