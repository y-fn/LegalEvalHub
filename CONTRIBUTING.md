# Contributing to LegalEvalHub

Thank you for your interest in contributing to **LexEval**, a community-driven platform for evaluating large language models (LLMs) on legal tasks.

You can contribute in two primary ways:
1. Submitting a **new task**
2. Submitting an **evaluation run** for an existing task

All contributions are made via pull requests to this GitHub repository. If you would like to contribute via alternative means, please reach out to <a href="mailto:nguha@cs.stanford.edu">nguha@cs.stanford.edu</a>.


## 🧩 Submitting a New Task

To add a new evaluation task to LexEval:

1. Create a JSON file at `tasks/<task_id>.json`
2. Follow the format below.
3. Open a pull request with a description of the task.

The task JSON file should have the following format:

```json
{
  "task_id": "stat_interp_v2",
  "name": "Statutory Interpretation v2",
  "family": "LegalBench",
  "short_description": "Binary classification task using federal court rulings.",
  "long_description": "Binary classification task using federal court rulings.",
  "dataset_url": "https://example.com/stat_interp_v2.csv",
  "num_samples": 500,
  "tags": ["statutory interpretation", "legal reasoning"],
  "document_type": "judicial opinion",
  "min_input_length": 100,
  "max_input_length": 1000,
  "metrics": [
    {"name": "accuracy", "direction": "maximize"},
    {"name": "f1", "direction": "maximize"}
  ],
  "contributed_by_name": "Your Name",
  "contributed_by_email": "your.name@institution.edu",
  "paper_url": "https://example.com/paper.pdf",
  "paper_title": "Paper Title",
  "paper_authors": ["Author 1", "Author 2"]
}
```

Some notes:
- `task_id` should be a unique identifier for the task.
- `name` should be a short name for the task.
- `family` (optional) should be the name of the task family or benchmark suite (e.g., "LegalBench", "ContractBench"). Tasks from the same family will be grouped together in the interface.
- `short_description` should be a short description of the task.
- `long_description` should be a long description of the task.
- `dataset_url` should be the URL of the dataset.
- `num_samples` should be the number of samples in the dataset.
- `tags` should be a list of tags for the task.
- `document_type` should be the type of document that the task is about.
- `min_input_length` should be the length of the shortest input in the dataset (measured in Llama-3 tokens).
- `max_input_length` should be the length of the longest input in the dataset (measured in Llama-3 tokens).
- `metrics` should be a list of metrics to evaluate the model on.
- `contributed_by_name` should be your name
- `contributed_by_email` should be your email
- `paper_url` should be the URL of the paper that describes the task.
- `paper_title` should be the title of the paper that describes the task.
- `paper_authors` should be a list of authors of the paper that describes the task.


## 📊 Submitting an Evaluation Run

To submit an evaluation run for an existing task:

1. Create a JSON file at `eval_runs/<task_id>/<submission_id>.json`
2. Follow the format below.
3. Open a pull request with a description of the evaluation run.

The evaluation run JSON file should have the following format:

```json
{
  "submission_id": "run_2025_06_30_001",
  "task_id": "stat_interp_v2",
  "model_name": "gpt-4",
  "prompt_id": "prompt_v3",
  "submitter": "stanford-nlp-lab",
  "submission_time": "2025-06-30T21:00:00Z",
  "metrics": {
    "accuracy": 0.87,
    "f1": 0.82
  },
  "predictions_url": "https://your-bucket.s3.amazonaws.com/submissions/run_2025_06_30_001.json"
}
```

Some notes:
- `submission_id` should be a unique identifier for the evaluation run.
- `task_id` should be the ID of the task that the evaluation run is for.
- `model_name` should be the name of the model that was used to generate the predictions.
- `prompt_id` should be the ID of the prompt that was used to generate the predictions.
- `submitter` should be the name of the person who submitted the evaluation run.
- `submission_time` should be the time the evaluation run was submitted.
- `metrics` should be a dictionary of metrics and their values.
- `predictions_url` should be the URL of the predictions file.


## 📝 Prompt Templates

If you want to use a custom prompt for a task, you can create a prompt template in the `prompts` folder.

The prompt template JSON file should have the following format: