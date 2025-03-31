#!/usr/bin/env python3
"""
Unit tests for the metrics module
"""

import os
import sys
import json
import time
import unittest
import tempfile
from datetime import datetime

# Add parent directory to path to allow importing metrics module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from metrics import Metrics, timed

class TestMetrics(unittest.TestCase):
    """Test cases for the Metrics class and related functionality."""
    
    def setUp(self):
        """Set up a new metrics instance before each test."""
        self.metrics = Metrics()
    
    def test_initialization(self):
        """Test that a new Metrics instance is initialized with correct defaults."""
        metrics_data = self.metrics.get_metrics()
        
        # Check that required keys exist
        self.assertIn("review_start_time", metrics_data)
        self.assertIn("timing", metrics_data)
        self.assertIn("coverage", metrics_data)
        self.assertIn("issues", metrics_data)
        self.assertIn("file_metrics", metrics_data)
        
        # Check coverage defaults
        self.assertEqual(metrics_data["coverage"]["files_reviewed"], 0)
        self.assertEqual(metrics_data["coverage"]["lines_reviewed"], 0)
        self.assertEqual(metrics_data["coverage"]["total_files"], 0)
        self.assertEqual(metrics_data["coverage"]["total_lines"], 0)
        
        # Check issues defaults
        self.assertEqual(metrics_data["issues"]["security"], 0)
        self.assertEqual(metrics_data["issues"]["performance"], 0)
        self.assertEqual(metrics_data["issues"]["style"], 0)
        self.assertEqual(metrics_data["issues"]["logic"], 0)
        self.assertEqual(metrics_data["issues"]["other"], 0)
    
    def test_record_file_review(self):
        """Test recording metrics for a reviewed file."""
        self.metrics.record_file_review("test.py", 100, 150)
        metrics_data = self.metrics.get_metrics()
        
        self.assertEqual(metrics_data["coverage"]["files_reviewed"], 1)
        self.assertEqual(metrics_data["coverage"]["lines_reviewed"], 100)
        
        # Check file-specific metrics
        self.assertIn("test.py", metrics_data["file_metrics"])
        self.assertEqual(metrics_data["file_metrics"]["test.py"]["lines_reviewed"], 100)
        self.assertEqual(metrics_data["file_metrics"]["test.py"]["total_lines"], 150)
        self.assertAlmostEqual(metrics_data["file_metrics"]["test.py"]["coverage_percent"], 66.67, places=2)
    
    def test_set_total_codebase_size(self):
        """Test setting total codebase size."""
        self.metrics.set_total_codebase_size(10, 5000)
        metrics_data = self.metrics.get_metrics()
        
        self.assertEqual(metrics_data["coverage"]["total_files"], 10)
        self.assertEqual(metrics_data["coverage"]["total_lines"], 5000)
    
    def test_record_issue(self):
        """Test recording an issue."""
        # First record a file so we can associate issues with it
        self.metrics.record_file_review("test.py", 100, 150)
        
        # Record issues
        self.metrics.record_issue("security", "test.py", 42, "Security vulnerability")
        self.metrics.record_issue("style", "test.py", 50, "Style issue")
        self.metrics.record_issue("unknown_type", "test.py", 60, "Unknown issue type")
        
        metrics_data = self.metrics.get_metrics()
        
        # Check that issues are correctly counted
        self.assertEqual(metrics_data["issues"]["security"], 1)
        self.assertEqual(metrics_data["issues"]["style"], 1)
        self.assertEqual(metrics_data["issues"]["other"], 1)  # Unknown type goes to "other"
        self.assertEqual(metrics_data["issues"]["total"], 3)
        
        # Check file-specific issue counts
        self.assertEqual(metrics_data["file_metrics"]["test.py"]["issues"]["security"], 1)
        self.assertEqual(metrics_data["file_metrics"]["test.py"]["issues"]["style"], 1)
        self.assertEqual(metrics_data["file_metrics"]["test.py"]["issues"]["other"], 1)
        
        # Check issue details
        self.assertIn("issue_details", metrics_data["file_metrics"]["test.py"])
        self.assertEqual(len(metrics_data["file_metrics"]["test.py"]["issue_details"]), 3)
        
        # Check a specific issue
        security_issue = next(
            (i for i in metrics_data["file_metrics"]["test.py"]["issue_details"] 
             if i["type"] == "security"), None
        )
        self.assertIsNotNone(security_issue)
        self.assertEqual(security_issue["line"], 42)
        self.assertEqual(security_issue["description"], "Security vulnerability")
    
    def test_coverage_percentage_calculation(self):
        """Test calculation of coverage percentages."""
        self.metrics.set_total_codebase_size(10, 1000)
        self.metrics.record_file_review("test1.py", 75, 100)
        self.metrics.record_file_review("test2.py", 150, 200)
        
        metrics_data = self.metrics.get_metrics()
        
        # 2 out of 10 files = 20%
        self.assertEqual(metrics_data["coverage"]["file_coverage_percent"], 20.0)
        
        # 225 out of 1000 lines = 22.5%
        self.assertEqual(metrics_data["coverage"]["line_coverage_percent"], 22.5)
    
    def test_issues_per_line_calculation(self):
        """Test calculation of issues per 1000 lines."""
        self.metrics.record_file_review("test.py", 1000, 1000)
        
        # Add 5 issues
        for i in range(5):
            self.metrics.record_issue("security", "test.py", i+1, f"Issue {i+1}")
        
        metrics_data = self.metrics.get_metrics()
        
        # 5 issues per 1000 lines = 5.0
        self.assertEqual(metrics_data["issues"]["issues_per_1000_lines"], 5.0)
    
    def test_export_json(self):
        """Test exporting metrics to JSON."""
        self.metrics.record_file_review("test.py", 100, 150)
        self.metrics.record_issue("security", "test.py", 42, "Security issue")
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            try:
                # Export to the temporary file
                self.metrics.export_json(temp_file.name)
                
                # Read back and verify
                with open(temp_file.name, 'r') as f:
                    loaded_metrics = json.load(f)
                
                self.assertEqual(loaded_metrics["coverage"]["files_reviewed"], 1)
                self.assertEqual(loaded_metrics["coverage"]["lines_reviewed"], 100)
                self.assertEqual(loaded_metrics["issues"]["security"], 1)
            finally:
                # Clean up
                os.unlink(temp_file.name)
    
    def test_timing_decorator(self):
        """Test the timing decorator."""
        @timed(self.metrics, category="test", filename="test.py")
        def sample_function():
            time.sleep(0.1)
            return 42
        
        # First record the file so we can associate timing with it
        self.metrics.record_file_review("test.py", 100, 150)
        
        # Call the decorated function
        result = sample_function()
        self.assertEqual(result, 42)
        
        metrics_data = self.metrics.get_metrics()
        
        # Check that timing was recorded
        self.assertIn("test", metrics_data["timing"])
        self.assertEqual(len(metrics_data["timing"]["test"]), 1)
        
        # Time should be approximately 0.1 seconds, but allow some margin
        timing = metrics_data["timing"]["test"][0]
        self.assertGreaterEqual(timing, 0.05)
        self.assertLessEqual(timing, 0.2)
        
        # Check that file timing was recorded
        self.assertIsNotNone(metrics_data["file_metrics"]["test.py"]["review_time"])
        self.assertGreaterEqual(metrics_data["file_metrics"]["test.py"]["review_time"], 0.05)
        self.assertLessEqual(metrics_data["file_metrics"]["test.py"]["review_time"], 0.2)

if __name__ == '__main__':
    unittest.main()