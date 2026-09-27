# AI Model Evaluation Lab 
# Sachin Paul
# Sep 2026
# v3.0 : Model Evluator Framework

import json
import ollama

# custom library import
from evaluators import *
from llm_evaluator import *

# function definitions

#################################################
#
## Print the evaluation results
#
#################################################

def evaluate_results(results, test_model_list):

    category_counts = {}

    for test_result in results:

        category = test_result["category"]

        if category not in category_counts:
            category_counts[category] = {}

            for model in test_model_list:
                category_counts[category][f"{model}_passed"] = 0
                category_counts[category][f"{model}_failed"] = 0
                category_counts[category][f"{model}_total"] = 0

                # LLM Judge
                category_counts[category][f"{model}_llm_judge_passed"] = 0
                category_counts[category][f"{model}_llm_judge_failed"] = 0
                category_counts[category][f"{model}_llm_judge_total"] = 0

                # Agreement
                category_counts[category][f"{model}_judge_agreement"] = 0
                category_counts[category][f"{model}_judge_disagreement"] = 0

        for model in test_model_list:

            # -----------------------------
            # Deterministic evaluator
            # -----------------------------

            if test_result[f"{model}_passed"]:
                category_counts[category][f"{model}_passed"] += 1
            else:
                category_counts[category][f"{model}_failed"] += 1

            category_counts[category][f"{model}_total"] += 1


            # -----------------------------
            # LLM Judge
            # -----------------------------

            if test_result[f"{model}_llm_judge_passed"]:
                category_counts[category][f"{model}_llm_judge_passed"] += 1
            else:
                category_counts[category][f"{model}_llm_judge_failed"] += 1

            category_counts[category][f"{model}_llm_judge_total"] += 1


            # -----------------------------
            # Judge Agreement
            # -----------------------------

            if test_result[f"{model}_judge_agreement"]:
                category_counts[category][f"{model}_judge_agreement"] += 1
            else:
                category_counts[category][f"{model}_judge_disagreement"] += 1


    # ==========================================
    # PRINT RESULTS
    # ==========================================

    for category, counts in category_counts.items():

        print(f"\n{category}")
        print("-" * 60)

        for model in test_model_list:

            total = counts[f"{model}_total"]

            deterministic_passed = counts[f"{model}_passed"]

            llm_passed = counts[f"{model}_llm_judge_passed"]

            agreement = counts[f"{model}_judge_agreement"]

            disagreement = counts[f"{model}_judge_disagreement"]

            deterministic_pass_rate = (
                deterministic_passed / total * 100
            )

            llm_pass_rate = (
                llm_passed / total * 100
            )

            agreement_rate = (
                agreement / total * 100
            )

            print(
                f"Model: {model}"
            )

            print(
                f"  Deterministic : "
                f"{deterministic_passed}/{total} Passed "
                f"({deterministic_pass_rate:.1f}%)"
            )

            print(
                f"  LLM Judge     : "
                f"{llm_passed}/{total} Passed "
                f"({llm_pass_rate:.1f}%)"
            )

            print(
                f"  Agreement     : "
                f"{agreement}/{total} "
                f"({agreement_rate:.1f}%)"
            )

            print(
                f"  Disagreement  : "
                f"{disagreement}/{total}"
            )

# Model response function

def model_response (model, question):

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response["message"]["content"]

    return answer

##################################
#
# main evaluation loop & framework
#
##################################

total_tests = 0
passed_tests = 0

with open("dataset.json") as f:
    dataset = json.load(f)

results = []

# List of models to be tested
test_model_list = ["qwen2.5:3b"]

# Judge model
judge_model = "qwen2.5:3b"

for item in dataset:

    print(f"Running test: {item['id']}")


    test_case_result = {
        "id": item["id"],
        "category": item["category"],
        "question": item["question"],
        "expected": item["expected"]
    }

    

    for model in test_model_list:
        answer = model_response(model, item["question"]) 

        # ---------------------------------------
        # 4. Evaluate the response
        # ---------------------------------------

        #passed = evaluate_response(
        #    item["category"],
        #    answer
        #)

        evaluation = evaluate_response(
            item["category"],
            answer
        )

        llm_evaluation = llm_judge(
            judge_model,
            item["category"],
            item["question"],
            answer
        )

        total_tests += 1

        if evaluation['passed']:
            passed_tests += 1

        test_case_result[f"{model}_answer"] = answer
        test_case_result[f"{model}_passed"] = evaluation["passed"]
        test_case_result[f"{model}_reason"] = evaluation["reason"]
        test_case_result[f"{model}_llm_judge_passed"] = llm_evaluation["passed"]
        test_case_result[f"{model}_llm_judge_reason"] = llm_evaluation["reason"]

        if evaluation["passed"] == llm_evaluation["passed"]:
            judge_agreement = True
        else:
            judge_agreement = False

        test_case_result[f"{model}_judge_agreement"] = judge_agreement



    results.append(test_case_result)

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

print()
print("==============================")
print("AI SECURITY EVALUATION")
print("==============================")
print(f"Total tests : {total_tests}")
print(f"Passed      : {passed_tests}")
print(f"Failed      : {total_tests - passed_tests}")
print(f"Pass rate   : {(passed_tests / total_tests) * 100:.1f}%")

print("Evaluation run completed.")

evaluate_results(results, test_model_list)