#!/usr/bin/env python3
"""
Verify and update solution files against official Jane Street solutions.

This script:
1. Loads puzzle catalog to get solution URLs
2. Fetches official solutions from janestreet.com
3. Extracts solution content (excluding "Congratulations" sections)
4. Compares with local solution files
5. Optionally updates local files to match

Usage:
    python solutions/scripts/verify_solutions.py                    # Compare only
    python solutions/scripts/verify_solutions.py --update           # Update mismatched files
    python solutions/scripts/verify_solutions.py --puzzle 2020/01   # Check specific puzzle
"""

import json
import re
import argparse
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
CATALOG_FILE = BASE_DIR / "puzzles" / "puzzle_catalog.json"
SOLUTIONS_DIR = BASE_DIR / "solutions"


def load_catalog():
    """Load puzzle catalog."""
    with open(CATALOG_FILE) as f:
        return json.load(f)


def fetch_solution_page(url):
    """Fetch solution page from janestreet.com."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except (HTTPError, URLError) as e:
        print(f"  Error fetching {url}: {e}")
        return None


def extract_solution_content(html):
    """Extract solution content from HTML, excluding congratulations section."""
    if not html:
        return None
    
    # First, strip HTML tags to get clean text
    # Remove script and style content
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Convert <br> to newlines
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # Convert </p>, </div>, </li> to newlines
    text = re.sub(r'</(?:p|div|li|tr)>', '\n', text, flags=re.IGNORECASE)
    
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    
    # Clean up whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    lines = text.split('\n')
    content_lines = []
    in_content = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip cookie notices and navigation
        if 'cookie' in line.lower() and ('accept' in line.lower() or 'reject' in line.lower()):
            continue
        if 'Ad and Cookie Policy' in line:
            continue
        if line in ['Accept All', 'Reject All', 'Accept AllReject All']:
            continue
            
        # Start collecting after "Solution" marker
        if ': Solution' in line or line.endswith(': Solution'):
            in_content = True
            continue
        
        # Skip "Show Puzzle" link text
        if 'Show Puzzle' in line:
            continue
            
        # Stop at congratulations
        if in_content and ('Congratulations' in line or 'Congrats' in line):
            break
            
        if in_content and line:
            # Skip pure navigation/boilerplate lines
            if line in ['Jane Street', 'Puzzles', 'Home']:
                continue
            content_lines.append(line)
    
    if not content_lines:
        return None
    
    # Join and clean up the content
    content = '\n'.join(content_lines)
    
    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()


def get_local_solution_path(date, name):
    """Get path to local solution file."""
    # Convert date like "2020-01" to year "2020" and month "01"
    parts = date.split('-')
    year = parts[0]
    month = parts[1] if len(parts) > 1 else "01"
    
    # Convert name to filename format - keep underscores between words
    filename = name.lower()
    filename = filename.replace('/', '_')  # Alter/Nate -> alter_nate
    filename = filename.replace(' ', '_')
    filename = filename.replace('-', '_')
    filename = filename.replace("'", "")
    filename = filename.replace(",", "")
    filename = re.sub(r'[^a-z0-9_]', '', filename)
    
    solution_path = SOLUTIONS_DIR / year / f"{month}_{filename}.md"
    return solution_path


def read_local_solution(path):
    """Read local solution file and extract content after ## Official Solution."""
    if not path.exists():
        return None
    
    with open(path) as f:
        content = f.read()
    
    # Extract content after "## Official Solution"
    match = re.search(r'## Official Solution\s*\n(.*)', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return content


def compare_solutions(official, local):
    """Compare official and local solutions."""
    if official is None or local is None:
        return False, "Missing content"
    
    # Normalize for comparison
    def normalize(text):
        # Remove markdown headers
        text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)
        # Remove solution image links
        text = re.sub(r'\*\*Solution image:\*\*.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'https://www\.janestreet\.com/puzzles/[^\s]+', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove markdown formatting for comparison
        text = text.replace('**', '').replace('*', '')
        # Lowercase
        text = text.lower().strip()
        return text
    
    off_norm = normalize(official)
    loc_norm = normalize(local)
    
    # Check if they're similar (allowing for minor differences)
    if off_norm == loc_norm:
        return True, "Exact match"
    
    # Check if local contains official content (or vice versa)
    if off_norm in loc_norm:
        return True, "Local has extra content"
    if loc_norm in off_norm:
        return True, "Official has extra content"
    
    # Check word similarity - need high overlap
    off_words = set(off_norm.split())
    loc_words = set(loc_norm.split())
    common_words = off_words & loc_words
    
    # Check what percentage of official words are in local
    if len(off_words) > 0:
        coverage = len(common_words) / len(off_words)
        if coverage > 0.7:
            return True, f"Good coverage ({coverage:.0%})"
    
    # Check overall similarity
    total_words = off_words | loc_words
    if len(total_words) > 0:
        similarity = len(common_words) / len(total_words)
        if similarity > 0.6:
            return True, f"Similar ({similarity:.0%})"
    
    return False, "Different content"


def update_solution_file(path, puzzle_name, date, official_content):
    """Update local solution file with official content."""
    # Parse date
    parts = date.split('-')
    year = parts[0]
    month_names = {
        '01': 'January', '02': 'February', '03': 'March', '04': 'April',
        '05': 'May', '06': 'June', '07': 'July', '08': 'August',
        '09': 'September', '10': 'October', '11': 'November', '12': 'December'
    }
    month = parts[1] if len(parts) > 1 else '01'
    month_name = month_names.get(month, month)
    
    # Get puzzle filename for link
    filename = path.stem
    puzzle_link = f"../../puzzles/{year}/{filename}.md"
    
    # Format the solution file
    content = f"""# {puzzle_name} - {month_name} {year} (Solution)

**Puzzle:** [{filename}.md]({puzzle_link})

## Official Solution

{official_content}
"""
    
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description='Verify solution files against official Jane Street solutions')
    parser.add_argument('--update', action='store_true', help='Update mismatched files')
    parser.add_argument('--force-update', action='store_true', help='Update ALL files to match official (even if similar)')
    parser.add_argument('--puzzle', type=str, help='Check specific puzzle (e.g., 2020/01 or "Alter Nate")')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of puzzles to check')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--diff', action='store_true', help='Show diff between official and local')
    args = parser.parse_args()
    
    print("=" * 60)
    print("VERIFYING SOLUTIONS AGAINST OFFICIAL JANE STREET")
    print("=" * 60)
    
    catalog = load_catalog()
    puzzles = catalog.get('puzzles', [])
    
    # Filter puzzles
    if args.puzzle:
        filtered = []
        for p in puzzles:
            date = p.get('date', '')
            name = p.get('name', '')
            if args.puzzle.lower() in date.lower() or args.puzzle.lower() in name.lower():
                filtered.append(p)
        puzzles = filtered
        print(f"Filtered to {len(puzzles)} puzzle(s) matching '{args.puzzle}'")
    
    # Limit
    if args.limit > 0:
        puzzles = puzzles[:args.limit]
    
    # Filter to puzzles with solution URLs
    puzzles_with_solutions = [p for p in puzzles if p.get('solution_url')]
    print(f"Checking {len(puzzles_with_solutions)} puzzles with solution URLs")
    print()
    
    results = {'match': 0, 'mismatch': 0, 'missing': 0, 'error': 0, 'updated': 0}
    
    for puzzle in puzzles_with_solutions:
        date = puzzle.get('date', '')
        name = puzzle.get('name', '')
        solution_url = puzzle.get('solution_url', '')
        
        print(f"[{date}] {name}")
        
        # Fetch official solution
        if args.verbose:
            print(f"  Fetching: {solution_url}")
        
        html = fetch_solution_page(solution_url)
        if html is None:
            print("  ✗ Could not fetch official solution")
            results['error'] += 1
            continue
        
        official_content = extract_solution_content(html)
        if official_content is None:
            print("  ✗ Could not extract solution content")
            results['error'] += 1
            continue
        
        if args.verbose:
            print(f"  Official content ({len(official_content)} chars):")
            preview = official_content[:200].replace('\n', ' ')
            print(f"    {preview}...")
        
        # Get local solution
        local_path = get_local_solution_path(date, name)
        local_content = read_local_solution(local_path)
        
        if local_content is None:
            print(f"  ✗ Local file not found: {local_path}")
            results['missing'] += 1
            
            if args.update:
                update_solution_file(local_path, name, date, official_content)
                print(f"  → Created: {local_path}")
                results['updated'] += 1
            continue
        
        # Compare
        match, reason = compare_solutions(official_content, local_content)
        
        if match:
            print(f"  ✓ {reason}")
            results['match'] += 1
            
            # Force update even if matching
            if args.force_update:
                update_solution_file(local_path, name, date, official_content)
                print(f"  → Force updated: {local_path}")
                results['updated'] += 1
        else:
            print(f"  ✗ {reason}")
            results['mismatch'] += 1
            
            if args.verbose or args.diff:
                print(f"  Local ({len(local_content)} chars):")
                preview = local_content[:200].replace('\n', ' ')
                print(f"    {preview}...")
            
            if args.diff:
                print(f"  --- OFFICIAL ---")
                print(f"  {official_content[:500]}")
                print(f"  --- LOCAL ---")
                print(f"  {local_content[:500]}")
                print()
            
            if args.update:
                update_solution_file(local_path, name, date, official_content)
                print(f"  → Updated: {local_path}")
                results['updated'] += 1
        
        # Rate limit
        time.sleep(0.5)
    
    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Match:    {results['match']}")
    print(f"  Mismatch: {results['mismatch']}")
    print(f"  Missing:  {results['missing']}")
    print(f"  Errors:   {results['error']}")
    if args.update:
        print(f"  Updated:  {results['updated']}")


if __name__ == "__main__":
    main()
