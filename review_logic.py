#!/usr/bin/env python3
"""
Review Logic Module for Code Review Assistant
This module provides automated code review functionality
"""

import os
import re
import ast
import logging
from typing import List, Dict, Any, Optional, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CodeReviewer:
    """Main class for performing automated code reviews"""
    
    def __init__(self, template_path: str = None):
        """
        Initialize the code reviewer
        
        Args:
            template_path: Path to the review template directory
        """
        self.template_path = template_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            'review_templates'
        )
        self.issues = []
        self.stats = {
            'files_reviewed': 0,
            'issues_found': 0,
            'issue_types': {}
        }
    
    def load_template(self, template_name: str) -> Dict[str, Any]:
        """
        Load a review template by name
        
        Args:
            template_name: Name of the template to load (without extension)
            
        Returns:
            Dictionary containing the parsed template
        """
        template_file = os.path.join(self.template_path, f"{template_name}.md")
        try:
            with open(template_file, 'r') as f:
                content = f.read()
                
            # Parse markdown template into structured format
            sections = self._parse_template(content)
            return sections
        except FileNotFoundError:
            logger.error(f"Template {template_name} not found at {template_file}")
            return {}
    
    def _parse_template(self, content: str) -> Dict[str, List[str]]:
        """
        Parse a markdown template into structured sections
        
        Args:
            content: Markdown content to parse
            
        Returns:
            Dictionary with section names as keys and lists of checklist items
        """
        sections = {}
        current_section = None
        
        for line in content.split('\n'):
            if line.startswith('## '):
                # New section
                current_section = line[3:].strip()
                sections[current_section] = []
            elif line.startswith('- [ ] ') and current_section:
                # Checklist item
                item = line[6:].strip()
                sections[current_section].append(item)
                
        return sections
    
    def review_file(self, file_path: str, template_name: str = 'general') -> List[Dict[str, Any]]:
        """
        Review a single file using the specified template
        
        Args:
            file_path: Path to the file to review
            template_name: Name of the template to use
            
        Returns:
            List of issues found during review
        """
        self.issues = []
        template = self.load_template(template_name)
        
        if not template:
            logger.error(f"Failed to load template {template_name}")
            return []
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Run different checks based on file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.py':
                self._review_python_file(file_path, content, template)
            elif file_ext in ['.js', '.ts']:
                self._review_javascript_file(file_path, content, template)
            else:
                # Generic review for other file types
                self._review_generic_file(file_path, content, template)
                
            # Update statistics
            self.stats['files_reviewed'] += 1
            self.stats['issues_found'] += len(self.issues)
            
            # Update issue type counts
            for issue in self.issues:
                category = issue.get('category', 'Other')
                self.stats['issue_types'][category] = self.stats['issue_types'].get(category, 0) + 1
                
            return self.issues
                
        except Exception as e:
            logger.error(f"Error reviewing file {file_path}: {str(e)}")
            return []
    
    def _review_python_file(self, file_path: str, content: str, template: Dict[str, List[str]]) -> None:
        """
        Review a Python file using AST and regex patterns
        
        Args:
            file_path: Path to the file
            content: File content
            template: Loaded template dictionary
        """
        try:
            # Parse file into AST
            tree = ast.parse(content)
            
            # Check for hardcoded credentials
            self._check_hardcoded_credentials(file_path, content)
            
            # Check for proper docstrings
            self._check_docstrings(file_path, tree)
            
            # Check for consistent naming conventions
            self._check_naming_conventions(file_path, tree)
            
            # Check for complex functions (cyclomatic complexity)
            self._check_function_complexity(file_path, tree)
            
        except SyntaxError as e:
            self.issues.append({
                'file': file_path,
                'line': e.lineno,
                'category': 'Syntax',
                'severity': 'High',
                'message': f"Syntax error: {str(e)}"
            })
    
    def _review_javascript_file(self, file_path: str, content: str, template: Dict[str, List[str]]) -> None:
        """
        Review a JavaScript or TypeScript file using regex patterns
        
        Args:
            file_path: Path to the file
            content: File content
            template: Loaded template dictionary
        """
        # Check for console.log statements
        self._check_console_logs(file_path, content)
        
        # Check for hardcoded credentials
        self._check_hardcoded_credentials(file_path, content)
    
    def _review_generic_file(self, file_path: str, content: str, template: Dict[str, List[str]]) -> None:
        """
        Review a generic file using basic checks
        
        Args:
            file_path: Path to the file
            content: File content
            template: Loaded template dictionary
        """
        # Check for overly long lines
        self._check_line_length(file_path, content)
        
        # Check for trailing whitespace
        self._check_trailing_whitespace(file_path, content)
    
    # Various check methods
    def _check_hardcoded_credentials(self, file_path: str, content: str) -> None:
        """Check for hardcoded credentials"""
        patterns = [
            r'password\s*=\s*["\']([^"\']+)["\']',
            r'api_?key\s*=\s*["\']([^"\']+)["\']',
            r'secret\s*=\s*["\']([^"\']+)["\']',
            r'token\s*=\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_no = content.count('\n', 0, match.start()) + 1
                self.issues.append({
                    'file': file_path,
                    'line': line_no,
                    'category': 'Security',
                    'severity': 'High',
                    'message': "Potential hardcoded credential detected"
                })
    
    def _check_docstrings(self, file_path: str, tree: ast.AST) -> None:
        """Check for missing or inadequate docstrings"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                has_docstring = False
                if (node.body and isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Str)):
                    has_docstring = True
                
                if not has_docstring and not (isinstance(node, ast.FunctionDef) and node.name.startswith('_')):
                    node_type = 'function' if isinstance(node, ast.FunctionDef) else 'class'
                    node_name = getattr(node, 'name', 'module')
                    
                    self.issues.append({
                        'file': file_path,
                        'line': node.lineno,
                        'category': 'Documentation',
                        'severity': 'Medium',
                        'message': f"Missing docstring for {node_type} '{node_name}'"
                    })
    
    def _check_naming_conventions(self, file_path: str, tree: ast.AST) -> None:
        """Check for consistent naming conventions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Class names should be CamelCase
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    self.issues.append({
                        'file': file_path,
                        'line': node.lineno,
                        'category': 'Style',
                        'severity': 'Low',
                        'message': f"Class '{node.name}' doesn't follow CamelCase naming convention"
                    })
            elif isinstance(node, ast.FunctionDef):
                # Function names should be snake_case
                if not node.name.startswith('__') and not re.match(r'^[a-z][a-z0-9_]*$', node.name):
                    self.issues.append({
                        'file': file_path,
                        'line': node.lineno,
                        'category': 'Style',
                        'severity': 'Low',
                        'message': f"Function '{node.name}' doesn't follow snake_case naming convention"
                    })
    
    def _check_function_complexity(self, file_path: str, tree: ast.AST) -> None:
        """Check for overly complex functions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                if complexity > 10:
                    self.issues.append({
                        'file': file_path,
                        'line': node.lineno,
                        'category': 'Maintainability',
                        'severity': 'Medium',
                        'message': f"Function '{node.name}' has high cyclomatic complexity ({complexity})"
                    })
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity
        
        # Count branching statements
        for subnode in ast.walk(node):
            if isinstance(subnode, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(subnode, ast.BoolOp) and isinstance(subnode.op, ast.And):
                complexity += len(subnode.values) - 1
        
        return complexity
    
    def _check_console_logs(self, file_path: str, content: str) -> None:
        """Check for console.log statements in JS/TS"""
        pattern = r'console\.log\('
        
        for match in re.finditer(pattern, content):
            line_no = content.count('\n', 0, match.start()) + 1
            self.issues.append({
                'file': file_path,
                'line': line_no,
                'category': 'Debug',
                'severity': 'Low',
                'message': "console.log statement should be removed in production code"
            })
    
    def _check_line_length(self, file_path: str, content: str) -> None:
        """Check for overly long lines"""
        max_length = 100
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if len(line) > max_length:
                self.issues.append({
                    'file': file_path,
                    'line': i + 1,
                    'category': 'Style',
                    'severity': 'Low',
                    'message': f"Line exceeds {max_length} characters (length: {len(line)})"
                })
    
    def _check_trailing_whitespace(self, file_path: str, content: str) -> None:
        """Check for trailing whitespace"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line and line[-1].isspace():
                self.issues.append({
                    'file': file_path,
                    'line': i + 1,
                    'category': 'Style',
                    'severity': 'Low',
                    'message': "Line has trailing whitespace"
                })
    
    def generate_review_report(self, issues: List[Dict[str, Any]] = None) -> str:
        """
        Generate a markdown report from review issues
        
        Args:
            issues: List of issues to include in report, or None to use self.issues
            
        Returns:
            Markdown formatted review report
        """
        issues = issues or self.issues
        
        if not issues:
            return "# Code Review Report\n\nNo issues found in the code review."
        
        # Group issues by file
        issues_by_file = {}
        for issue in issues:
            file_path = issue.get('file', 'Unknown')
            if file_path not in issues_by_file:
                issues_by_file[file_path] = []
            issues_by_file[file_path].append(issue)
        
        # Generate report
        report = ["# Code Review Report\n"]
        
        # Summary section
        report.append("## Summary\n")
        report.append(f"- Files reviewed: {self.stats['files_reviewed']}")
        report.append(f"- Total issues found: {self.stats['issues_found']}")
        
        # Issues by category
        report.append("\n### Issues by Category\n")
        for category, count in self.stats['issue_types'].items():
            report.append(f"- {category}: {count}")
        
        # Detailed issues by file
        report.append("\n## Detailed Findings\n")
        for file_path, file_issues in issues_by_file.items():
            report.append(f"### File: `{file_path}`\n")
            
            # Group by severity
            severity_order = ['High', 'Medium', 'Low']
            for severity in severity_order:
                severity_issues = [i for i in file_issues if i.get('severity') == severity]
                
                if severity_issues:
                    report.append(f"#### {severity} Severity Issues\n")
                    
                    for issue in severity_issues:
                        line = issue.get('line', 'Unknown')
                        category = issue.get('category', 'Other')
                        message = issue.get('message', 'No description')
                        
                        report.append(f"- **Line {line}** ({category}): {message}")
                    
                    report.append("")  # Empty line for spacing
        
        return "\n".join(report)

def main():
    """Main function for running the code reviewer"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Code Review Tool')
    parser.add_argument('path', help='Path to file or directory to review')
    parser.add_argument('--template', '-t', default='general', 
                        help='Template to use for review (general, security, performance)')
    parser.add_argument('--output', '-o', help='Output file for review report')
    
    args = parser.parse_args()
    
    reviewer = CodeReviewer()
    
    if os.path.isfile(args.path):
        # Review single file
        issues = reviewer.review_file(args.path, args.template)
        report = reviewer.generate_review_report(issues)
    elif os.path.isdir(args.path):
        # Review all files in directory
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.html', '.css')):
                    file_path = os.path.join(root, file)
                    reviewer.review_file(file_path, args.template)
        
        report = reviewer.generate_review_report()
    else:
        logger.error(f"Path not found: {args.path}")
        return
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        logger.info(f"Review report written to {args.output}")
    else:
        print(report)

if __name__ == "__main__":
    main()