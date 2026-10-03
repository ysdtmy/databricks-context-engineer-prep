# generate_all_data.py
import json
import os
from build_rich_guide import RICH_GUIDE_CHAPTERS
from build_data import cheatsheets
from questions_d1 import D1_QUESTIONS
from questions_d2 import D2_QUESTIONS
from questions_d3 import D3_QUESTIONS
from questions_d4 import D4_QUESTIONS
from questions_d567 import D567_QUESTIONS
from questions_drill import DRILL_QUESTIONS
from questions_missed import MISSED_QUESTIONS

# Assemble all 70 questions
all_70 = D1_QUESTIONS + D2_QUESTIONS + D3_QUESTIONS + D4_QUESTIONS + D567_QUESTIONS
print(f"Total structured questions: {len(all_70)}")

# First 45 are Full Mock Exam (Q1 - Q45)
mock_questions = []
for idx, q in enumerate(all_70[:45]):
    q_copy = dict(q)
    q_copy["id"] = f"Q{idx + 1}"
    q_copy["num"] = idx + 1
    q_copy["type"] = "mock"
    mock_questions.append(q_copy)

# Remaining 25 are Practice / Domain Specific (D1 - D25)
practice_questions = []
for idx, q in enumerate(all_70[45:]):
    q_copy = dict(q)
    q_copy["id"] = f"D{idx + 1}"
    q_copy["num"] = idx + 1
    q_copy["type"] = "practice"
    practice_questions.append(q_copy)

exam_data = {
    "guideChapters": RICH_GUIDE_CHAPTERS,
    "cheatsheets": cheatsheets,
    "mockQuestions": mock_questions,
    "practiceQuestions": practice_questions,
    "drillQuestions": DRILL_QUESTIONS,
    "reviewQuestions": MISSED_QUESTIONS
}

js_content = "/**\n * Databricks Certified Context Engineer Associate - Complete Exam Data\n * English Questions & Options, In-Depth Japanese Explanations, Rich Study Guide\n */\n"
js_content += "window.EXAM_DATA = " + json.dumps(exam_data, ensure_ascii=False, indent=2) + ";\n"

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.js")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Successfully generated data.js ({len(mock_questions)} mock + {len(practice_questions)} practice + {len(DRILL_QUESTIONS)} drill = {len(mock_questions) + len(practice_questions) + len(DRILL_QUESTIONS)} questions, {len(RICH_GUIDE_CHAPTERS)} rich chapters)")
