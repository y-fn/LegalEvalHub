from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os
from datetime import datetime
from collections import defaultdict
import statistics

app = Flask(__name__)

@app.context_processor
def inject_presets():
    """Inject presets into all templates for the dropdown menu"""
    return dict(presets=get_task_presets())

def get_tasks():
    """Load all tasks from the tasks directory"""
    tasks = []
    tasks_dir = os.path.join(os.path.dirname(__file__), '..', 'tasks')
    
    if os.path.exists(tasks_dir):
        for filename in os.listdir(tasks_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(tasks_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        task = json.load(f)
                        tasks.append(task)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON in {filename}: {e}")
                    continue
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
    
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

def get_task_presets():
    """Load task presets from configuration file"""
    presets_path = os.path.join(os.path.dirname(__file__), 'task_presets.json')
    
    if os.path.exists(presets_path):
        with open(presets_path, 'r') as f:
            data = json.load(f)
            return data.get('presets', {})
    
    return {}

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
    model_scores = defaultdict(lambda: {
        'scores': [], 
        'task_count': 0, 
        'runs': [], 
        'submitters': set(), 
        'submission_ids': set(),
        'ranks': [],
        'raw_metrics': []
    })
    
    for task_id in task_ids:
        task = get_task_by_id(task_id)
        if not task:
            continue
            
        eval_runs = get_eval_runs(task_id)
        if not eval_runs:
            continue
            
        # Get primary metric info
        primary_metric = task['metrics'][0]['name']
        direction = task['metrics'][0]['direction']
        
        # Sort runs by primary metric to determine ranks
        sorted_runs = sorted(eval_runs, 
                           key=lambda x: x.get('metrics', {}).get(primary_metric, 0),
                           reverse=(direction == 'maximize'))
        
        # Create a rank mapping
        rank_map = {}
        for rank, run in enumerate(sorted_runs, 1):
            rank_map[run.get('model_name', 'Unknown')] = rank
        
        # Calculate normalized scores
        metric_values = [run.get('metrics', {}).get(primary_metric, 0) for run in eval_runs]
        if not metric_values:
            continue
            
        min_val = min(metric_values)
        max_val = max(metric_values)
        
        for run in eval_runs:
            model_name = run.get('model_name', 'Unknown')
            submitter = run.get('submitter', 'Unknown')
            submission_id = run.get('submission_id', '')
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
            model_scores[model_name]['submitters'].add(submitter)
            model_scores[model_name]['submission_ids'].add(submission_id)
            model_scores[model_name]['ranks'].append(rank_map[model_name])
            model_scores[model_name]['raw_metrics'].append(score)
            model_scores[model_name]['runs'].append({
                'task_id': task_id,
                'task_name': task['name'],
                'score': score,
                'normalized_score': normalized,
                'metric': primary_metric,
                'submitter': submitter,
                'rank': rank_map[model_name]
            })
    
    # Calculate average scores
    leaderboard = []
    for model_name, data in model_scores.items():
        # Only include models that have been evaluated on ALL tasks in the preset
        print(model_name, data['task_count'], len(task_ids))
        if data['scores'] and data['task_count'] == len(task_ids):
            avg_raw_metric = statistics.mean(data['raw_metrics'])
            # Don't calculate wins or avg_rank yet - we'll do it after recalculating relative ranks
            
            # Get the most common submitter (in case there are multiple)
            submitters_list = list(data['submitters'])
            submitter = submitters_list[0] if len(submitters_list) == 1 else ', '.join(sorted(submitters_list))
            
            leaderboard.append({
                'model': model_name,
                'submitter': submitter,
                'wins': 0, # Placeholder - will be calculated later
                'avg_rank': 0, # Placeholder - will be calculated later
                'avg_raw_metric': avg_raw_metric,
                'num_tasks': data['task_count'],
                'total_tasks': len(task_ids),
                'num_submissions': len(data['submission_ids']),
                'runs': data['runs']
            })
    
    # Don't sort yet - we need to calculate avg_rank first after relative rank recalculation
    
    # Recalculate task-specific ranks relative to leaderboard models only
    leaderboard_models = {entry['model'] for entry in leaderboard}
    
    # Group runs by task for relative ranking
    task_runs = {}
    for entry in leaderboard:
        for run in entry['runs']:
            task_id = run['task_id']
            if task_id not in task_runs:
                task_runs[task_id] = []
            task_runs[task_id].append({
                'model': entry['model'],
                'score': run['score'],
                'run': run
            })
    
    # Recalculate ranks for each task among leaderboard models
    for task_id, runs in task_runs.items():
        # Get task info to determine ranking direction
        task = next((t for t in get_tasks() if t['task_id'] == task_id), None)
        if not task:
            continue
            
        primary_metric = task['metrics'][0]['name']
        direction = task['metrics'][0]['direction']
        
        # Sort runs by score for this task
        runs.sort(key=lambda x: x['score'], reverse=(direction == 'maximize'))
        
        # Assign ranks with proper tie handling
        current_rank = 1
        for i, run_data in enumerate(runs):
            # Check if this score is different from the previous one
            if i > 0 and runs[i]['score'] != runs[i-1]['score']:
                current_rank = i + 1  # Update rank to current position
            
            model_name = run_data['model']
            # Find the entry in leaderboard and update the specific run's rank
            for entry in leaderboard:
                if entry['model'] == model_name:
                    for run in entry['runs']:
                        if run['task_id'] == task_id:
                            run['rank'] = current_rank
                            break
                    break
    
    # Now calculate wins and average rank based on the updated relative ranks
    for entry in leaderboard:
        # Calculate wins (number of rank=1 positions)
        wins = sum(1 for run in entry['runs'] if run['rank'] == 1)
        entry['wins'] = wins
        
        # Calculate average rank using the new relative ranks
        relative_ranks = [run['rank'] for run in entry['runs']]
        entry['avg_rank'] = statistics.mean(relative_ranks)
    
    # Now sort by average rank (lower is better)
    leaderboard.sort(key=lambda x: x['avg_rank'])
    
    # Update final ranks after sorting
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
    """Redirect to the benchmarks page"""
    return redirect(url_for('benchmarks'))

@app.route('/benchmarks')
def benchmarks():
    """Aggregate leaderboards landing page"""
    presets = get_task_presets()
    return render_template('benchmarks.html', presets=presets)

@app.route('/leaderboard/<preset_id>')
def preset_leaderboard(preset_id):
    """Dedicated page for a specific preset leaderboard"""
    presets = get_task_presets()
    
    # Check if preset exists
    if preset_id not in presets:
        return "Preset not found", 404
    
    preset_data = presets[preset_id]
    tasks = get_tasks()
    
    # Get tasks for this preset
    selected_task_ids = preset_data['tasks']
    selected_tasks = [task for task in tasks if task['task_id'] in selected_task_ids]
    
    # Check if it's a single-task preset
    if len(selected_task_ids) == 1:
        # For single-task presets, get the task-specific leaderboard
        task_id = selected_task_ids[0]
        task = get_task_by_id(task_id)
        eval_runs = get_eval_runs(task_id)
        single_task_leaderboard = calculate_leaderboard(task, eval_runs) if task else []
        
        return render_template('preset_leaderboard.html',
                             preset_id=preset_id,
                             preset_data=preset_data,
                             selected_tasks=selected_tasks,
                             single_task_leaderboard=single_task_leaderboard,
                             all_presets=presets)
    else:
        # Calculate aggregate leaderboard for multi-task presets
        leaderboard = calculate_aggregate_scores(selected_task_ids)
        
        return render_template('preset_leaderboard.html',
                             preset_id=preset_id,
                             preset_data=preset_data,
                             selected_tasks=selected_tasks,
                             leaderboard=leaderboard,
                             all_presets=presets)

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

@app.route('/faq')
def faq():
    """FAQ page"""
    return render_template('faq.html')

@app.route('/resources')
def resources():
    """Resources page"""
    return render_template('resources.html')

@app.route('/sitemap')
def sitemap():
    """Simple sitemap page listing all available pages"""
    presets = get_task_presets()
    tasks = get_tasks()
    
    pages = {
        'Main Pages': [
            ('Home', url_for('home')),
            ('Tasks', url_for('tasks')),
            ('Aggregate Leaderboards', url_for('benchmarks')),
            ('Resources', url_for('resources')),
            ('FAQ', url_for('faq')),
        ],
        'Individual Leaderboards': [
            (preset_data['name'], url_for('preset_leaderboard', preset_id=preset_id))
            for preset_id, preset_data in presets.items()
        ],
        'Individual Tasks': [
            (task['name'], url_for('task_detail', task_id=task['task_id']))
            for task in tasks[:10]  # Show first 10 tasks
        ]
    }
    
    return render_template('sitemap.html', pages=pages, num_tasks=len(tasks))

if __name__ == '__main__':
    app.run(debug=True, port=5000)