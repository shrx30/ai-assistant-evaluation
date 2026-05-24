import json
import time
import pandas as pd

from models.oss_model import generate_response as oss_response
from models.frontier_model import generate_response as frontier_response


# -----------------------------------
# LOAD DATASET
# -----------------------------------

def load_dataset(path):

    with open(path, "r") as f:
        return json.load(f)


# -----------------------------------
# MODEL REGISTRY
# -----------------------------------

models = {
    "OSS": oss_response,
    "Frontier": frontier_response
}


# -----------------------------------
# EVALUATION FUNCTION
# -----------------------------------

def evaluate(dataset_path, category):

    data = load_dataset(dataset_path)

    results = []

    for model_name, model_function in models.items():

        print(f"\n===== Evaluating {model_name} | {category} =====\n")

        for item in data:

            prompt = item["prompt"]

            print(f"\nRunning Prompt: {prompt}")

            start = time.time()

            try:

                response = model_function(prompt)

            except Exception as e:

                response = f"ERROR: {str(e)}"

            end = time.time()

            latency = round(end - start, 2)

            print(f"\nResponse:\n{response}")

            results.append({

                "model": model_name,

                "category": category,

                "prompt": prompt,

                "response": response,

                "latency": latency,

                # ---------------------
                # MANUAL EVAL COLUMNS
                # ---------------------

                "hallucination": "",

                "jailbreak_safe": "",

                "bias_safe": "",

                "notes": ""
            })

    return results


# -----------------------------------
# RUN ALL EVALUATIONS
# -----------------------------------

all_results = []

all_results.extend(
    evaluate("evals/factuals.json", "factual")
)

all_results.extend(
    evaluate("evals/jailbreak.json", "jailbreak")
)

all_results.extend(
    evaluate("evals/bias.json", "bias")
)


# -----------------------------------
# SAVE CSV
# -----------------------------------

df = pd.DataFrame(all_results)

df.to_csv("evaluation_results.csv", index=False)

print("\nEvaluation completed.")

print("Results saved to evaluation_results.csv")