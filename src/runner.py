from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tqdm.auto import tqdm
from eval import run_evaluation, analyze_results, get_table_from_results, store_results
from dataset import get_dataset
from llm import get_llm

def run(provider: str, model: str, dataset_name: str, sample_size: int):
    data_source = get_dataset(dataset_name, sample_size)
    llm = get_llm(provider, model, data_source.max_tokens)

    rows = data_source.load()
    metadatas = [data_source.metadata(dataset) for dataset in rows]
    prompts = [data_source.prompt_for(dataset) for dataset in rows]
    correct_answers = [data_source.correct_answer(dataset) for dataset in rows]

    # ex.map needs a list for each argument that the function takes. Since extract_prediction and infer don't change per dataset, we lock them in with partial. ex.map then only loops over the three per-dataset lists (metadatas, prompts, correct_answers).
    evaluate = partial(
        run_evaluation,
        extract_prediction=data_source.extract_prediction,
        infer_llm=llm.infer,
        is_correct=data_source.is_correct,
    )

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(tqdm(ex.map(evaluate, metadatas, prompts, correct_answers), total=len(rows)))

    results_table = get_table_from_results(results)

    store_results(f"eval_results/results_{llm.model_name.replace('/', '_')}.csv", results_table)

    analyze_results(results_table, llm.model_name, data_source.name)