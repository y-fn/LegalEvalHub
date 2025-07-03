# ⚖️ LegalEvalHub: Benchmarking LLMs on Legal Tasks

**LegalEvalHub** is a simple leaderboard-centric website for tracking and sharing LLM performance on different legal tasks. The platform is intended to be open: please contribute either tasks or evaluation runs. You can access the website [here](https://legalevalhub.up.railway.app/).

To contribute an evaluation run, a new task, or a new leaderboard, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

---

## 📁 Repository Structure

```bash
.
├── tasks/                      # Community-defined task metadata
│   └── <task_id>.json
├── eval_runs/                 # Community-submitted eval run metadata
│   └── <task_id>/             # One folder per task
│       └── <submission_id>.json
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
│   │   ├── benchmarks.html    # Aggregate leaderboards overview
│   │   ├── preset_leaderboard.html  # Individual aggregate leaderboard
│   │   ├── faq.html           # Frequently asked questions
│   │   └── resources.html     # Resources and documentation
│   ├── static/
│   │   └── css/
│   │       └── style.css      # Wikipedia-style minimal CSS
│   └── task_presets.json      # Aggregate leaderboard configurations
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

