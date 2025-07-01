# LegalEvalHub Web Interface

This is the web interface for LegalEvalHub, providing leaderboards and task browsing capabilities.

## Setup

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Features

- **Home Page**: Browse all available legal evaluation tasks
- **Task Detail Pages**: View leaderboards and detailed metrics for each task
- **API Endpoints**: 
  - `/api/tasks` - Get all tasks in JSON format
  - `/api/task/<task_id>/leaderboard` - Get leaderboard data for a specific task

## Development

The application automatically reloads when you make changes to the code (debug mode is enabled).

## Structure

- `app.py` - Main Flask application
- `templates/` - HTML templates
- `static/css/` - Stylesheets