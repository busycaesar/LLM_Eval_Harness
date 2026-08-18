import pandas

def get_table_from_results(results):
    return pandas.DataFrame(results)

def analyze_results(results_table, model, dataset):
    accuracy = results_table["accurate"].mean()
    # Counts rows where the prediction is not present maybe due to failed LLM call or no valid answer present in the response.
    unparsed_responses = results_table["prediction"].isna().sum()
    # Counts rows where the LLM call failed.
    errors = results_table["raw_response"].str.startswith("ERROR:").sum()

    print(f"Model:      {model}")
    print(f"Dataset:    {dataset}")
    print(f"Items:      {len(results_table)}")
    print(f"Accuracy:   {accuracy:.3f}")
    print(f"Unparsed:   {unparsed_responses}")
    print(f"API errors: {errors}")