#!/usr/bin/env python3
"""
Example script demonstrating the usage of the metrics module
in the Code Review Assistant.
"""

import os
import sys
import time
import random

# Add parent directory to path to allow importing metrics module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from metrics import Metrics, timed

def simulate_codebase():
    """Generate a simulated codebase structure for the demo."""
    return {
        "main.py": {"lines": 150, "issues": {"security": 1, "performance": 2, "style": 3}},
        "utils.py": {"lines": 250, "issues": {"security": 0, "performance": 1, "style": 5}},
        "api.py": {"lines": 320, "issues": {"security": 3, "performance": 2, "logic": 1}},
        "models.py": {"lines": 400, "issues": {"security": 0, "performance": 1, "style": 2}},
        "views.py": {"lines": 280, "issues": {"security": 1, "performance": 0, "logic": 3}},
        "config.py": {"lines": 50, "issues": {"security": 1, "performance": 0, "style": 1}},
        "database.py": {"lines": 180, "issues": {"security": 2, "performance": 3, "logic": 0}},
    }

def main():
    """Run a simulated code review to demonstrate metrics collection."""
    print("Starting simulated code review with metrics...")
    
    # Create a metrics instance
    metrics = Metrics()
    
    # Simulate a codebase
    codebase = simulate_codebase()
    total_files = len(codebase)
    total_lines = sum(file_info["lines"] for file_info in codebase.values())
    
    # Set the total codebase size
    metrics.set_total_codebase_size(files=total_files, lines=total_lines)
    print(f"Codebase: {total_files} files, {total_lines} lines of code")
    
    # Mock review of each file
    for filename, file_info in codebase.items():
        # Simulate not reviewing all files
        if random.random() > 0.7:  # 30% chance to skip a file
            print(f"Skipping review of: {filename}")
            continue
        
        # Simulate only partial review of some files
        if random.random() > 0.5:  # 50% chance of partial review
            lines_reviewed = int(file_info["lines"] * random.uniform(0.5, 0.9))
        else:
            lines_reviewed = file_info["lines"]
        
        print(f"Reviewing: {filename} ({lines_reviewed}/{file_info['lines']} lines)")
        
        # Record the file review
        metrics.record_file_review(
            filename=filename,
            lines_reviewed=lines_reviewed,
            total_lines=file_info["lines"]
        )
        
        # Decorate a function to time the file review
        @timed(metrics, category="file_review", filename=filename)
        def review_file(name, lines):
            """Simulate reviewing a file."""
            # Simulate taking time to review - more lines take longer
            sleep_time = lines / 1000 * random.uniform(0.5, 2.0)
            time.sleep(sleep_time)
            print(f"  Reviewed {name} in {sleep_time:.2f} seconds")
            return True
        
        # Perform the timed review
        review_file(filename, lines_reviewed)
        
        # Record found issues
        for issue_type, count in file_info["issues"].items():
            # Only record issues in reviewed parts of the file
            adjusted_count = int(count * (lines_reviewed / file_info["lines"]))
            
            for i in range(adjusted_count):
                # Generate a random line number within the reviewed lines
                line_number = random.randint(1, lines_reviewed)
                description = f"Sample {issue_type} issue #{i+1}"
                
                metrics.record_issue(
                    issue_type=issue_type,
                    filename=filename,
                    line_number=line_number,
                    description=description
                )
                print(f"  Found {issue_type} issue at line {line_number}: {description}")
    
    # Simulate some analysis time
    @timed(metrics, category="analysis")
    def perform_analysis():
        """Simulate performing analysis."""
        time.sleep(random.uniform(0.5, 1.5))
        return True
    
    print("\nPerforming post-review analysis...")
    perform_analysis()
    
    # Print metrics summary
    metrics.print_summary()
    
    # Export metrics to JSON
    output_file = "review_metrics.json"
    metrics.export_json(output_file)
    print(f"\nMetrics exported to {output_file}")

if __name__ == "__main__":
    main()