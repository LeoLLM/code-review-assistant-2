#!/usr/bin/env python3
"""
Metrics collection and analysis module for Code Review Assistant

This module provides functionality to track and analyze various metrics
during code reviews, including timing information, coverage stats, and
issue tracking.
"""

import time
import json
import functools
import statistics
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Union, TypeVar

# Type definitions
F = TypeVar('F', bound=Callable[..., Any])
Metric = Dict[str, Any]
MetricCollection = Dict[str, Metric]

class Metrics:
    """Class for collecting and managing code review metrics."""
    
    def __init__(self):
        """Initialize an empty metrics collection."""
        self._metrics: MetricCollection = {
            "review_start_time": datetime.now().isoformat(),
            "timing": {},
            "coverage": {
                "files_reviewed": 0,
                "lines_reviewed": 0,
                "total_files": 0,
                "total_lines": 0,
            },
            "issues": {
                "security": 0,
                "performance": 0,
                "style": 0,
                "logic": 0,
                "other": 0,
            },
            "file_metrics": {},
        }
    
    def record_file_review(self, filename: str, lines_reviewed: int, total_lines: int) -> None:
        """Record metrics for a reviewed file.
        
        Args:
            filename: Name of the file reviewed
            lines_reviewed: Number of lines reviewed in the file
            total_lines: Total lines in the file
        """
        self._metrics["coverage"]["files_reviewed"] += 1
        self._metrics["coverage"]["lines_reviewed"] += lines_reviewed
        
        # Store per-file metrics
        self._metrics["file_metrics"][filename] = {
            "lines_reviewed": lines_reviewed,
            "total_lines": total_lines,
            "coverage_percent": (lines_reviewed / total_lines * 100) if total_lines > 0 else 100,
            "review_time": None,  # Will be set by timing decorator
            "issues": {
                "security": 0,
                "performance": 0,
                "style": 0,
                "logic": 0,
                "other": 0,
            }
        }
    
    def set_total_codebase_size(self, files: int, lines: int) -> None:
        """Set the total size of the codebase being reviewed.
        
        Args:
            files: Total number of files in the codebase
            lines: Total number of lines of code in the codebase
        """
        self._metrics["coverage"]["total_files"] = files
        self._metrics["coverage"]["total_lines"] = lines
    
    def record_issue(self, issue_type: str, filename: str, 
                     line_number: Optional[int] = None, 
                     description: Optional[str] = None) -> None:
        """Record an issue found during review.
        
        Args:
            issue_type: Type of issue (security, performance, style, logic, other)
            filename: File where the issue was found
            line_number: Line number where the issue was found
            description: Description of the issue
        """
        if issue_type not in self._metrics["issues"]:
            issue_type = "other"
            
        self._metrics["issues"][issue_type] += 1
        
        # Also record in per-file metrics
        if filename in self._metrics["file_metrics"]:
            self._metrics["file_metrics"][filename]["issues"][issue_type] += 1
            
            # Add to issue list if we're tracking details
            if line_number or description:
                if "issue_details" not in self._metrics["file_metrics"][filename]:
                    self._metrics["file_metrics"][filename]["issue_details"] = []
                
                self._metrics["file_metrics"][filename]["issue_details"].append({
                    "type": issue_type,
                    "line": line_number,
                    "description": description
                })
    
    def get_metrics(self) -> MetricCollection:
        """Return the current metrics.
        
        Returns:
            Dictionary containing all collected metrics
        """
        # Calculate derived metrics
        metrics = self._metrics.copy()
        
        # Add coverage percentages
        if metrics["coverage"]["total_files"] > 0:
            metrics["coverage"]["file_coverage_percent"] = (
                metrics["coverage"]["files_reviewed"] / metrics["coverage"]["total_files"] * 100
            )
        else:
            metrics["coverage"]["file_coverage_percent"] = 0
            
        if metrics["coverage"]["total_lines"] > 0:
            metrics["coverage"]["line_coverage_percent"] = (
                metrics["coverage"]["lines_reviewed"] / metrics["coverage"]["total_lines"] * 100
            )
        else:
            metrics["coverage"]["line_coverage_percent"] = 0
        
        # Add total issues count
        metrics["issues"]["total"] = sum(metrics["issues"].values())
        
        # Add issues per line metric (issue density)
        if metrics["coverage"]["lines_reviewed"] > 0:
            metrics["issues"]["issues_per_1000_lines"] = (
                metrics["issues"]["total"] / metrics["coverage"]["lines_reviewed"] * 1000
            )
        else:
            metrics["issues"]["issues_per_1000_lines"] = 0
        
        # Add review end time and total duration
        metrics["review_end_time"] = datetime.now().isoformat()
        start_time = datetime.fromisoformat(metrics["review_start_time"])
        end_time = datetime.fromisoformat(metrics["review_end_time"])
        metrics["total_duration_seconds"] = (end_time - start_time).total_seconds()
        
        return metrics
    
    def export_json(self, file_path: str) -> None:
        """Export metrics to a JSON file.
        
        Args:
            file_path: Path to the output JSON file
        """
        with open(file_path, 'w') as f:
            json.dump(self.get_metrics(), f, indent=2)
    
    def print_summary(self) -> None:
        """Print a summary of the metrics to the console."""
        metrics = self.get_metrics()
        
        print("\n===== CODE REVIEW METRICS SUMMARY =====")
        print(f"Review duration: {metrics['total_duration_seconds']:.1f} seconds")
        print(f"Files reviewed: {metrics['coverage']['files_reviewed']} of {metrics['coverage']['total_files']} "
              f"({metrics['coverage']['file_coverage_percent']:.1f}%)")
        print(f"Lines reviewed: {metrics['coverage']['lines_reviewed']} of {metrics['coverage']['total_lines']} "
              f"({metrics['coverage']['line_coverage_percent']:.1f}%)")
        
        print("\nIssues found:")
        for issue_type, count in metrics["issues"].items():
            if issue_type != "total" and issue_type != "issues_per_1000_lines":
                print(f"  - {issue_type.capitalize()}: {count}")
        
        print(f"Total issues: {metrics['issues']['total']}")
        print(f"Issue density: {metrics['issues']['issues_per_1000_lines']:.2f} issues per 1000 lines")
        
        if metrics["file_metrics"]:
            print("\nTop files by issue count:")
            # Sort files by total issues
            file_issues = []
            for filename, file_data in metrics["file_metrics"].items():
                total_issues = sum(file_data["issues"].values())
                if total_issues > 0:
                    file_issues.append((filename, total_issues))
            
            # Display top 5 files or fewer
            for filename, count in sorted(file_issues, key=lambda x: x[1], reverse=True)[:5]:
                print(f"  - {filename}: {count} issues")


