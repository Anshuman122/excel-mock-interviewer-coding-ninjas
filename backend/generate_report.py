from .llm_rubric import evaluate_answer
from .excel_tests import validate_excel

def generate_report(text_answer, rubric, excel_file_path=None):
    text_eval = evaluate_answer(text_answer, rubric)

    excel_eval = None
    if excel_file_path:
        try:
            excel_eval = validate_excel(excel_file_path)
        except Exception as e:
            excel_eval = {"error": f"Failed to validate excel: {e}"}

    # Combine
    report = {
        "text_eval": text_eval,
        "excel_eval": excel_eval
    }

    return report