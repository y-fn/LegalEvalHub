#!/usr/bin/env python3
"""
Script to rename evaluation directories to include 'legalbench_' prefix.
Only handles eval_runs since tasks are already renamed.
"""

import os
import json
import shutil
from pathlib import Path

def update_eval_runs(eval_runs_dir):
    """Rename evaluation directories and update task_id in eval files."""
    updated_dirs = 0
    updated_files = 0
    errors = []
    
    # Get list of directories to rename
    dirs_to_rename = []
    for dirname in os.listdir(eval_runs_dir):
        dir_path = os.path.join(eval_runs_dir, dirname)
        
        # Skip non-directories and special files
        if not os.path.isdir(dir_path) or dirname.startswith('.'):
            continue
        
        # Skip if already has legalbench_ prefix
        if dirname.startswith('legalbench_'):
            continue
            
        dirs_to_rename.append(dirname)
    
    print(f"Found {len(dirs_to_rename)} directories to rename")
    
    # Process each directory
    for dirname in dirs_to_rename:
        dir_path = os.path.join(eval_runs_dir, dirname)
        new_dirname = f"legalbench_{dirname}"
        new_dir_path = os.path.join(eval_runs_dir, new_dirname)
        
        try:
            # Rename directory
            shutil.move(dir_path, new_dir_path)
            print(f"✓ Renamed {dirname} → {new_dirname}")
            updated_dirs += 1
            
            # Update task_id in all JSON files in this directory
            for eval_file in Path(new_dir_path).glob('*.json'):
                try:
                    with open(eval_file, 'r') as f:
                        eval_data = json.load(f)
                    
                    # Update task_id if it matches the old directory name
                    if 'task_id' in eval_data and eval_data['task_id'] == dirname:
                        eval_data['task_id'] = new_dirname
                        
                        with open(eval_file, 'w') as f:
                            json.dump(eval_data, f, indent=2)
                        
                        updated_files += 1
                        
                except (json.JSONDecodeError, KeyError) as e:
                    error_msg = f"Could not update {eval_file.name}: {e}"
                    print(f"  ⚠️  {error_msg}")
                    errors.append(error_msg)
                    
        except Exception as e:
            error_msg = f"Could not rename {dirname}: {e}"
            print(f"✗ {error_msg}")
            errors.append(error_msg)
    
    return updated_dirs, updated_files, errors

def main():
    # Path to eval runs
    base_dir = Path(__file__).parent
    eval_runs_dir = base_dir / 'eval_runs'
    
    print("Evaluation Directory Renaming Tool")
    print("=" * 50)
    print(f"Eval runs directory: {eval_runs_dir}")
    print()
    
    if not eval_runs_dir.exists():
        print(f"Error: Eval runs directory not found: {eval_runs_dir}")
        return
    
    # Confirmation
    print("⚠️  This will rename evaluation directories to add 'legalbench_' prefix")
    print("⚠️  Make sure you have a backup!")
    response = input("\nContinue? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Aborted.")
        return
    
    print("\nStarting rename process...")
    print("-" * 50)
    
    dir_count, file_count, errors = update_eval_runs(eval_runs_dir)
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"✅ Renamed {dir_count} directories")
    print(f"✅ Updated {file_count} JSON files")
    
    if errors:
        print(f"\n⚠️  {len(errors)} errors occurred:")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
    
    print("\nDone!")

if __name__ == "__main__":
    main()