#!/usr/bin/env python3
"""
Script to rename all tasks to include 'legalbench_' prefix.
This updates:
1. Task files in tasks/
2. task_id field inside task JSON files
3. Evaluation directories in eval_runs/
4. task_id references in evaluation JSON files
"""

import os
import json
import shutil
from pathlib import Path

def update_task_files(tasks_dir):
    """Rename task files and update task_id inside them."""
    updated_count = 0
    
    for filename in os.listdir(tasks_dir):
        if not filename.endswith('.json'):
            continue
            
        old_path = os.path.join(tasks_dir, filename)
        task_name = filename[:-5]  # Remove .json
        
        # Skip if already has legalbench_ prefix
        if task_name.startswith('legalbench_'):
            print(f"Skipping {filename} - already has prefix")
            continue
        
        # New filename with prefix
        new_task_name = f"legalbench_{task_name}"
        new_filename = f"{new_task_name}.json"
        new_path = os.path.join(tasks_dir, new_filename)
        
        # Read and update the JSON content
        with open(old_path, 'r') as f:
            task_data = json.load(f)
        
        # Update task_id
        old_task_id = task_data.get('task_id', task_name)
        task_data['task_id'] = new_task_name
        
        # Write to new file
        with open(new_path, 'w') as f:
            json.dump(task_data, f, indent=2)
        
        # Remove old file
        os.remove(old_path)
        
        print(f"✓ Renamed {filename} → {new_filename}")
        print(f"  Updated task_id: {old_task_id} → {new_task_name}")
        updated_count += 1
    
    return updated_count

def update_eval_runs(eval_runs_dir):
    """Rename evaluation directories and update task_id in eval files."""
    updated_dirs = 0
    updated_files = 0
    
    for dirname in os.listdir(eval_runs_dir):
        dir_path = os.path.join(eval_runs_dir, dirname)
        
        # Skip non-directories and special files
        if not os.path.isdir(dir_path) or dirname.startswith('.'):
            continue
        
        # Skip if already has legalbench_ prefix
        if dirname.startswith('legalbench_'):
            print(f"Skipping eval dir {dirname} - already has prefix")
            continue
        
        # New directory name with prefix
        new_dirname = f"legalbench_{dirname}"
        new_dir_path = os.path.join(eval_runs_dir, new_dirname)
        
        # Rename directory
        shutil.move(dir_path, new_dir_path)
        print(f"✓ Renamed eval directory {dirname} → {new_dirname}")
        updated_dirs += 1
        
        # Update task_id in all JSON files in this directory
        for eval_file in Path(new_dir_path).glob('*.json'):
            try:
                with open(eval_file, 'r') as f:
                    eval_data = json.load(f)
                
                # Update task_id if it exists
                if 'task_id' in eval_data and eval_data['task_id'] == dirname:
                    eval_data['task_id'] = new_dirname
                    
                    with open(eval_file, 'w') as f:
                        json.dump(eval_data, f, indent=2)
                    
                    print(f"  Updated task_id in {eval_file.name}")
                    updated_files += 1
                    
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  Warning: Could not update {eval_file.name}: {e}")
    
    return updated_dirs, updated_files

def main():
    # Paths
    base_dir = Path(__file__).parent
    tasks_dir = base_dir / 'tasks'
    eval_runs_dir = base_dir / 'eval_runs'
    
    print("Starting task renaming process...")
    print(f"Tasks directory: {tasks_dir}")
    print(f"Eval runs directory: {eval_runs_dir}")
    print()
    
    # Backup reminder
    print("⚠️  WARNING: This will rename files and directories!")
    print("Make sure you have a backup before proceeding.")
    response = input("Continue? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Aborted.")
        return
    
    print("\n" + "="*50)
    print("UPDATING TASK FILES")
    print("="*50)
    
    if tasks_dir.exists():
        task_count = update_task_files(tasks_dir)
        print(f"\nUpdated {task_count} task files")
    else:
        print(f"Tasks directory not found: {tasks_dir}")
    
    print("\n" + "="*50)
    print("UPDATING EVALUATION RUNS")
    print("="*50)
    
    if eval_runs_dir.exists():
        dir_count, file_count = update_eval_runs(eval_runs_dir)
        print(f"\nUpdated {dir_count} evaluation directories")
        print(f"Updated {file_count} evaluation files")
    else:
        print(f"Eval runs directory not found: {eval_runs_dir}")
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print("✅ Task renaming complete!")
    print("\nNext steps:")
    print("1. Test the website to ensure everything works")
    print("2. Update any external references to the old task names")
    print("3. Commit the changes to git")

if __name__ == "__main__":
    main()