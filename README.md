# AI Security Evaluation Framework

**Current version V5**

A Python-based framework for evaluating the security behaviour of Large Language Models (LLMs) against adversarial and security-focused test cases.

The framework currently uses **Ollama and Qwen 2.5 3B** as the target model and provides a foundation for progressively more sophisticated LLM evaluation techniques, including deterministic evaluation, LLM-as-a-Judge, model evaluation platforms, observability, and agent security testing.
---
## Objective

The objective of this project is to build a practical **LLM security evaluation capability** that can:

* Execute repeatable security test cases against an LLM
* Evaluate model responses against defined security criteria
* Identify failures in model security behaviour
* Measure results by security category
* Produce structured evaluation results
* Progress from deterministic evaluation to LLM-based evaluation
* Extend into AI agent and tool-use security testing

The framework is being developed with a focus on **AI security, model evaluation, adversarial testing, and agentic AI security**.

---

## Architecture

The current evaluation flow is:

```text
                    ┌──────────────────┐
                    │   Test Dataset   │
                    │    dataset.json  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Target Model   |
                    |   list (default  │
                    │   Qwen 2.5 3B)   │
                    │     via Ollama   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Model Response   │
                    └────────┬─────────┘
                             |
                             |                            
                             ▼                            
                    ┌──────────────────┐         ┌──────────────────┐    
                    │                  │         |                  |
                    │ Evaluators       |-------->| LLM as Judge     |
                    | Deterministic    |         |                  |
                    | Rules            │         |                  |
                    └────────┬─────────┘         └────────┬─────────┘
                                                          |
                                                          |
                    ┌──────────────────┐                  |
                    │ PASS / FAIL      │<-----------------|
                    │ + Reason         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   results.json   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Category Metrics │
                    └──────────────────┘
```                          │
                             ▼
                    ┌──────────────────┐
                    │ LLM Judge vs     |
                    | Evaluator        |
                    | Comparison       |
                    └──────────────────┘


## Version build plan

V1:	Qwen + dataset + responses	Python + Ollama
V2:	One deterministic evaluator	Evaluation fundamentals
V3:	Multi-category evaluator + reasons + metrics Evaluation framework architecture
V4: Code refactoring, and enabling evals for multiple models 
V5:	<We are here> LLM-as-a-Judge	LLM evaluation methodology
V6:	Promptfoo	Industry evaluation tooling
V7:	Phoenix	Observability + tracing
V8:	Agent + mock tools	Agent evaluation
V9:	Agent security testing	Tool abuse, excessive agency, identity
V10:	Security eval pipeline	CI/CD + regression testing