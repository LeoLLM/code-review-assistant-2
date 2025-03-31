#!/usr/bin/env python3
"""
Metrics visualization module for Code Review Assistant

This module provides visualization tools for the metrics collected
during code reviews, allowing users to generate various charts and
reports from metrics data.
"""

import os
import json
import argparse
from typing import Dict, List, Any, Optional, Union
import statistics

# Note: This module depends on matplotlib and will conditionally import it
# to avoid hard dependency for users who don't need visualization
try:
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def check_visualization_available():
    """Check if visualization dependencies are available.
    
    Returns:
        bool: True if visualization is available, False otherwise
    
    Raises:
        ImportError: If matplotlib is not installed
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "Visualization features require matplotlib. "
            "Install it with 'pip install matplotlib'."
        )
    return True

class MetricsVisualizer:
    """Class for visualizing code review metrics."""
    
    def __init__(self, metrics_data=None, metrics_file=None):
        """Initialize with either provided metrics data or a file path.
        
        Args:
            metrics_data: Dictionary containing metrics data
            metrics_file: Path to a JSON file containing metrics data
        
        Raises:
            ValueError: If neither metrics_data nor metrics_file is provided
        """
        if metrics_data:
            self.metrics = metrics_data
        elif metrics_file:
            with open(metrics_file, 'r') as f:
                self.metrics = json.load(f)
        else:
            raise ValueError("Either metrics_data or metrics_file must be provided")
        
        # Validate metrics data
        self._validate_metrics()
        
        # Check if visualization is available
        self._visualization_available = MATPLOTLIB_AVAILABLE
    
    def _validate_metrics(self):
        """Validate the metrics data has required fields.
        
        Raises:
            ValueError: If metrics data is missing required fields
        """
        required_keys = ["coverage", "issues", "file_metrics"]
        for key in required_keys:
            if key not in self.metrics:
                raise ValueError(f"Metrics data is missing required field: {key}")
    
    def generate_coverage_chart(self, output_file=None, show=True):
        """Generate a chart showing code coverage metrics.
        
        Args:
            output_file: Optional file path to save the chart
            show: Whether to display the chart
            
        Returns:
            None
        """
        check_visualization_available()
        
        # Extract coverage data
        coverage = self.metrics["coverage"]
        file_coverage = coverage.get("file_coverage_percent", 0)
        line_coverage = coverage.get("line_coverage_percent", 0)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Create bar chart
        coverage_types = ["Files", "Lines"]
        coverage_values = [file_coverage, line_coverage]
        colors = ["#3498db", "#2ecc71"]
        
        # Create bars
        bars = ax.bar(coverage_types, coverage_values, color=colors, width=0.5)
        
        # Add value labels on the bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontweight='bold')
        
        # Add title and labels
        ax.set_title('Code Review Coverage', fontsize=16, fontweight='bold')
        ax.set_ylabel('Coverage Percentage')
        ax.set_ylim(0, 100)  # Set y range to 0-100%
        
        # Add a goal line for reference
        ax.axhline(y=80, color='r', linestyle='--', alpha=0.7)
        ax.text(1.5, 81, 'Target: 80%', color='r', ha='center')
        
        # Add grid
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Add additional coverage info as text
        text = (f"Files Reviewed: {coverage['files_reviewed']} of {coverage['total_files']}\n"
                f"Lines Reviewed: {coverage['lines_reviewed']} of {coverage['total_lines']}")
        fig.text(0.13, 0.01, text, ha='left', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        # Save if output file provided
        if output_file:
            plt.savefig(output_file, dpi=100, bbox_inches='tight')
            print(f"Coverage chart saved to: {output_file}")
        
        # Show if requested
        if show:
            plt.show()
        else:
            plt.close()
    
    def generate_issues_chart(self, output_file=None, show=True):
        """Generate a chart showing issue distribution.
        
        Args:
            output_file: Optional file path to save the chart
            show: Whether to display the chart
            
        Returns:
            None
        """
        check_visualization_available()
        
        # Extract issues data, excluding non-category fields
        issues = {k: v for k, v in self.metrics["issues"].items() 
                 if k not in ["total", "issues_per_1000_lines"]}
        
        # Skip if no issues
        if sum(issues.values()) == 0:
            print("No issues to visualize")
            return
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Create bar chart - sort by count
        issue_types = sorted(issues.keys(), key=lambda x: issues[x], reverse=True)
        issue_counts = [issues[t] for t in issue_types]
        
        # Title case the issue types for display
        display_types = [t.title() for t in issue_types]
        
        # Define colors
        colors = {
            "security": "#e74c3c",  # Red for security issues
            "performance": "#f39c12",  # Orange for performance
            "style": "#3498db",  # Blue for style
            "logic": "#9b59b6",  # Purple for logic
            "other": "#7f8c8d"   # Gray for other
        }
        bar_colors = [colors.get(t, "#7f8c8d") for t in issue_types]
        
        # Create bar chart
        bars = ax1.bar(display_types, issue_counts, color=bar_colors)
        
        # Add value labels on the bars
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{int(height)}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom')
        
        # Add title and labels for bar chart
        ax1.set_title('Issues by Type', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Number of Issues')
        ax1.set_ylim(0, max(issue_counts) * 1.2)  # Add 20% padding
        
        # Rotate x labels if more than 3 categories
        if len(issue_types) > 3:
            plt.setp(ax1.get_xticklabels(), rotation=30, ha='right')
        
        # Add grid
        ax1.grid(True, axis='y', linestyle='--', alpha=0.5)
        
        # Pie chart showing the same data
        ax2.pie(
            issue_counts, 
            labels=display_types, 
            colors=bar_colors,
            autopct='%1.1f%%', 
            startangle=90,
            shadow=False,
            wedgeprops={'edgecolor': 'w', 'linewidth': 1}
        )
        ax2.set_title('Issue Distribution', fontsize=14, fontweight='bold')
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Add a note about total issues and issue density
        density = self.metrics["issues"].get("issues_per_1000_lines", 0)
        total = self.metrics["issues"].get("total", sum(issues.values()))
        fig.text(0.5, 0.01, 
                 f"Total: {total} issues | Density: {density:.2f} issues per 1000 lines", 
                 ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        
        # Save if output file provided
        if output_file:
            plt.savefig(output_file, dpi=100, bbox_inches='tight')
            print(f"Issues chart saved to: {output_file}")
        
        # Show if requested
        if show:
            plt.show()
        else:
            plt.close()
    
    def generate_file_issues_chart(self, output_file=None, show=True, top_n=10):
        """Generate a chart showing issues by file.
        
        Args:
            output_file: Optional file path to save the chart
            show: Whether to display the chart
            top_n: Number of top files to show
            
        Returns:
            None
        """
        check_visualization_available()
        
        # Compile issue counts by file
        file_issues = {}
        for filename, data in self.metrics["file_metrics"].items():
            if "issues" in data:
                file_issues[filename] = sum(data["issues"].values())
        
        # Skip if no files with issues
        if not file_issues:
            print("No files with issues to visualize")
            return
        
        # Sort and take top N files by issue count
        top_files = sorted(file_issues.items(), key=lambda x: x[1], reverse=True)[:top_n]
        filenames = [name for name, _ in top_files]
        issue_counts = [count for _, count in top_files]
        
        # Shorten long filenames for display
        display_names = []
        for name in filenames:
            if len(name) > 20:
                parts = name.split('/')
                if len(parts) > 1:
                    display_names.append(f".../{parts[-1]}")
                else:
                    display_names.append(f"{name[:17]}...")
            else:
                display_names.append(name)
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Create horizontal bar chart
        bars = plt.barh(display_names, issue_counts, color="#3498db")
        
        # Add value labels on the bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
                     str(int(width)), ha='left', va='center')
        
        # Add title and labels
        plt.title('Issues by File', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Issues')
        plt.gca().invert_yaxis()  # Invert to show highest count at top
        
        # Add grid
        plt.grid(True, axis='x', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        # Save if output file provided
        if output_file:
            plt.savefig(output_file, dpi=100, bbox_inches='tight')
            print(f"File issues chart saved to: {output_file}")
        
        # Show if requested
        if show:
            plt.show()
        else:
            plt.close()
    
    def generate_timing_chart(self, output_file=None, show=True):
        """Generate a chart showing timing metrics.
        
        Args:
            output_file: Optional file path to save the chart
            show: Whether to display the chart
            
        Returns:
            None
        """
        check_visualization_available()
        
        # Extract timing data
        timing = self.metrics.get("timing", {})
        
        # Skip if no timing data
        if not timing:
            print("No timing data to visualize")
            return
        
        # Calculate average timing for each category
        timing_data = {}
        for category, times in timing.items():
            timing_data[category] = sum(times) / len(times)
        
        # Sort categories by time
        categories = sorted(timing_data.keys(), key=lambda x: timing_data[x], reverse=True)
        avg_times = [timing_data[cat] for cat in categories]
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Create bar chart
        bars = plt.bar(categories, avg_times, color="#2ecc71")
        
        # Add value labels on the bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height + 0.1,
                     f'{height:.2f}s', ha='center', va='bottom')
        
        # Add title and labels
        plt.title('Average Time by Activity', fontsize=16, fontweight='bold')
        plt.ylabel('Time (seconds)')
        
        # Add grid
        plt.grid(True, axis='y', linestyle='--', alpha=0.5)
        
        # Add total review time
        total_time = self.metrics.get("total_duration_seconds", 0)
        plt.figtext(0.5, 0.01, f"Total review time: {total_time:.1f} seconds", 
                   ha="center", fontsize=10)
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1)
        
        # Save if output file provided
        if output_file:
            plt.savefig(output_file, dpi=100, bbox_inches='tight')
            print(f"Timing chart saved to: {output_file}")
        
        # Show if requested
        if show:
            plt.show()
        else:
            plt.close()
    
    def generate_summary_report(self, output_dir=None, prefix=""):
        """Generate a complete set of charts as a report.
        
        Args:
            output_dir: Directory to save charts (will be created if doesn't exist)
            prefix: Optional prefix for filenames
            
        Returns:
            List of generated filenames
        """
        check_visualization_available()
        
        # Create output directory if provided and doesn't exist
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate each chart type
        filenames = []
        
        # Coverage chart
        if output_dir:
            filename = os.path.join(output_dir, f"{prefix}coverage.png")
            self.generate_coverage_chart(output_file=filename, show=False)
            filenames.append(filename)
        else:
            self.generate_coverage_chart(show=True)
            
        # Issues chart
        if output_dir:
            filename = os.path.join(output_dir, f"{prefix}issues.png")
            self.generate_issues_chart(output_file=filename, show=False)
            filenames.append(filename)
        else:
            self.generate_issues_chart(show=True)
            
        # File issues chart
        if output_dir:
            filename = os.path.join(output_dir, f"{prefix}file_issues.png")
            self.generate_file_issues_chart(output_file=filename, show=False)
            filenames.append(filename)
        else:
            self.generate_file_issues_chart(show=True)
            
        # Timing chart
        if output_dir:
            filename = os.path.join(output_dir, f"{prefix}timing.png")
            self.generate_timing_chart(output_file=filename, show=False)
            filenames.append(filename)
        else:
            self.generate_timing_chart(show=True)
            
        return filenames
        
# Command-line interface if run directly
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code Review Metrics Visualization")
    parser.add_argument('metrics_file', help='Path to the metrics JSON file')
    parser.add_argument('--output', '-o', help='Output directory for charts', default=None)
    parser.add_argument('--prefix', '-p', help='Prefix for output filenames', default="")
    parser.add_argument('--chart', '-c', choices=['coverage', 'issues', 'files', 'timing', 'all'],
                        default='all', help='Which chart to generate')
    
    args = parser.parse_args()
    
    try:
        # Create visualizer
        visualizer = MetricsVisualizer(metrics_file=args.metrics_file)
        
        # Generate requested charts
        if args.chart == 'coverage' or args.chart == 'all':
            if args.output:
                filename = os.path.join(args.output, f"{args.prefix}coverage.png")
                visualizer.generate_coverage_chart(output_file=filename, show=False)
            else:
                visualizer.generate_coverage_chart()
        
        if args.chart == 'issues' or args.chart == 'all':
            if args.output:
                filename = os.path.join(args.output, f"{args.prefix}issues.png")
                visualizer.generate_issues_chart(output_file=filename, show=False)
            else:
                visualizer.generate_issues_chart()
        
        if args.chart == 'files' or args.chart == 'all':
            if args.output:
                filename = os.path.join(args.output, f"{args.prefix}file_issues.png")
                visualizer.generate_file_issues_chart(output_file=filename, show=False)
            else:
                visualizer.generate_file_issues_chart()
        
        if args.chart == 'timing' or args.chart == 'all':
            if args.output:
                filename = os.path.join(args.output, f"{args.prefix}timing.png")
                visualizer.generate_timing_chart(output_file=filename, show=False)
            else:
                visualizer.generate_timing_chart()
        
    except ImportError as e:
        print(f"Error: {e}")
        print("To use visualization features, install matplotlib with:")
        print("pip install matplotlib")
        
    except Exception as e:
        print(f"Error: {e}")