# ⚖️ LegalEvalHub: Benchmarking LLMs on Legal Tasks

**LegalEvalHub** is a community-driven platform for evaluating large language models (LLMs) on legal tasks. The platform supports shared benchmarks, reproducible submissions, and transparent leaderboards—designed to track and compare model performance across diverse legal challenges.


To contribute a eval run or a task, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

---

## 🧠 Overview

LegalEvalHub provides:

- **Task definitions** hosted in this GitHub repo as lightweight JSON files
- **Model evaluation runs** uploaded via a web interface, referencing hosted prediction files
- **Leaderboards** that update as new eval runs are submitted
- **Per-task pages** that include metadata, metrics, and model outputs

---

## 📁 Repository Structure

```bash
.
├── tasks/                      # Community-defined task metadata
│   └── <task_id>.json
├── eval_runs/                 # Community-submitted eval run metadata
│   └── <task_id>/             # One folder per task
│       └── <submission_id>.json
├── prompts/                   # (Optional) Prompt templates
│   └── <prompt_id>.txt
├── utils/                     # Validation utilities (coming soon)
│   └── validate_task.py
│   └── validate_eval_run.py
├── web/                       # Flask web interface
│   ├── app.py                 # Main Flask application
│   ├── templates/             # HTML templates
│   │   ├── base.html          # Base template with navigation
│   │   ├── index.html         # Home page with project overview
│   │   ├── home.html          # Tasks listing page
│   │   ├── task_detail.html   # Individual task page
│   │   └── aggregate.html     # Aggregate leaderboard page
│   └── static/
│       └── css/
│           └── style.css      # Wikipedia-style minimal CSS
├── requirements.txt           # Python dependencies
├── README.md
└── CONTRIBUTING.md
```

---

## 🚀 Quick Start

### Running the Web Interface

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/LegalEvalHub.git
   cd LegalEvalHub
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask application:**
   ```bash
   cd web
   python app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

---

## 🌐 Web Interface Features

The LegalEvalHub web interface provides:

### Home Page
- Project overview and documentation
- Links to browse tasks, view leaderboards, and contribute

### Tasks Page
- Browse all available legal evaluation tasks
- **Search functionality** to find tasks by name or description
- **Filter by task family** (e.g., LegalBench, ContractBench)
- **Filter by tags** (e.g., contract analysis, statutory interpretation)
- **Filter by document type** (e.g., judicial opinion, commercial contract)
- View submission counts for each task

### Task Detail Pages
- Complete task description and metadata
- **Ranked leaderboard** showing model performance across all metrics
- Direct links to:
  - Dataset downloads
  - Associated research papers
  - API endpoints for programmatic access

### Aggregate Leaderboard
- Compare model performance across multiple tasks
- **Quick selection by family** - View aggregate scores for entire task families
- **Quick selection by tag** - View aggregate scores for tasks with specific tags
- **Quick selection by document type** - View aggregate scores for tasks with specific document types
- **Custom task selection** - Choose individual tasks to aggregate
- Normalized scoring methodology for fair comparison across different metrics

### API Endpoints
- `GET /api/tasks` - Returns all tasks in JSON format
- `GET /api/task/<task_id>/leaderboard` - Returns leaderboard data for a specific task
- `GET /api/aggregate?tasks=<task_ids>` - Returns aggregate leaderboard for selected tasks

---

## 📊 Example Tasks

The repository includes sample tasks demonstrating different types of legal evaluations:

1. **Contract Clause Extraction** - Extract and classify specific clauses from legal contracts
2. **Case Outcome Prediction** - Predict binary outcomes of federal court cases
3. **Legal Question Answering** - Answer multiple-choice questions about legal concepts

Each task includes metrics like accuracy, F1 score, precision, and recall as appropriate.
