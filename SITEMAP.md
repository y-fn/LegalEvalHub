# LegalEvalHub Site Map

## Main Pages

### Home (`/`)
- Project overview and introduction
- Statistics: total tasks, submissions, and unique models
- Featured tasks with highest submission counts
- Quick links to main sections

### Tasks (`/tasks`)
- Browse all 162 legal evaluation tasks
- Search by task name or description
- Filter by:
  - Task family (e.g., LegalBench)
  - Tags (e.g., contract law, interpretation)
  - Document type (e.g., contract clause, statute)
- Each task shows submission count

### Task Detail (`/task/<task_id>`)
- Complete task description and metadata
- Leaderboard with model rankings
- Metrics displayed (accuracy, F1, etc.)
- Links to dataset and papers
- Task statistics (samples, token lengths)

### Aggregate Leaderboards (`/benchmarks`)
- Overview of all aggregate benchmarks
- Explanation of scoring methodology
- Grid view of available benchmarks
- Links to individual benchmark leaderboards

### Individual Benchmark (`/leaderboard/<preset_id>`)
- Benchmark-specific leaderboard
- Three ranking metrics:
  - Average Score (normalized 0-100%)
  - Average Rank (mean position)
  - Raw Metric Average
- List of tasks in benchmark
- Links to other benchmarks

### Resources (`/resources`)
- Links to evaluation harness
- Documentation and guides
- Community resources

### FAQ (`/faq`)
- Common questions about the platform
- How to contribute
- Technical details

### Sitemap (`/sitemap`)
- Complete list of all pages
- Hierarchical organization

## API Endpoints

### Get All Tasks
`GET /api/tasks`
- Returns all task definitions in JSON

### Get Task Leaderboard
`GET /api/task/<task_id>/leaderboard`
- Returns leaderboard for specific task

### Get Aggregate Scores
`GET /api/aggregate?tasks=<task_ids>`
- Returns aggregate scores for selected tasks

## Navigation Structure

```
Home
├── Tasks
│   └── Individual Task Pages (162 tasks)
├── Aggregate Leaderboards
│   ├── Core Legal Reasoning
│   ├── Contract Understanding
│   ├── MAUD M&A Provisions
│   ├── Statutory Interpretation
│   ├── Case Law Analysis
│   ├── Legal Classification Tasks
│   ├── Legal Information Retrieval
│   ├── Legal Interpretation Tasks
│   ├── Legal Knowledge Tasks
│   ├── Legal Text Generation
│   ├── Legal Entailment Tasks
│   └── Full LegalBench
├── Resources
├── FAQ
└── GitHub (external)
```