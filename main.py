from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tqdm.auto import tqdm

from eval import run_evaluation, analyze_results, get_table_from_results, store_results
from dataset import MMLUDataset
from llm import AnthropicProvider

provider = AnthropicProvider(model="claude-sonnet-5")
dataset = MMLUDataset(sample_size=10)

rows = dataset.load()
metadatas = [dataset.metadata(row) for row in rows]
prompts = [dataset.prompt_for(row) for row in rows]
correct_answers = [dataset.correct_answer(row) for row in rows]

# ex.map needs a list for each argument the function takes. Since extract_prediction and infer
# don't change per row, we lock them in with partial. ex.map then only loops over the three per-row
# lists (metadatas, prompts, correct_answers).
evaluate = partial(run_evaluation, extract_prediction=dataset.extract_prediction, infer_llm=provider.infer)

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(tqdm(ex.map(evaluate, metadatas, prompts, correct_answers), total=len(rows)))

results_table = get_table_from_results(results)

store_results(f"eval_results/results_{provider.model_name.replace('/', '_')}.csv", results_table)

analyze_results(results_table, provider.model_name, dataset.name)