# Task Presets Configuration

This document explains how to configure and manage pre-configured task combinations for the aggregate leaderboard.

## Overview

Task presets allow users to quickly select meaningful combinations of tasks for aggregate evaluation. Presets are defined in `web/task_presets.json`.

## Preset Structure

Each preset has the following structure:

```json
{
  "preset_id": {
    "name": "Display Name",
    "description": "A description of what this preset contains",
    "tasks": [
      "task_id_1",
      "task_id_2",
      "task_id_3"
    ]
  }
}
```

## Current Presets

### 1. Core Legal Reasoning (`core_legal_reasoning`)
Fundamental legal reasoning tasks including rule application, issue spotting, and conclusion tasks.

### 2. Contract Understanding (`contract_understanding`)
Tasks focused on contract analysis, interpretation, and clause identification. Includes all CUAD and contract NLI tasks.

### 3. M&A Deal Points - MAUD (`maud_ma_provisions`)
All merger agreement provision tasks from the MAUD dataset.

### 4. Legal Q&A (`legal_qa`)
Question answering tasks across various legal domains including rules, privacy policies, and consumer contracts.

### 5. Case Outcome Prediction (`case_outcome_prediction`)
Tasks predicting judicial decisions and case outcomes.

### 6. Statutory Interpretation (`statutory_interpretation`)
Tasks involving interpretation and application of statutes.

### 7. Corporate Legal (`corporate_legal`)
Tasks related to corporate law, securities, and business agreements, including supply chain disclosures and corporate lobbying.

### 8. Legal Ethics & Professional Responsibility (`legal_ethics`)
Tasks related to professional conduct and ethical obligations.

### 9. Specialized Legal Domains (`specialized_legal`)
Tasks in specialized areas of law including tax, insurance, torts, and the Learned Hands classification tasks.

### 10. Citation Analysis (`citation_analysis`)
Tasks involving legal citations and references.

### 11. Legal Definition & Concept Extraction (`definition_extraction`)
Tasks focused on identifying and extracting legal definitions.

### 12. Quick Benchmark (`quick_benchmark`)
A small representative subset of 10 tasks for quick evaluation.

## Adding New Presets

To add a new preset:

1. Edit `web/task_presets.json`
2. Add a new entry with a unique preset ID
3. Include:
   - `name`: Short, descriptive name (shown on buttons)
   - `description`: Longer explanation (shown as tooltip and in results)
   - `tasks`: Array of task IDs

Example:
```json
"my_custom_preset": {
  "name": "My Custom Tasks",
  "description": "A custom selection of tasks for specific testing",
  "tasks": [
    "legalbench_hearsay",
    "legalbench_scalr",
    "legalbench_proa"
  ]
}
```

## Guidelines for Creating Presets

1. **Meaningful Groupings**: Group tasks that measure similar capabilities or relate to the same legal domain
2. **Appropriate Size**: Keep presets between 3-50 tasks for meaningful aggregation
3. **Clear Names**: Use descriptive names that immediately convey the preset's purpose
4. **Detailed Descriptions**: Explain what capability or domain the preset evaluates
5. **Task Validation**: Ensure all task IDs in the preset actually exist

## Usage

Presets appear in the aggregate leaderboard interface at `/aggregate`. Users can:
- Click on a preset to instantly load those tasks
- See the number of tasks in each preset
- Read descriptions to understand what each preset evaluates

The URL format for presets is: `/aggregate?preset=preset_id`

## Maintenance

Periodically review presets to:
- Remove tasks that no longer exist
- Add new relevant tasks to existing presets
- Create new presets for emerging evaluation needs
- Update descriptions to remain accurate