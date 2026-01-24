#!/usr/bin/env python3
"""
Jane Street Puzzle Practice System

This script helps you practice solving Jane Street puzzles and track your progress.
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
CATALOG_PATH = BASE_DIR / "puzzle_catalog.json"
PROGRESS_PATH = BASE_DIR / "my_attempts" / "progress.json"
ATTEMPTS_DIR = BASE_DIR / "my_attempts"


def load_catalog():
    """Load the puzzle catalog."""
    with open(CATALOG_PATH, 'r') as f:
        return json.load(f)


def load_progress():
    """Load or create progress tracking."""
    if PROGRESS_PATH.exists():
        with open(PROGRESS_PATH, 'r') as f:
            return json.load(f)
    return {
        "attempts": [],
        "completed": [],
        "stats": {
            "total_attempted": 0,
            "total_solved": 0,
            "by_category": {}
        }
    }


def save_progress(progress):
    """Save progress to file."""
    ATTEMPTS_DIR.mkdir(exist_ok=True)
    with open(PROGRESS_PATH, 'w') as f:
        json.dump(progress, f, indent=2)


def get_random_puzzle(catalog, category=None, exclude_completed=True, progress=None):
    """Get a random puzzle, optionally filtered by category."""
    puzzles = catalog["puzzles"]

    # Filter by category if specified
    if category:
        puzzles = [p for p in puzzles if p.get("category") == category]

    # Exclude completed if requested
    if exclude_completed and progress:
        completed_names = set(progress.get("completed", []))
        puzzles = [p for p in puzzles if p["name"] not in completed_names]

    # Exclude current puzzle (no solution yet)
    puzzles = [p for p in puzzles if p.get("status") != "current"]

    if not puzzles:
        return None

    return random.choice(puzzles)


def list_categories(catalog):
    """List all puzzle categories with counts."""
    categories = {}
    for puzzle in catalog["puzzles"]:
        cat = puzzle.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    return categories


def list_puzzles_by_category(catalog, category):
    """List all puzzles in a category."""
    return [p for p in catalog["puzzles"] if p.get("category") == category]


def record_attempt(progress, puzzle_name, solved, notes=""):
    """Record an attempt at solving a puzzle."""
    attempt = {
        "puzzle": puzzle_name,
        "date": datetime.now().isoformat(),
        "solved": solved,
        "notes": notes
    }
    progress["attempts"].append(attempt)
    progress["stats"]["total_attempted"] += 1

    if solved:
        progress["stats"]["total_solved"] += 1
        if puzzle_name not in progress["completed"]:
            progress["completed"].append(puzzle_name)

    save_progress(progress)
    return attempt


def get_stats(progress):
    """Get solving statistics."""
    stats = progress["stats"].copy()
    stats["completion_rate"] = (
        stats["total_solved"] / stats["total_attempted"] * 100
        if stats["total_attempted"] > 0 else 0
    )
    return stats


def print_puzzle(puzzle):
    """Pretty print puzzle info."""
    print("\n" + "="*60)
    print(f"📝 {puzzle['name']}")
    print(f"📅 {puzzle['date']}")
    print(f"🏷️  Category: {puzzle.get('category', 'unknown')}")
    print(f"🔗 {puzzle['puzzle_url']}")
    if puzzle.get('key_concepts'):
        print(f"💡 Key concepts: {', '.join(puzzle['key_concepts'])}")
    if puzzle.get('answer'):
        print(f"✅ Answer: [Hidden - type 'show' to reveal]")
    print("="*60)


def main():
    """Interactive practice mode."""
    print("\n🎯 Jane Street Puzzle Practice System")
    print("="*40)

    catalog = load_catalog()
    progress = load_progress()

    while True:
        print("\nOptions:")
        print("1. Random puzzle")
        print("2. Random puzzle by category")
        print("3. List categories")
        print("4. View my stats")
        print("5. Mark puzzle as solved")
        print("6. View recent attempts")
        print("7. Quit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            puzzle = get_random_puzzle(catalog, progress=progress)
            if puzzle:
                print_puzzle(puzzle)
                show = input("\nShow answer? (y/n): ").strip().lower()
                if show == 'y' and puzzle.get('answer'):
                    print(f"\n🎯 Answer: {puzzle['answer']}")
            else:
                print("No puzzles available!")

        elif choice == "2":
            cats = list_categories(catalog)
            print("\nCategories:")
            for cat, count in sorted(cats.items()):
                print(f"  - {cat}: {count} puzzles")
            cat_choice = input("\nEnter category: ").strip()
            puzzle = get_random_puzzle(catalog, category=cat_choice, progress=progress)
            if puzzle:
                print_puzzle(puzzle)
            else:
                print(f"No puzzles found in category '{cat_choice}'")

        elif choice == "3":
            cats = list_categories(catalog)
            print("\nCategories:")
            for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
                print(f"  {cat}: {count} puzzles")

        elif choice == "4":
            stats = get_stats(progress)
            print(f"\n📊 Your Stats:")
            print(f"  Attempted: {stats['total_attempted']}")
            print(f"  Solved: {stats['total_solved']}")
            print(f"  Completion rate: {stats['completion_rate']:.1f}%")
            print(f"  Puzzles completed: {len(progress['completed'])}")

        elif choice == "5":
            name = input("Puzzle name: ").strip()
            notes = input("Notes (optional): ").strip()
            record_attempt(progress, name, True, notes)
            print(f"✅ Marked '{name}' as solved!")

        elif choice == "6":
            recent = progress["attempts"][-10:]
            print("\nRecent attempts:")
            for a in reversed(recent):
                status = "✅" if a["solved"] else "❌"
                print(f"  {status} {a['puzzle']} ({a['date'][:10]})")

        elif choice == "7":
            print("\nGoodbye! Keep practicing! 🎯")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
