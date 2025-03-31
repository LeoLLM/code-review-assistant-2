#!/usr/bin/env python3
"""
Example script demonstrating the usage of the metrics visualization module
in the Code Review Assistant.

This example generates sample metrics data similar to what would be produced
during a real code review, then shows how to visualize it using the
metrics_viz module.
"""

import os
import sys
import json
import tempfile
import random
from datetime import datetime, timedelta

# Add parent directory to path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our metrics modules
from metrics import Metrics
from metrics_viz import MetricsVisualizer, check_visualization_available

def generate_sample_metrics():
    """Generate a sample metrics dataset for visualization demo."""
    metrics = Metrics()
    
    # Set codebase size
    total_files = 25
    total_lines = 8500
    metrics.set_total_codebase_size(total_files, total_lines)
    
    # Define some sample files with varying sizes
    sample_files = {
        "main.py": 250,
        "utils.py": 350,
        "api.py": 420,
        "models.py": 580,
        "views/user_view.py": 320,
        "views/admin_view.py": 280,
        "tests/test_api.py": 210,
        "tests/test_models.py": 310,
        "config.py": 70,
        "database.py": 430,
        "auth.py": 280,
        "logging.py": 150,
        "templates/base.py": 60,
        "exceptions.py": 90,
    }
    
    # Record reviews for some files (simulating partial coverage)
    for filename, total_lines in sample_files.items():
        # 80% chance of reviewing each file
        if random.random() < 0.8:
            # Vary the coverage for each file
            coverage_percent = random.uniform(0.5, 1.0)
            lines_reviewed = int(total_lines * coverage_percent)
            
            # Record the file review
            metrics.record_file_review(filename, lines_reviewed, total_lines)
            
            # Record timing for each file review (more lines = more time)
            # Store this directly in the metrics data structure since we're not
            # using the timing decorator in this simulation
            base_time = lines_reviewed / 100  # base time proportional to lines
            variation = random.uniform(0.8, 1.2)  # +/- 20% variation
            review_time = base_time * variation
            
            if "timing" not in metrics._metrics:
                metrics._metrics["timing"] = {}
            
            if "file_review" not in metrics._metrics["timing"]:
                metrics._metrics["timing"]["file_review"] = []
            
            metrics._metrics["timing"]["file_review"].append(review_time)
            metrics._metrics["file_metrics"][filename]["review_time"] = review_time
            
            # Simulate finding issues in the file
            security_issues = random.randint(0, 2)
            performance_issues = random.randint(0, 3)
            style_issues = random.randint(0, 5)
            logic_issues = random.randint(0, 2)
            
            # Record the issues
            for i in range(security_issues):
                line = random.randint(1, lines_reviewed)
                metrics.record_issue("security", filename, line, f"Security issue {i+1}")
                
            for i in range(performance_issues):
                line = random.randint(1, lines_reviewed)
                metrics.record_issue("performance", filename, line, f"Performance issue {i+1}")
                
            for i in range(style_issues):
                line = random.randint(1, lines_reviewed)
                metrics.record_issue("style", filename, line, f"Style issue {i+1}")
                
            for i in range(logic_issues):
                line = random.randint(1, lines_reviewed)
                metrics.record_issue("logic", filename, line, f"Logic issue {i+1}")
    
    # Add some timing data for other activities
    activities = {
        "parsing": (1.5, 3.0),  # min and max seconds
        "analysis": (3.0, 8.0),
        "reporting": (2.0, 4.0),
        "planning": (1.0, 2.0)
    }
    
    for activity, (min_time, max_time) in activities.items():
        # Generate 2-5 timing entries for each activity
        for _ in range(random.randint(2, 5)):
            time_spent = random.uniform(min_time, max_time)
            
            if activity not in metrics._metrics["timing"]:
                metrics._metrics["timing"][activity] = []
                
            metrics._metrics["timing"][activity].append(time_spent)
    
    # Set review time range
    # Start time is 1-3 hours ago
    hours_ago = random.uniform(1, 3)
    start_time = datetime.now() - timedelta(hours=hours_ago)
    metrics._metrics["review_start_time"] = start_time.isoformat()
    
    # Force recalculation of derived metrics
    return metrics.get_metrics()

def main():
    """Run a demo of metrics visualization."""
    try:
        # Check if visualization is available
        check_visualization_available()
        
        print("Generating sample metrics data...")
        metrics_data = generate_sample_metrics()
        
        # Create a temporary file to store the metrics
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            json.dump(metrics_data, tmp, indent=2)
            metrics_file = tmp.name
        
        print(f"Sample metrics saved to: {metrics_file}")
        
        # Create the visualizer
        print("Creating visualizer...")
        visualizer = MetricsVisualizer(metrics_file=metrics_file)
        
        # Generate and save all charts to a directory
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"Generating charts in '{output_dir}' directory...")
        files = visualizer.generate_summary_report(output_dir=output_dir, prefix="demo_")
        
        print("\nGenerated chart files:")
        for f in files:
            print(f"- {f}")
        
        # Also show charts interactively
        print("\nShowing charts interactively...")
        visualizer.generate_coverage_chart()
        visualizer.generate_issues_chart()
        visualizer.generate_file_issues_chart()
        visualizer.generate_timing_chart()
        
        # Clean up the temporary file
        os.unlink(metrics_file)
        
    except ImportError as e:
        print(f"Error: {e}")
        print("\nTo run this example, you need to install matplotlib:")
        print("pip install matplotlib")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()