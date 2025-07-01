from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime
from collections import defaultdict
import statistics

app = Flask(__name__)

def get_tasks():
    """Load all tasks from the tasks directory"""
    tasks = []
    tasks_dir = os.path.join(os.path.dirname(__file__), '..', 'tasks')
    
    if os.path.exists(tasks_dir):
        for filename in os.listdir(tasks_dir):
            if filename.endswith('.json'):
                with open(os.path.join(tasks_dir, filename), 'r') as f:
                    task = json.load(f)
                    tasks.append(task)
    
    return sorted(tasks, key=lambda x: x.get('name', ''))

def get_all_tags():
    """Get all unique tags from all tasks"""
    tasks = get_tasks()
    tags = set()
    for task in tasks:
        tags.update(task.get('tags', []))
    return sorted(list(tags))

def get_all_families():
    """Get all unique families from all tasks"""
    tasks = get_tasks()
    families = set()
    for task in tasks:
        family = task.get('family')
        if family:
            families.add(family)
    return sorted(list(families))

def get_all_document_types():
    """Get all unique document types from all tasks"""
    tasks = get_tasks()
    doc_types = set()
    for task in tasks:
        doc_type = task.get('document_type')
        if doc_type:
            doc_types.add(doc_type)
    return sorted(list(doc_types))

def get_tasks_by_family(family):
    """Get all tasks belonging to a specific family"""
    tasks = get_tasks()
    return [task for task in tasks if task.get('family') == family]

def get_eval_runs(task_id):
    """Load all evaluation runs for a specific task"""
    eval_runs = []
    eval_dir = os.path.join(os.path.dirname(__file__), '..', 'eval_runs', task_id)
    
    if os.path.exists(eval_dir):
        for filename in os.listdir(eval_dir):
            if filename.endswith('.json'):
                with open(os.path.join(eval_dir, filename), 'r') as f:
                    run = json.load(f)
                    eval_runs.append(run)
    
    return eval_runs

def get_task_by_id(task_id):
    """Get a specific task by ID"""
    tasks = get_tasks()
    for task in tasks:
        if task['task_id'] == task_id:
            return task
    return None

def calculate_leaderboard(task, eval_runs):
    """Calculate leaderboard rankings based on task metrics"""
    if not eval_runs or not task.get('metrics'):
        return []
    
    # Get the primary metric (first one listed)
    primary_metric = task['metrics'][0]['name']
    direction = task['metrics'][0]['direction']
    
    # Sort runs by primary metric
    sorted_runs = sorted(eval_runs, 
                        key=lambda x: x.get('metrics', {}).get(primary_metric, 0),
                        reverse=(direction == 'maximize'))
    
    # Add rank to each run
    for i, run in enumerate(sorted_runs):
        run['rank'] = i + 1
    
    return sorted_runs

def calculate_aggregate_scores(task_ids):
    """Calculate aggregate scores across multiple tasks"""
    model_scores = defaultdict(lambda: {'scores': [], 'task_count': 0, 'runs': []})
    
    for task_id in task_ids:
        task = get_task_by_id(task_id)
        if not task:
            continue
            
        eval_runs = get_eval_runs(task_id)
        if not eval_runs:
            continue
            
        # Normalize scores for this task (0-1 scale based on best/worst)
        primary_metric = task['metrics'][0]['name']
        direction = task['metrics'][0]['direction']
        
        metric_values = [run.get('metrics', {}).get(primary_metric, 0) for run in eval_runs]
        if not metric_values:
            continue
            
        min_val = min(metric_values)
        max_val = max(metric_values)
        
        for run in eval_runs:
            model_name = run.get('model_name', 'Unknown')
            score = run.get('metrics', {}).get(primary_metric, 0)
            
            # Normalize score to 0-1
            if max_val > min_val:
                if direction == 'maximize':
                    normalized = (score - min_val) / (max_val - min_val)
                else:
                    normalized = (max_val - score) / (max_val - min_val)
            else:
                normalized = 1.0
                
            model_scores[model_name]['scores'].append(normalized)
            model_scores[model_name]['task_count'] += 1
            model_scores[model_name]['runs'].append({
                'task_id': task_id,
                'task_name': task['name'],
                'score': score,
                'normalized_score': normalized,
                'metric': primary_metric
            })
    
    # Calculate average scores
    leaderboard = []
    for model_name, data in model_scores.items():
        if data['scores']:
            avg_score = statistics.mean(data['scores'])
            leaderboard.append({
                'model_name': model_name,
                'avg_score': avg_score,
                'task_count': data['task_count'],
                'total_tasks': len(task_ids),
                'runs': data['runs']
            })
    
    # Sort by average score
    leaderboard.sort(key=lambda x: x['avg_score'], reverse=True)
    
    # Add ranks
    for i, entry in enumerate(leaderboard):
        entry['rank'] = i + 1
    
    return leaderboard

