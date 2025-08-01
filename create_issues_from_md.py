#!/usr/bin/env python3
"""
Script to create Jira issues from a markdown file using jira-cli.
Supports dry-run mode to preview commands before execution.
"""

import re
import argparse
import subprocess
import json
import sys
from pathlib import Path


def parse_markdown_file(file_path):
    """Parse the markdown file and extract issue details."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split by issue headers
    issue_pattern = r'### \*\*Jira Issue \d+\*\*'
    issues = re.split(issue_pattern, content)[1:]  # Skip content before first issue
    
    parsed_issues = []
    
    for issue_text in issues:
        issue_data = {}
        
        # Extract Priority
        priority_match = re.search(r'\* \*\*Priority:\*\* (.+)', issue_text)
        if priority_match:
            issue_data['priority'] = priority_match.group(1).strip()
        
        # Extract Summary
        summary_match = re.search(r'\* \*\*Summary:\*\* (.+)', issue_text)
        if summary_match:
            issue_data['summary'] = summary_match.group(1).strip()
        
        # Extract Description
        desc_match = re.search(r'\* \*\*Description:\*\*\s*\n((?:\s+\* .+\n?)+)', issue_text)
        if desc_match:
            desc_lines = desc_match.group(1).strip().split('\n')
            # Clean up the description lines
            clean_lines = []
            for line in desc_lines:
                # Remove leading whitespace and bullet points
                cleaned = re.sub(r'^\s*\*\s*', '', line)
                if cleaned:
                    clean_lines.append(cleaned)
            issue_data['description'] = '\n'.join(clean_lines)
        
        # Skip assignee as requested
        
        if all(key in issue_data for key in ['priority', 'summary', 'description']):
            parsed_issues.append(issue_data)
    
    return parsed_issues


def build_jira_cli_command(issue, project_key, issue_type, label=None):
    """Build the jira-cli command for creating an issue."""
    cmd = [
        'jira-cli', 'create',
        '--project', project_key,
        '--summary', issue['summary'],
        '--type', issue_type,
        '--description', issue['description']
    ]
    
    # Add priority and label as custom fields
    fields = {
        'priority': {'name': issue['priority']}
    }
    
    if label:
        fields['labels'] = [label]
    
    cmd.extend(['--fields', json.dumps(fields)])
    
    return cmd


def main():
    parser = argparse.ArgumentParser(description='Create Jira issues from markdown file')
    parser.add_argument('markdown_file', help='Path to the markdown file containing issues')
    parser.add_argument('--project', '-p', required=True, help='Jira project key')
    parser.add_argument('--type', '-t', default='Task', help='Issue type (default: Task)')
    parser.add_argument('--label', '-l', help='Label to add to all issues')
    parser.add_argument('--dry-run', '-n', action='store_true', 
                        help='Show commands without executing them')
    parser.add_argument('--save-script', '-s', help='Save commands to a shell script file')
    
    args = parser.parse_args()
    
    # Check if markdown file exists
    if not Path(args.markdown_file).exists():
        print(f"Error: File '{args.markdown_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Parse the markdown file
    print(f"Parsing {args.markdown_file}...")
    issues = parse_markdown_file(args.markdown_file)
    print(f"Found {len(issues)} issues to create\n")
    
    if not issues:
        print("No issues found in the markdown file")
        return
    
    # Open script file if requested
    script_file = None
    if args.save_script:
        script_file = open(args.save_script, 'w')
        script_file.write('#!/bin/bash\n')
        script_file.write('# Script generated from ' + args.markdown_file + '\n')
        script_file.write('# Run this script to create all Jira issues\n\n')
        script_file.write('set -e  # Exit on first error\n\n')
    
    # Process each issue
    for i, issue in enumerate(issues, 1):
        print(f"{'='*60}")
        print(f"Issue {i}/{len(issues)}")
        print(f"Priority: {issue['priority']}")
        print(f"Summary: {issue['summary']}")
        print(f"Description preview: {issue['description'][:100]}...")
        if args.label:
            print(f"Label: {args.label}")
        
        # Build the command
        cmd = build_jira_cli_command(issue, args.project, args.type, args.label)
        
        if args.dry_run:
            # In dry-run mode, show the command
            print(f"\nCommand that would be executed:")
            # Create a shell-escaped version for display
            escaped_cmd = []
            for arg in cmd:
                if ' ' in arg or '\n' in arg or '"' in arg or '`' in arg:
                    # Escape quotes and backticks for shell
                    escaped_arg = arg.replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$')
                    escaped_cmd.append(f'"{escaped_arg}"')
                else:
                    escaped_cmd.append(arg)
            print(' '.join(escaped_cmd))
            print()
            
            # Save to script file if requested
            if script_file:
                script_file.write(f'echo "Creating issue {i}/{len(issues)}..."\n')
                script_file.write(' '.join(escaped_cmd) + '\n')
                script_file.write('echo "Issue created successfully"\n\n')
        else:
            # Execute the command
            print(f"\nCreating issue...")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
                if result.returncode == 0:
                    print(f"✓ Success: {result.stdout}")
                else:
                    print(f"✗ Error: {result.stderr}")
            except Exception as e:
                print(f"✗ Failed to execute command: {e}")
    
    print(f"{'='*60}")
    
    # Close script file if it was opened
    if script_file:
        script_file.write('echo "All issues created successfully!"\n')
        script_file.close()
        # Make the script executable
        subprocess.run(['chmod', '+x', args.save_script])
        print(f"\nCommands saved to: {args.save_script}")
        print(f"Run 'bash {args.save_script}' to create all issues")
    
    if args.dry_run:
        print("\nDRY RUN COMPLETE - No issues were actually created")
        print("Remove the --dry-run flag to create the issues")
    else:
        print(f"\nCompleted processing {len(issues)} issues")


if __name__ == '__main__':
    main()