# Timing decorator for measuring function execution time
def timed(metrics_instance: Metrics, category: str, filename: Optional[str] = None) -> Callable[[F], F]:
    """Decorator to time function execution and record it in metrics.
    
    Args:
        metrics_instance: Metrics instance to record timing
        category: Category name for the timing (e.g., 'parsing', 'analysis')
        filename: Optional filename if timing a file-specific operation
    
    Returns:
        Decorated function with timing
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            
            # Record in general timing metrics
            if category not in metrics_instance._metrics["timing"]:
                metrics_instance._metrics["timing"][category] = []
            
            metrics_instance._metrics["timing"][category].append(elapsed_time)
            
            # If this is for a specific file, record in file metrics
            if filename and filename in metrics_instance._metrics["file_metrics"]:
                metrics_instance._metrics["file_metrics"][filename]["review_time"] = elapsed_time
            
            return result
        return wrapper  # type: ignore
    return decorator


# Global metrics instance
_global_metrics = Metrics()

def get_metrics_instance() -> Metrics:
    """Get the global metrics instance.
    
    Returns:
        Global metrics instance
    """
    return _global_metrics


# Command-line interface if run directly
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Code Review Metrics Tool")
    parser.add_argument('--export', type=str, help='Export metrics to specified JSON file')
    args = parser.parse_args()
    
    # Example usage
    metrics = get_metrics_instance()
    metrics.set_total_codebase_size(files=10, lines=5000)
    
    # Simulate some file reviews
    metrics.record_file_review("example.py", lines_reviewed=100, total_lines=120)
    metrics.record_issue("style", "example.py", 25, "Inconsistent indentation")
    metrics.record_issue("security", "example.py", 42, "Potential SQL injection")
    
    metrics.record_file_review("utils.py", lines_reviewed=200, total_lines=250)
    metrics.record_issue("performance", "utils.py", 15, "Inefficient algorithm")
    
    # Print summary
    metrics.print_summary()
    
    # Export if requested
    if args.export:
        metrics.export_json(args.export)
        print(f"Metrics exported to {args.export}")