@app.route('/')
def home():
    """Home page with project overview and navigation guide"""
    tasks = get_tasks()
    
    # Calculate statistics
    total_submissions = 0
    unique_models = set()
    
    for task in tasks:
        eval_runs = get_eval_runs(task['task_id'])
        task['submission_count'] = len(eval_runs)
        total_submissions += len(eval_runs)
        
        for run in eval_runs:
            unique_models.add(run.get('model_name', 'Unknown'))
    
    # Get featured tasks (those with most submissions)
    featured_tasks = sorted(tasks, key=lambda x: x.get('submission_count', 0), reverse=True)[:3]
    
    return render_template('index.html', 
                         task_count=len(tasks),
                         total_submissions=total_submissions,
                         unique_models=len(unique_models),
                         featured_tasks=featured_tasks)

@app.route('/tasks')
def tasks():
    """Tasks page showing all tasks with search and filters"""
    tasks = get_tasks()
    all_tags = get_all_tags()
    all_families = get_all_families()
    all_doc_types = get_all_document_types()
    
    # Get submission counts for each task
    for task in tasks:
        eval_runs = get_eval_runs(task['task_id'])
        task['submission_count'] = len(eval_runs)
    
    return render_template('home.html', 
                         tasks=tasks, 
                         all_tags=all_tags, 
                         all_families=all_families,
                         all_doc_types=all_doc_types)

@app.route('/task/<task_id>')
def task_detail(task_id):
    """Task detail page with leaderboard"""
    task = get_task_by_id(task_id)
    
    if not task:
        return "Task not found", 404
    
    eval_runs = get_eval_runs(task_id)
    leaderboard = calculate_leaderboard(task, eval_runs)
    
    return render_template('task_detail.html', 
                         task=task, 
                         leaderboard=leaderboard,
                         total_submissions=len(eval_runs))

@app.route('/aggregate')
def aggregate_leaderboard():
    """Aggregate leaderboard page"""
    tasks = get_tasks()
    all_families = get_all_families()
    all_tags = get_all_tags()
    all_doc_types = get_all_document_types()
    
    # Check if family, tag, or document type filter is applied
    selected_family = request.args.get('family')
    selected_tag = request.args.get('tag')
    selected_doc_type = request.args.get('doc_type')
    selected_task_ids = request.args.getlist('tasks')
    
    # If family is selected, get tasks from that family
    if selected_family:
        family_tasks = get_tasks_by_family(selected_family)
        selected_task_ids = [task['task_id'] for task in family_tasks]
    # If tag is selected, get tasks with that tag
    elif selected_tag:
        tag_tasks = [task for task in tasks if selected_tag in task.get('tags', [])]
        selected_task_ids = [task['task_id'] for task in tag_tasks]
    # If document type is selected, get tasks with that document type
    elif selected_doc_type:
        doc_type_tasks = [task for task in tasks if task.get('document_type') == selected_doc_type]
        selected_task_ids = [task['task_id'] for task in doc_type_tasks]
    # If no tasks selected and no filters, use all tasks
    elif not selected_task_ids:
        selected_task_ids = [task['task_id'] for task in tasks]
    
    # Get selected tasks info
    selected_tasks = [task for task in tasks if task['task_id'] in selected_task_ids]
    
    # Calculate aggregate leaderboard
    leaderboard = calculate_aggregate_scores(selected_task_ids)
    
    return render_template('aggregate.html',
                         tasks=tasks,
                         all_families=all_families,
                         all_tags=all_tags,
                         all_doc_types=all_doc_types,
                         selected_family=selected_family,
                         selected_tag=selected_tag,
                         selected_doc_type=selected_doc_type,
                         selected_tasks=selected_tasks,
                         selected_task_ids=selected_task_ids,
                         leaderboard=leaderboard)

@app.route('/api/tasks')
def api_tasks():
    """API endpoint for getting all tasks"""
    return jsonify(get_tasks())

@app.route('/api/task/<task_id>/leaderboard')
def api_task_leaderboard(task_id):
    """API endpoint for getting task leaderboard"""
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    eval_runs = get_eval_runs(task_id)
    leaderboard = calculate_leaderboard(task, eval_runs)
    
    return jsonify({
        'task': task,
        'leaderboard': leaderboard
    })

@app.route('/api/aggregate')
def api_aggregate():
    """API endpoint for aggregate leaderboard"""
    task_ids = request.args.getlist('tasks')
    if not task_ids:
        task_ids = [task['task_id'] for task in get_tasks()]
    
    leaderboard = calculate_aggregate_scores(task_ids)
    
    return jsonify({
        'task_ids': task_ids,
        'leaderboard': leaderboard
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)