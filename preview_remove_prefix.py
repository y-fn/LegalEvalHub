#!/usr/bin/env python3
"""
Preview what would be changed when removing legalbench_ prefix.
"""

import os
import json
from pathlib import Path

def preview_task_files(tasks_dir):
    """Preview task files that would be renamed."""
    to_rename = []
    no_prefix = []
    
    for filename in sorted(os.listdir(tasks_dir)):
        if not filename.endswith('.json'):
            continue
            
        task_name = filename[:-5]  # Remove .json
        
        if task_name.startswith('legalbench_'):
            new_task_name = task_name[11:]  # Remove prefix
            new_filename = f"{new_task_name}.json"
            to_rename.append((filename, new_filename))
        else:
            no_prefix.append(filename)
    
    return to_rename, no_prefix

def preview_eval_runs(eval_runs_dir):
    """Preview evaluation directories that would be renamed."""
    to_rename = []
    no_prefix = []
    conflicts = []
    
    for dirname in sorted(os.listdir(eval_runs_dir)):
        dir_path = os.path.join(eval_runs_dir, dirname)
        
        if not os.path.isdir(dir_path) or dirname.startswith('.'):
            continue
        
        if dirname.startswith('legalbench_'):
            new_dirname = dirname[11:]  # Remove prefix
            new_dir_path = os.path.join(eval_runs_dir, new_dirname)
            
            if os.path.exists(new_dir_path):
                conflicts.append((dirname, new_dirname))
            else:
                to_rename.append((dirname, new_dirname))
        else:
            no_prefix.append(dirname)
    
    return to_rename, no_prefix, conflicts

def preview_presets(presets_file):
    """Preview task IDs in presets that would be updated."""
    if not os.path.exists(presets_file):
        return 0, []
    
    with open(presets_file, 'r') as f:
        presets_data = json.load(f)
    
    to_update = []
    
    for preset_id, preset_data in presets_data.get('presets', {}).items():
        if 'tasks' in preset_data:
            prefixed_tasks = [t for t in preset_data['tasks'] if t.startswith('legalbench_')]
            if prefixed_tasks:
                to_update.append((preset_id, len(prefixed_tasks)))
    
    return sum(count for _, count in to_update), to_update

def main():
    base_dir = Path(__file__).parent
    tasks_dir = base_dir / 'tasks'
    eval_runs_dir = base_dir / 'eval_runs'
    presets_file = base_dir / 'web' / 'task_presets.json'
    
    print("PREVIEW: Removing 'legalbench_' prefix")
    print("=" * 60)
    
    # Preview task files
    print("\nTASK FILES:")
    print("-" * 40)
    
    if tasks_dir.exists():
        to_rename, no_prefix = preview_task_files(tasks_dir)
        
        print(f"Files to rename: {len(to_rename)}")
        for old, new in to_rename[:10]:  # Show first 10
            print(f"  {old} → {new}")
        if len(to_rename) > 10:
            print(f"  ... and {len(to_rename) - 10} more")
        
        print(f"\nAlready without prefix: {len(no_prefix)}")
    else:
        print(f"Tasks directory not found: {tasks_dir}")
    
    # Preview eval directories
    print("\n\nEVALUATION DIRECTORIES:")
    print("-" * 40)
    
    if eval_runs_dir.exists():
        to_rename, no_prefix, conflicts = preview_eval_runs(eval_runs_dir)
        
        print(f"Directories to rename: {len(to_rename)}")
        for old, new in to_rename[:10]:  # Show first 10
            print(f"  {old} → {new}")
        if len(to_rename) > 10:
            print(f"  ... and {len(to_rename) - 10} more")
        
        if conflicts:
            print(f"\n⚠️  CONFLICTS (target already exists): {len(conflicts)}")
            for old, new in conflicts[:5]:
                print(f"  {old} → {new} (EXISTS!)")
            if len(conflicts) > 5:
                print(f"  ... and {len(conflicts) - 5} more")
        
        print(f"\nAlready without prefix: {len(no_prefix)}")
    else:
        print(f"Eval runs directory not found: {eval_runs_dir}")
    
    # Preview presets
    print("\n\nTASK PRESETS:")
    print("-" * 40)
    
    total_refs, preset_updates = preview_presets(presets_file)
    print(f"Task references to update: {total_refs}")
    for preset_id, count in preset_updates:
        print(f"  {preset_id}: {count} tasks")
    
    print("\n" + "=" * 60)
    print("To perform the actual changes, run:")
    print("  python remove_legalbench_prefix.py")

if __name__ == "__main__":
    main()