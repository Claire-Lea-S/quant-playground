#!/usr/bin/env python3
"""
Compare AI-generated answers with official solutions using AI comparison.

This script reads:
- puzzles/attempts/my_answers.json (AI's answers)
- solutions/{year}/*.md (official answers)

And outputs:
- solutions/attempts/attempts_log.csv (append summary row)
- solutions/attempts/puzzle_results_detail.csv (update individual results)
- solutions/attempts/summary.txt (summary statistics)

Usage:
    python solutions/scripts/compare_answers.py
"""

import json
import os
import re
import csv
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Paths - script is in solutions/scripts/, so go up twice to reach root
BASE_DIR = Path(__file__).parent.parent.parent
PUZZLES_DIR = BASE_DIR / "puzzles"
SOLUTIONS_DIR = BASE_DIR / "solutions"

ANSWERS_FILE = PUZZLES_DIR / "attempts" / "my_answers.json"
ATTEMPTS_LOG = SOLUTIONS_DIR / "attempts" / "attempts_log.csv"
RESULTS_DETAIL = SOLUTIONS_DIR / "attempts" / "puzzle_results_detail.csv"
SUMMARY_FILE = SOLUTIONS_DIR / "attempts" / "summary.txt"
CATALOG_FILE = PUZZLES_DIR / "puzzle_catalog.json"


def load_my_answers():
    """Load AI-generated answers."""
    if not ANSWERS_FILE.exists():
        print(f"No answers file found at {ANSWERS_FILE}")
        print("Run the solve-puzzle skill first!")
        return []
    
    with open(ANSWERS_FILE) as f:
        content = f.read().strip()
        if not content or content == "[]":
            print("No answers recorded yet. Run the solve-puzzle skill first!")
            return []
        return json.loads(content)


