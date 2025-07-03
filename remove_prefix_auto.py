#!/usr/bin/env python3
"""
Script to remove 'legalbench_' prefix - auto mode (no prompts).
"""

import os
import json
import shutil
from pathlib import Path

def update_task_files(tasks_dir):
    """Remove legalbench_ prefix from task files and update task_id inside them."""
    updated_count = 0
    
    for filename in os.listdir(tasks_dir):
        if not filename.endswith('.json'):
            continue
            
        old_path = os.path.join(tasks_dir, filename)
        task_name = filename[:-5]  # Remove .json
        
        # Skip if doesn't have legalbench_ prefix
        if not task_name.startswith('legalbench_'):
            continue
        
        # New filename without prefix
        new_task_name = task_name[11:]  # Remove 'legalbench_'
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
        updated_count += 1
    
    return updated_count

def update_task_presets(presets_file):
    """Remove legalbench_ prefix from task IDs in presets."""
    if not os.path.exists(presets_file):
        print(f"Presets file not found: {presets_file}")
        return 0
    
    with open(presets_file, 'r') as f:
        presets_data = json.load(f)
    
    updated_count = 0
    
    # Update each preset
    for preset_id, preset_data in presets_data.get('presets', {}).items():
        if 'tasks' in preset_data:
            original_tasks = preset_data['tasks']
            updated_tasks = []
            
            for task_id in original_tasks:
                if task_id.startswith('legalbench_'):
                    new_task_id = task_id[11:]  # Remove prefix
                    updated_tasks.append(new_task_id)
                    updated_count += 1
                else:
                    updated_tasks.append(task_id)
            
            preset_data['tasks'] = updated_tasks
            print(f"✓ Updated preset '{preset_id}': {len(original_tasks)} tasks")
    
    # Write back
    with open(presets_file, 'w') as f:
        json.dump(presets_data, f, indent=2)
    
    return updated_count

def main():
    # Paths
    base_dir = Path(__file__).parent
    tasks_dir = base_dir / 'tasks'
    presets_file = base_dir / 'web' / 'task_presets.json'
    
    print("Removing 'legalbench_' prefix from all files...")
    print("="*50)
    
    # Update task files
    print("\nUPDATING TASK FILES")
    print("-"*40)
    
    if tasks_dir.exists():
        task_count = update_task_files(tasks_dir)
        print(f"\nUpdated {task_count} task files")
    else:
        print(f"Tasks directory not found: {tasks_dir}")
    
    # Update presets
    print("\nUPDATING TASK PRESETS")
    print("-"*40)
    
    preset_count = update_task_presets(presets_file)
    print(f"\nUpdated {preset_count} task references in presets")
    
    print("\n" + "="*50)
    print("✅ Prefix removal complete!")

if __name__ == "__main__":
    main()