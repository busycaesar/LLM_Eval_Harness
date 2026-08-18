from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tqdm.auto import tqdm

from eval import run_evaluation, analyze_results, get_table_from_results, store_results
from dataset import get_dataset, DATASET, get_prompt_for_data, extract_prediction, LETTERS
from llm import infer_llm, MODEL

dataset = get_dataset(10)
prompts = [get_prompt_for_data(row) for row in dataset]
correct_answers = [LETTERS[row["answer"]] for row in dataset]

# ex.map needs a list for each argument the function takes. Since extract_prediction and infer_llm don't change per row, we lock them in with partial. ex.map then only loops over the three per-row lists (dataset, prompts, correct_answers).
evaluate = partial(run_evaluation, extract_prediction=extract_prediction, infer_llm=infer_llm)

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(tqdm(ex.map(evaluate, dataset, prompts, correct_answers), total=len(dataset)))

results_table = get_table_from_results(results)

store_results(f"eval_results/results_{MODEL.replace('/', '_')}.csv", results_table)

analyze_results(results_table, MODEL, DATASET)