def extract_answer_from_solution(solution_path):
    """Extract the answer from a solution markdown file."""
    if not solution_path.exists():
        return None
    
    with open(solution_path) as f:
        content = f.read()
    
    # Look for common answer patterns - ordered from most specific to most general
    patterns = [
        # Explicit "answer is" patterns
        r'\*\*Answer[:\s]*([^*]+)\*\*',
        r'Answer[:\s]*\*\*([^*]+)\*\*',
        r'answer is \*\*([^*]+)\*\*',
        r'answer[:\s]+\*\*([^*]+)\*\*',
        r'the answer[^*]*\*\*([^*]+)\*\*',
        
        # Specific result patterns  
        r'move is \*\*([^*]+)\*\*',
        r'ticker is \*\*([^*]+)\*\*',
        r'yields[^*]*\*\*([^*]+)\*\*',
        r'would be[^*]*\*\*([^*]+)\*\*',
        r'counts? (?:to have )?been \*\*([^*]+)\*\*',
        
        # Scientific notation: "about **3.35 × 10^48**" or similar
        r'\*\*([0-9.]+\s*[×x]\s*10\^?\d+)\*\*',
        r'about \*\*([^*]+)\*\*',
        
        # Parenthetical answers: "(Harry, Larry, Mary) = (20, 34, 48)"
        r'\(([^)]+)\)\s*=\s*\(([^)]+)\)',
        
        # "When N = 15" patterns (for threshold answers)
        r'[Ww]hen N\s*=\s*(\d+)',
        r'smallest N[^0-9]*(\d+)',
        r'N\s*=\s*(\d+)[^0-9]',
        
        # Bullet list of probabilities
        r'chances[^:]*:\s*\n((?:[-•]\s*\w+:\s*[^\n]+\n?)+)',
        
        # Any bold text with alphanumeric content
        r'\*\*([A-Za-z0-9,./\-×\s\^()=]+)\*\*(?:\s|,|\.|$)',
        
        # Numbers in various formats
        r'\*\*([0-9,.\-]+)\*\*',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            # Handle multiple groups (for parenthetical patterns)
            if match.lastindex and match.lastindex > 1:
                result = f"({match.group(1)}) = ({match.group(2)})"
            else:
                result = match.group(1).strip()
            
            # Clean up bullet lists
            if '\n' in result:
                lines = [l.strip().lstrip('-•').strip() for l in result.split('\n') if l.strip()]
                result = ', '.join(lines)
            return result
    
    return None


def ai_compare_answers(my_answer, official_answer):
    """Use AI to compare if two answers are equivalent."""
    try:
        import anthropic
        client = anthropic.Anthropic()
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": f"""Are these two puzzle answers equivalent? Answer only YES or NO.

My answer: {my_answer}
Official answer: {official_answer}

Consider:
- Different formatting (= vs :, spaces, commas)
- Equivalent numeric values (fractions, decimals)
- Same meaning expressed differently

Answer YES or NO:"""
            }]
        )
        
        result = response.content[0].text.strip().upper()
        return "YES" in result
        
    except Exception as e:
        print(f"  AI comparison failed: {e}, falling back to string matching")
        return fallback_compare(my_answer, official_answer)


def fallback_compare(my_answer, official_answer):
    """Fallback string comparison if AI fails."""
    if my_answer is None or official_answer is None:
        return None
    
    my_norm = str(my_answer).lower().strip().replace(",", "").replace("=", ":").replace(" ", "")
    off_norm = str(official_answer).lower().strip().replace(",", "").replace("=", ":").replace(" ", "")
    
    if my_norm == off_norm:
        return True
    
    # Check substring
    if my_norm in off_norm or off_norm in my_norm:
        return True
    
    return False


def compare_answers(my_answer, official_answer):
    """Compare two answers using AI."""
    if my_answer is None or official_answer is None:
        return None
    
    return ai_compare_answers(my_answer, official_answer)


def load_catalog():
    """Load puzzle catalog for category info."""
    if not CATALOG_FILE.exists():
        return {"puzzles": []}
    with open(CATALOG_FILE) as f:
        return json.load(f)


def get_puzzle_category(puzzle_id, catalog):
    """Get category for a puzzle from catalog."""
    for puzzle in catalog.get("puzzles", []):
        date = puzzle.get("date", "")
        name = puzzle.get("name", "").lower().replace(" ", "_").replace("-", "_")
        
        if date in puzzle_id or name in puzzle_id.lower():
            return puzzle.get("category", "unknown")
    
    return "unknown"


def load_existing_detail():
    """Load existing puzzle_results_detail.csv."""
    if not RESULTS_DETAIL.exists():
        return None, []
    
    with open(RESULTS_DETAIL) as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if len(rows) < 1:
        return None, []
    
    header = rows[0]
    data_rows = rows[1:] if len(rows) > 1 else []
    return header, data_rows


def update_results_detail(results, header, existing_rows):
    """Update puzzle_results_detail.csv with new results."""
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')
    
    new_row = [date_str, time_str]
    results_map = {r['puzzle']: r['status'] for r in results}
    
    for col in header[2:]:
        if col in results_map:
            new_row.append(results_map[col])
        else:
            new_row.append('')
    
    existing_rows.append(new_row)
    
    with open(RESULTS_DETAIL, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(existing_rows)


def update_attempts_log(by_category, total_correct, total):
    """Append a row to attempts_log.csv."""
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')
    
    if ATTEMPTS_LOG.exists():
        with open(ATTEMPTS_LOG) as f:
            reader = csv.reader(f)
            rows = list(reader)
        header = rows[0] if rows else None
    else:
        header = None
    
    if not header:
        return
    
    new_row = [date_str, time_str]
    
    for col in header[2:]:
        if col == 'overall':
            new_row.append(f"{total_correct}/{total}")
        elif col in by_category:
            cat = by_category[col]
            cat_total = cat['correct'] + cat['incorrect'] + cat['unknown']
            new_row.append(f"{cat['correct']}/{cat_total}")
        else:
            new_row.append('')
    
    with open(ATTEMPTS_LOG, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_row)


def main():
    print("=" * 60)
    print("COMPARING ANSWERS WITH SOLUTIONS (AI-powered)")
    print("=" * 60)
    print(f"Answers file: {ANSWERS_FILE}")
    print(f"Solutions dir: {SOLUTIONS_DIR}")
    print()
    
    my_answers = load_my_answers()
    if not my_answers:
        return
    
    catalog = load_catalog()
    
    results = []
    by_category = defaultdict(lambda: {"correct": 0, "incorrect": 0, "unknown": 0})
    
    for entry in my_answers:
        puzzle_id = entry.get("puzzle", "")
        my_answer = entry.get("my_answer", "")
        
        parts = puzzle_id.split("/")
        if len(parts) >= 2:
            year = parts[0]
            name = parts[1]
            solution_path = SOLUTIONS_DIR / year / f"{name}.md"
        else:
            solution_path = None
        
        official_answer = extract_answer_from_solution(solution_path) if solution_path else None
        
        is_correct = compare_answers(my_answer, official_answer)
        
        category = get_puzzle_category(puzzle_id, catalog)
        
        status = "correct" if is_correct == True else ("incorrect" if is_correct == False else "unknown")
        results.append({
            "puzzle": puzzle_id,
            "my_answer": my_answer,
            "official_answer": official_answer or "N/A",
            "status": status,
            "category": category
        })
        
        by_category[category][status] += 1
        
        symbol = "✓" if is_correct == True else ("✗" if is_correct == False else "?")
        print(f"[{symbol}] {puzzle_id}: {my_answer} vs {official_answer or 'N/A'}")
    
    header, existing_rows = load_existing_detail()
    if header:
        update_results_detail(results, header, existing_rows)
        print(f"\nUpdated: {RESULTS_DETAIL}")
    
    total_correct = sum(cat["correct"] for cat in by_category.values())
    total_incorrect = sum(cat["incorrect"] for cat in by_category.values())
    total_unknown = sum(cat["unknown"] for cat in by_category.values())
    total = total_correct + total_incorrect + total_unknown
    
    update_attempts_log(by_category, total_correct, total)
    print(f"Appended to: {ATTEMPTS_LOG}")
    
    summary = []
    summary.append("")
    summary.append("=" * 60)
    summary.append("SUMMARY")
    summary.append("=" * 60)
    summary.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"Total: {total_correct}/{total} correct ({100*total_correct/total:.1f}%)" if total > 0 else "No puzzles")
    summary.append("")
    summary.append("By Category:")
    
    for category, counts in sorted(by_category.items()):
        cat_total = counts["correct"] + counts["incorrect"] + counts["unknown"]
        if cat_total > 0:
            pct = 100 * counts["correct"] / cat_total
            summary.append(f"  {category}: {counts['correct']}/{cat_total} ({pct:.1f}%)")
    
    summary_text = "\n".join(summary)
    print(summary_text)
    
    with open(SUMMARY_FILE, "w") as f:
        f.write(summary_text)
    
    print(f"\nSummary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
