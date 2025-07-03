# Changelog

## [2025-07-03] - Major Update

### Added
- **Aggregate Leaderboards**: 12 pre-configured benchmark suites grouping related tasks
- **Enhanced Metrics**: Added Average Rank and Raw Metric Average to leaderboards
- **Resources Page**: Central hub for documentation, tools, and community links
- **FAQ Page**: Comprehensive frequently asked questions
- **Benchmarks Landing Page**: Overview of all aggregate leaderboards with explanations
- **Dropdown Navigation**: Converted benchmarks navigation to dropdown menu
- **Context Processor**: Added Flask context processor for global template variables
- **Error Handling**: Added JSON parsing error handling for malformed task files

### Changed
- **Task Tags**: Removed redundant tags ("classification", "binary classification", "multiclass classification")
- **Navigation**: Renamed "Benchmarks" to "Aggregate Leaderboards" throughout
- **Task List Display**: Simplified task lists from grid boxes to bullet points
- **Directory Structure**: Updated to save results as `results/task/model/prompt`
- **Documentation**: Comprehensive updates to README and CONTRIBUTING files
- **Leaderboard Calculation**: Enhanced to include rank tracking and raw metric averages

### Removed
- **Prompt Folder**: Removed prompt folder and all references from documentation
- **Custom Benchmarks**: Removed custom benchmark selection, only preset benchmarks available
- **Redundant Tags**: Cleaned up classification-related tags from all 162 task files

### Technical
- **Flask Routes**: Added routes for benchmarks, resources, FAQ, and preset leaderboards
- **Template Updates**: Created new templates for benchmarks, resources, FAQ pages
- **CSS Enhancements**: Added styles for dropdown menus, FAQ sections, resource cards
- **API Consistency**: Standardized JSON response formats across endpoints

### Data Updates
- **Task Files**: Updated all 162 task JSON files to remove redundant classification tags
- **Task Presets**: Configured 12 aggregate leaderboard presets in `task_presets.json`
- **Evaluation Runs**: Added support for batch API metadata in evaluation results

### Documentation
- **README.md**: Complete rewrite with updated features and structure
- **CONTRIBUTING.md**: Enhanced with field descriptions and aggregate leaderboard info
- **SITEMAP.md**: Added comprehensive site structure documentation
- **In-app Documentation**: Added detailed explanations on benchmarks and FAQ pages