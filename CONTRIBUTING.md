# Contributing to LegalEvalHub

Thank you for your interest in contributing to **LegalEvalHub**!

You can contribute in three primary ways:
1. Submitting a **new task**
2. Submitting an **evaluation run** for an existing task
3. Submitting a **new leaderboard**

All contributions are made via pull requests to this GitHub repository. If you would like to contribute via alternative means, please reach out to <a href="mailto:nguha@cs.stanford.edu">nguha@cs.stanford.edu</a>.


## 🧩 Submitting a New Task

To add a new evaluation task to LegalEvalHub:

1. Create a JSON file at `tasks/<task_id>.json`
2. Follow the format below.
3. Open a pull request with a description of the task.

The task JSON file should have the following format:

```json
{
  "task_id": "your_task_id",
  "name": "Your Task Name",
  "family": "LegalBench",
  "description": "Brief description of what the task evaluates",
  "dataset_url": "https://example.com/your_dataset.csv",
  "num_samples": 500,
  "tags": ["contract law", "interpretation"],
  "document_type": "contract clause",
  "min_input_length": 100,
  "max_input_length": 1000,
  "metrics": [
    {"name": "accuracy", "direction": "maximize"},
    {"name": "f1_macro", "direction": "maximize"},
    {"name": "balanced_accuracy", "direction": "maximize"}
  ],
  "task_type": "Binary classification",
  "legal_reasoning_type": "Interpretation",
  "contributed_by_name": "Your Name",
  "contributed_by_email": "your.name@institution.edu",
  "paper_url": "https://example.com/paper.pdf",
  "paper_title": "Paper Title",
  "paper_authors": ["Author 1", "Author 2"],
  "source": "Dataset source",
  "license": "CC BY 4.0"
}
```

### Field Descriptions:

- **`task_id`**: Unique identifier for the task (use lowercase with underscores)
- **`name`**: Human-readable task name
- **`family`**: Task family or benchmark suite (typically "LegalBench")
- **`description`**: Clear description of what the task evaluates
- **`dataset_url`**: URL where the dataset can be accessed
- **`num_samples`**: Total number of examples in the dataset
- **`tags`**: List of descriptive tags (avoid generic tags like "classification")
  - Examples: "contract law", "interpretation", "rule application", "tax law"
- **`document_type`**: Type of legal document analyzed
  - Examples: "contract clause", "statute", "judicial opinion", "privacy policy"
- **`min_input_length`** & **`max_input_length`**: Token counts (using LLaMA tokenizer)
- **`metrics`**: List of evaluation metrics with direction
  - Common metrics: accuracy, f1_macro, f1_micro, balanced_accuracy
  - Direction: "maximize" for most metrics, "minimize" for error metrics
- **`task_type`**: Classification type
  - Options: "Binary classification", "Multiclass classification", "Text generation", "Numeric prediction"
- **`legal_reasoning_type`**: Type of legal reasoning required
  - Examples: "Interpretation", "Rule application", "Issue spotting"
- **`contributed_by_name`** & **`contributed_by_email`**: Your contact information
- **`paper_url`**, **`paper_title`**, **`paper_authors`**: Associated research paper
- **`source`**: Original dataset source
- **`license`**: Data license (e.g., "CC BY 4.0")


## 📊 Submitting an Evaluation Run

To submit an evaluation run for an existing task:

1. Create a JSON file at `eval_runs/<task_id>/<submission_id>.json`
2. Follow the format below.
3. Open a pull request with a description of the evaluation run.

The evaluation run JSON file should have the following format:

```json
{
  "submission_id": "run_2025_07_03_123456_abc123",
  "task_id": "hearsay",
  "model_name": "gpt-4",
  "prompt_id": "base",
  "submitter": "Your Name",
  "submission_time": "2025-07-03T12:34:56Z",
  "metrics": {
    "accuracy": 0.87,
    "balanced_accuracy": 0.85,
    "f1_macro": 0.86,
    "f1_micro": 0.87,
    "valid_predictions_ratio": 1.0,
    "n_samples": 100
  },
  "predictions_url": "https://storage.googleapis.com/legal-eval-runs/predictions/hearsay/gpt-4/base/run_2025_07_03_123456_abc123_predictions.json"
}
```

### Field Descriptions:

- **`submission_id`**: Unique identifier (format: `run_YYYY_MM_DD_HHMMSS_RANDOM`)
- **`task_id`**: Must match an existing task ID
- **`model_name`**: Name and version of the model evaluated
- **`prompt_id`**: Identifier for the prompt template used (typically "base")
- **`submitter`**: Your name or organization
- **`submission_time`**: ISO 8601 timestamp
- **`metrics`**: Dictionary containing all evaluation metrics
  - Must include all metrics specified in the task definition
  - Include `n_samples` to show how many examples were evaluated
  - Include `valid_predictions_ratio` to show prediction quality
- **`predictions_url`**: URL to hosted predictions file (optional but recommended)


## 🏆 Contributing a New Leaderboard

To add a new aggregate leaderboard to LegalEvalHub, open `web/task_presets.json` and add your new leaderboard configuration:

```json
{
  "presets": {
    "your_leaderboard_id": {
      "name": "Your Leaderboard Name",
      "description": "A clear description of what this leaderboard evaluates and why these tasks are grouped together.",
      "tasks": [
        "task_id_1",
        "task_id_2",
        "task_id_3"
      ]
    }
  }
}
```
