#!/usr/bin/env python3
"""
Preview what would be renamed without making changes.
"""

import os
import json
from pathlib import Path

def preview_task_files(tasks_dir):
    """Preview task files that would be renamed."""
    to_rename = []
    already_prefixed = []
    
    for filename in sorted(os.listdir(tasks_dir)):
        if not filename.endswith('.json'):
            continue
            
        task_name = filename[:-5]  # Remove .json
        
        if task_name.startswith('legalbench_'):
            already_prefixed.append(filename)
        else:
            new_filename = f"legalbench_{task_name}.json"
            to_rename.append((filename, new_filename))
    
    return to_rename, already_prefixed

def preview_eval_runs(eval_runs_dir):
    """Preview evaluation directories that would be renamed."""
    to_rename = []
    already_prefixed = []
    
    for dirname in sorted(os.listdir(eval_runs_dir)):
        dir_path = os.path.join(eval_runs_dir, dirname)
        
        if not os.path.isdir(dir_path) or dirname.startswith('.'):
            continue
        
        if dirname.startswith('legalbench_'):
            already_prefixed.append(dirname)
        else:
            new_dirname = f"legalbench_{dirname}"
            to_rename.append((dirname, new_dirname))
    
    return to_rename, already_prefixed

def main():
    base_dir = Path(__file__).parent
    tasks_dir = base_dir / 'tasks'
    eval_runs_dir = base_dir / 'eval_runs'
    
    print("PREVIEW: What would be renamed")
    print("=" * 60)
    
    # Preview task files
    print("\nTASK FILES:")
    print("-" * 40)
    
    if tasks_dir.exists():
        to_rename, already_prefixed = preview_task_files(tasks_dir)
        
        print(f"Files to rename: {len(to_rename)}")
        for old, new in to_rename[:10]:  # Show first 10
            print(f"  {old} → {new}")
        if len(to_rename) > 10:
            print(f"  ... and {len(to_rename) - 10} more")
        
        print(f"\nAlready prefixed: {len(already_prefixed)}")
        if already_prefixed:
            for name in already_prefixed[:5]:
                print(f"  {name}")
            if len(already_prefixed) > 5:
                print(f"  ... and {len(already_prefixed) - 5} more")
    else:
        print(f"Tasks directory not found: {tasks_dir}")
    
    # Preview eval directories
    print("\n\nEVALUATION DIRECTORIES:")
    print("-" * 40)
    
    if eval_runs_dir.exists():
        to_rename, already_prefixed = preview_eval_runs(eval_runs_dir)
        
        print(f"Directories to rename: {len(to_rename)}")
        for old, new in to_rename[:10]:  # Show first 10
            print(f"  {old} → {new}")
        if len(to_rename) > 10:
            print(f"  ... and {len(to_rename) - 10} more")
        
        print(f"\nAlready prefixed: {len(already_prefixed)}")
        if already_prefixed:
            for name in already_prefixed[:5]:
                print(f"  {name}")
            if len(already_prefixed) > 5:
                print(f"  ... and {len(already_prefixed) - 5} more")
    else:
        print(f"Eval runs directory not found: {eval_runs_dir}")
    
    print("\n" + "=" * 60)
    print("To perform the actual rename, run:")
    print("  python rename_tasks_to_legalbench.py")

if __name__ == "__main__":
    main()