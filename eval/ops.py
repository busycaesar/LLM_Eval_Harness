import time

def call_model(prompt, infer_llm, retries=4):
    for attempt in range(retries):
        try:
            return infer_llm(prompt)
        except Exception as e:
            if attempt == retries - 1:
                return f"ERROR: {e}"
            time.sleep(2 ** attempt)

def run_evaluation(data, prompt, correct_answer, extract_prediction, infer_llm):
    raw_response = call_model(prompt, infer_llm)
    prediction = extract_prediction(raw_response)

    return {
        "subject": data["subject"],
        "question": data["question"],
        "raw_response": raw_response,
        "prediction": prediction,
        "correct_answer": correct_answer,
        "accurate": prediction == correct_answer,
    }

def store_results(path, results_table):
    results_table.to_csv(path, index=False)
