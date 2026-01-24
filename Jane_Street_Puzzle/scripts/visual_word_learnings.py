"""
Visual and Word Puzzle Learnings from Jane Street Puzzles
=========================================================

This module contains lessons learned from attempting and analyzing Jane Street's
visual and word puzzles. The goal is to build a "playbook" for solving future
puzzles in these categories.

Puzzles Analyzed:
1. Dogs Playing Poker (2025-08) - Visual puzzle with emoji decoding + Caesar cipher
2. Games Night! (2024-12) - Board game identification and extraction
3. Game Night! (2023-05) - Codenames boards with binary encoding
4. Eldrow (2022-02) - Reverse Wordle word chains
5. Poetry in Motion (2019-12) - Chess position encoded in poem structure
6. Crosswords (2017-12) - Braille encoding in crossword loops
7. Some Ones, Somewhere (2025-06) - Partridge tiling with coordinate extraction

Author: Generated from puzzle practice session
Date: 2026-01-24
"""

from typing import List, Dict, Tuple, Optional
import string


# =============================================================================
# PUZZLE ATTEMPTS AND REASONING
# =============================================================================

PUZZLE_ATTEMPTS = {
    "dogs_playing_poker_2025_08": {
        "my_initial_approach": """
            I recognized this involved emoji decoding and Caesar cipher from the hints.
            My strategy was:
            1. Identify emojis representing each dog
            2. Look for patterns in emoji names
            3. Apply Caesar cipher if text emerged

            I correctly identified that emojis have standardized names that could be
            indexed into, but I missed the two-layer decoding:
            - First layer: Index into emoji names using card values
            - Second layer: Shift letters by chip counts
        """,
        "what_i_missed": [
            "The two-layer encoding (emoji indexing + Caesar shift)",
            "Using chip counts as the shift value for Caesar cipher",
            "K-9 = 'canine' wordplay for the final answer"
        ],
        "official_answer": "Kc,9c (King of clubs, 9 of clubs)",
        "key_insight": "Visual puzzles often have MULTIPLE encoding layers - decode one to get instructions for the next"
    },

    "games_night_2024_12": {
        "my_initial_approach": """
            I correctly identified that:
            - Multiple board games were shown incomplete
            - Missing pieces would encode letters
            - The answer was a single word

            My approach of looking for missing pieces was correct, but I didn't
            anticipate the layered extraction:
            - First extraction: Pieces arranged as letters spell 'MISSING ONES'
            - Second extraction: First letters of missing pieces spell 'YOU SUNK MY'
            - Final answer completes the phrase: BATTLESHIP
        """,
        "what_i_missed": [
            "The pieces themselves were arranged INTO letter shapes (not just missing)",
            "Two-layer extraction: letter shapes first, then initial letters",
            "The phrase completion mechanism ('You sunk my ___')"
        ],
        "official_answer": "BATTLESHIP",
        "key_insight": "Look for MULTIPLE extraction methods - both visual arrangement AND content extraction"
    },

    "game_night_2023_05": {
        "my_initial_approach": """
            Codenames boards suggested word association, but I didn't anticipate
            the binary encoding mechanism. My approach would have been to look
            for semantic patterns in the selected words.
        """,
        "what_i_missed": [
            "Each row encodes a 5-bit binary number (selected=1, unselected=0)",
            "Binary numbers map to letters A-Z (0-25 or 1-26)",
            "The decoded message gives instructions for next iteration",
            "Recursive decoding: each message tells you how to filter for the next round"
        ],
        "official_answer": "SIEVE",
        "decoding_steps": [
            "Binary -> 'SCRABBLESUMODD_'",
            "Filter by odd Scrabble sum -> 'LONGERTHANFIVE_'",
            "Filter by length > 5 -> 'MIDDLELETTEROF_'",
            "Read middle letters of remaining words -> 'SIEVE'"
        ],
        "key_insight": "When selections form a grid, think BINARY encoding (selected/unselected = 1/0)"
    },

    "eldrow_2022_02": {
        "my_initial_approach": """
            I understood the Wordle mechanics but underestimated the search complexity.
            My strategy was:
            1. Start with words that give minimal info (preserve options)
            2. Progressively eliminate letters
            3. Use words ending in -ER pattern for consistency

            The winning solution used -ER words ending pattern, which I partially
            anticipated. The key was systematic computer-aided search.
        """,
        "what_i_missed": [
            "The optimal pattern uses -ER ending words consistently",
            "Maximum chain is 16 words (not close to theoretical 26)",
            "Need algorithmic search, not just intuition"
        ],
        "official_answer": "16 words: GAZER->INNER->QUEER->ODDER->BOXER->FOYER->HOVER->JOKER->WOOER->LOWER->MOWER->POWER->ROWER->SOWER->TOWER->COWER",
        "key_insight": "Word puzzles with constraints often have structural solutions (-ER pattern) that require systematic search"
    },

    "poetry_in_motion_2019_12": {
        "my_initial_approach": """
            I recognized this was chess-related from 'black just moved' hint.
            However, I didn't anticipate the poem structure encoding the board.

            My approach would have been to look for chess notation in the text,
            not to treat the poem as a positional grid.
        """,
        "what_i_missed": [
            "8 lines x 8 words = chessboard grid",
            "First letter of each word = piece type (K,Q,R,B,N,P)",
            "Capitalized lines = white pieces, lowercase = black pieces",
            "Need to prove castling rights through move history analysis"
        ],
        "official_answer": "Rxd7 followed by Qb8# (White wins in 2)",
        "key_insight": "Poem structure (lines x words) can encode spatial information like chess boards"
    },

    "crosswords_2017_12": {
        "my_initial_approach": """
            For a crossword puzzle, I would typically look for:
            - Clue wordplay
            - Theme connections
            - Meta-puzzle extraction

            I did not anticipate Braille encoding.
        """,
        "what_i_missed": [
            "Arrow loops in the grid create intersection points",
            "Intersection points within regions form Braille patterns",
            "Braille letters spell the answer",
            "Need knowledge of Braille alphabet to decode"
        ],
        "official_answer": "NOVUS ANNUS (Latin for 'New Year')",
        "key_insight": "Visual puzzles may use alternative encoding systems (Braille, Morse, semaphore)"
    },

    "some_ones_somewhere_2025_06": {
        "my_initial_approach": """
            Partridge tiling was a new concept for me. I would have:
            1. Tried to understand the tiling constraints
            2. Looked for the 1x1 squares in each grid
            3. Attempted to extract information from positions

            The coordinate-to-letter mapping was intuitive, but I missed
            the border decoding step.
        """,
        "what_i_missed": [
            "Border letters form 'tiling' and 'partridge' when blanks filled with ABC...XYZ pattern",
            "Each 1x1 square position gives (row, col) coordinates",
            "Coordinates map to letters: 19th row, 21st col = (S, U)",
            "All coordinate pairs spell the answer phrase"
        ],
        "official_answer": "the sum of cubes is a square",
        "key_insight": "Grid positions (row, col) can encode letter pairs when mapped to alphabet"
    }
}


# =============================================================================
# KEY TECHNIQUES THAT WORK
# =============================================================================

KEY_TECHNIQUES = {
    "binary_encoding": {
        "description": "Selections in a grid encode binary numbers that map to letters",
        "when_to_use": "Grid of items where some are 'selected' or highlighted",
        "method": "Row of N items -> N-bit number -> letter (A=0/1, B=1/2, etc.)",
        "examples": ["Game Night! 2023 Codenames boards"]
    },

    "multi_layer_extraction": {
        "description": "First decode gives instructions for second decode",
        "when_to_use": "When first extraction seems like partial instructions",
        "method": "Decode layer 1 -> Apply instructions -> Decode layer 2 -> ...",
        "examples": [
            "Dogs Playing Poker (emoji index -> Caesar shift)",
            "Games Night! (letter shapes -> first letters -> phrase completion)",
            "Game Night! (binary -> Scrabble filter -> length filter -> middle letters)"
        ]
    },

    "coordinate_extraction": {
        "description": "Grid positions map to letters via row/column numbers",
        "when_to_use": "Grid puzzle where specific cells are marked or special",
        "method": "Position (row, col) -> letter pair where row=letter1, col=letter2",
        "examples": ["Some Ones, Somewhere (1x1 square positions)"]
    },

    "structural_encoding": {
        "description": "Physical structure of text/puzzle encodes spatial information",
        "when_to_use": "Poems, crosswords, or text with suspicious dimensions",
        "method": "Count lines x words or analyze grid structure for hidden patterns",
        "examples": [
            "Poetry in Motion (8x8 poem = chessboard)",
            "Crosswords (loop intersections form Braille)"
        ]
    },

    "caesar_cipher_variants": {
        "description": "Shifting letters by some amount indicated in the puzzle",
        "when_to_use": "When decoded text seems like gibberish but structured",
        "method": "Find the shift value in puzzle context (chips, numbers, etc.)",
        "examples": ["Dogs Playing Poker (shift by chip count)"]
    },

    "indexing_into_names": {
        "description": "Use numbers to index into standardized names of elements",
        "when_to_use": "Emojis, symbols, or items with official names + associated numbers",
        "method": "Element with number N -> take Nth letter of element's official name",
        "examples": ["Dogs Playing Poker (card value -> letter in emoji name)"]
    },

    "missing_piece_identification": {
        "description": "Find what's missing from a set to extract information",
        "when_to_use": "Incomplete collections or sets shown",
        "method": "Identify complete set -> find missing element -> extract first letter or property",
        "examples": ["Games Night! (missing board game pieces)"]
    },

    "alternative_alphabets": {
        "description": "Patterns may encode Braille, Morse, semaphore, or other systems",
        "when_to_use": "Dot patterns, intersection points, or flag-like arrangements",
        "method": "Identify the encoding system -> decode using that alphabet",
        "examples": ["Crosswords (Braille in intersection points)"]
    },

    "wordplay_and_phonetics": {
        "description": "Final answer often involves clever wordplay",
        "when_to_use": "When decoded phrase seems like a hint rather than answer",
        "method": "Look for puns, homphones, or phrase completions",
        "examples": [
            "Dogs Playing Poker (K-9 = canine)",
            "Games Night! (You sunk my ___ = BATTLESHIP)"
        ]
    },

    "recursive_constraint_solving": {
        "description": "For word chains, find structural patterns that enable long sequences",
        "when_to_use": "Puzzles asking for longest/optimal sequences",
        "method": "Look for word patterns (endings, letter patterns) that minimize constraint propagation",
        "examples": ["Eldrow (-ER ending words enable 16-word chain)"]
    }
}


# =============================================================================
# MISTAKES AND MISCONCEPTIONS
# =============================================================================

MISTAKES_AND_MISCONCEPTIONS = {
    "single_layer_assumption": {
        "description": "Assuming one decoding step is sufficient",
        "lesson": "Jane Street puzzles typically have 2-4 encoding layers",
        "fix": "After first decode, ask: 'Does this give me instructions for another decode?'"
    },

    "ignoring_flavor_text": {
        "description": "Treating puzzle narrative as just flavor, not clues",
        "lesson": "Every word in Jane Street puzzles is intentional",
        "fix": "Parse flavor text for hints about encoding methods"
    },

    "missing_visual_arrangements": {
        "description": "Looking at content but not how it's arranged",
        "lesson": "Physical arrangement of elements often carries information",
        "fix": "Step back and look at shapes formed by the elements"
    },

    "unfamiliar_encoding_systems": {
        "description": "Not recognizing Braille, Morse, or other alternative alphabets",
        "lesson": "Build knowledge of various encoding systems",
        "fix": "When dots/patterns appear, check against known encoding systems"
    },

    "underestimating_search_space": {
        "description": "Trying to solve computationally hard problems by intuition",
        "lesson": "Some puzzles require systematic search",
        "fix": "Write code to explore solution space when constraints are tight"
    },

    "literal_interpretation": {
        "description": "Not looking for wordplay in final answers",
        "lesson": "Final step often involves puns or phrase completion",
        "fix": "Ask: 'Is this a hint pointing to something else?'"
    },

    "missing_grid_structure": {
        "description": "Not noticing when text forms a grid with meaning",
        "lesson": "8x8, 5x5, or other structured text may encode spatial info",
        "fix": "Count dimensions of text structures and consider positional meaning"
    }
}


# =============================================================================
# HELPER FUNCTIONS FOR SOLVING PATTERNS
# =============================================================================

def binary_row_to_letter(selections: List[bool], zero_indexed: bool = True) -> str:
    """
    Convert a row of selections to a letter using binary encoding.

    Args:
        selections: List of booleans where True = selected/highlighted
        zero_indexed: If True, 00000 = A. If False, 00001 = A.

    Returns:
        The corresponding letter

    Example:
        >>> binary_row_to_letter([True, False, False, False, True])  # 10001 = 17
        'R' (if zero_indexed) or 'Q' (if not)
    """
    binary_val = sum(bit << (len(selections) - 1 - i)
                     for i, bit in enumerate(selections) if bit)
    if not zero_indexed:
        binary_val -= 1
    if 0 <= binary_val < 26:
        return chr(ord('A') + binary_val)
    return '?'


def grid_to_binary_letters(grid: List[List[bool]], zero_indexed: bool = True) -> str:
    """
    Convert an entire grid of selections to a string of letters.

    Args:
        grid: 2D list of booleans (rows of selections)
        zero_indexed: If True, 00000 = A

    Returns:
        String of decoded letters
    """
    return ''.join(binary_row_to_letter(row, zero_indexed) for row in grid)


def caesar_shift(text: str, shift: int) -> str:
    """
    Apply Caesar cipher shift to text.

    Args:
        text: Input string
        shift: Number of positions to shift (positive = forward)

    Returns:
        Shifted text
    """
    result = []
    for char in text:
        if char.upper() in string.ascii_uppercase:
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)
    return ''.join(result)


def variable_caesar_shift(text: str, shifts: List[int]) -> str:
    """
    Apply variable Caesar shifts where each letter has its own shift amount.

    Args:
        text: Input string (only letters count for shift indexing)
        shifts: List of shift values, one per letter in text

    Returns:
        Shifted text
    """
    result = []
    shift_idx = 0
    for char in text:
        if char.upper() in string.ascii_uppercase:
            if shift_idx < len(shifts):
                shift = shifts[shift_idx]
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + shift) % 26 + base
                result.append(chr(shifted))
                shift_idx += 1
            else:
                result.append(char)
        else:
            result.append(char)
    return ''.join(result)


def index_into_name(name: str, index: int, one_indexed: bool = True) -> str:
    """
    Get a character from a name at a given index.

    Args:
        name: The full name string
        index: Position to extract (1-indexed by default for card values)
        one_indexed: If True, index 1 = first character

    Returns:
        Character at that position, or '?' if out of bounds
    """
    idx = index - 1 if one_indexed else index
    if 0 <= idx < len(name):
        return name[idx]
    return '?'


def extract_first_letters(items: List[str]) -> str:
    """
    Extract first letter of each item.

    Args:
        items: List of strings

    Returns:
        String of first letters
    """
    return ''.join(item[0] if item else '' for item in items)


def coordinates_to_letters(coords: List[Tuple[int, int]], one_indexed: bool = True) -> str:
    """
    Convert grid coordinates to letter pairs.

    Args:
        coords: List of (row, col) tuples
        one_indexed: If True, position 1 = 'A'

    Returns:
        String of letters from coordinates
    """
    result = []
    for row, col in coords:
        r = row - 1 if one_indexed else row
        c = col - 1 if one_indexed else col
        if 0 <= r < 26:
            result.append(chr(ord('A') + r))
        if 0 <= c < 26:
            result.append(chr(ord('A') + c))
    return ''.join(result)


def decode_braille(pattern: List[List[bool]]) -> str:
    """
    Decode a Braille pattern to a letter.

    Braille cell layout:
    1 4
    2 5
    3 6

    Args:
        pattern: 3x2 grid of booleans representing dot presence

    Returns:
        Decoded letter
    """
    # Standard Braille alphabet (dots numbered 1-6 as above)
    BRAILLE_MAP = {
        (True, False, False, False, False, False): 'A',
        (True, True, False, False, False, False): 'B',
        (True, False, False, True, False, False): 'C',
        (True, False, False, True, True, False): 'D',
        (True, False, False, False, True, False): 'E',
        (True, True, False, True, False, False): 'F',
        (True, True, False, True, True, False): 'G',
        (True, True, False, False, True, False): 'H',
        (False, True, False, True, False, False): 'I',
        (False, True, False, True, True, False): 'J',
        (True, False, True, False, False, False): 'K',
        (True, True, True, False, False, False): 'L',
        (True, False, True, True, False, False): 'M',
        (True, False, True, True, True, False): 'N',
        (True, False, True, False, True, False): 'O',
        (True, True, True, True, False, False): 'P',
        (True, True, True, True, True, False): 'Q',
        (True, True, True, False, True, False): 'R',
        (False, True, True, True, False, False): 'S',
        (False, True, True, True, True, False): 'T',
        (True, False, True, False, False, True): 'U',
        (True, True, True, False, False, True): 'V',
        (False, True, False, True, True, True): 'W',
        (True, False, True, True, False, True): 'X',
        (True, False, True, True, True, True): 'Y',
        (True, False, True, False, True, True): 'Z',
    }

    # Convert 3x2 grid to tuple of 6 bools (column-major: 1,2,3,4,5,6)
    if len(pattern) == 3 and all(len(row) == 2 for row in pattern):
        dots = (
            pattern[0][0], pattern[1][0], pattern[2][0],  # Column 1
            pattern[0][1], pattern[1][1], pattern[2][1]   # Column 2
        )
        return BRAILLE_MAP.get(dots, '?')
    return '?'


def scrabble_score(word: str) -> int:
    """
    Calculate Scrabble score for a word.

    Args:
        word: The word to score

    Returns:
        Total Scrabble point value
    """
    SCORES = {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
        'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
        'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
        'Y': 4, 'Z': 10
    }
    return sum(SCORES.get(c.upper(), 0) for c in word)


def middle_letter(word: str) -> str:
    """
    Get the middle letter of a word (only valid for odd-length words).

    Args:
        word: The input word

    Returns:
        Middle letter if odd length, empty string if even
    """
    if len(word) % 2 == 1:
        return word[len(word) // 2]
    return ''


def check_wordle_constraints(guess: str, target: str,
                            previous_greens: Dict[int, str],
                            previous_yellows: List[Tuple[str, int]],
                            gray_letters: set) -> bool:
    """
    Check if a Wordle guess satisfies hard-mode constraints.

    Args:
        guess: The word being checked
        target: The target word (for computing new constraints)
        previous_greens: Dict of position -> letter for green letters
        previous_yellows: List of (letter, wrong_position) tuples
        gray_letters: Set of letters known to not be in target

    Returns:
        True if guess satisfies all constraints
    """
    guess = guess.upper()

    # Check gray letters aren't used
    for letter in gray_letters:
        if letter in guess:
            return False

    # Check green letters are in correct positions
    for pos, letter in previous_greens.items():
        if pos < len(guess) and guess[pos] != letter:
            return False

    # Check yellow letters are present but not in wrong positions
    for letter, wrong_pos in previous_yellows:
        if letter not in guess:
            return False
        if wrong_pos < len(guess) and guess[wrong_pos] == letter:
            return False

    return True


def fill_alphabet_pattern(text: str, pattern: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    """
    Fill blank spaces in text with cycling alphabet pattern.

    Args:
        text: Text with spaces/blanks to fill
        pattern: Pattern to cycle through (default: A-Z)

    Returns:
        Text with blanks filled

    Example:
        >>> fill_alphabet_pattern("_T_I_L_I_N_G_")  # Blanks become A,B,C,...
    """
    result = []
    pattern_idx = 0
    for char in text:
        if char == '_' or char == ' ':
            result.append(pattern[pattern_idx % len(pattern)])
            pattern_idx += 1
        else:
            result.append(char)
            # Also advance pattern for non-blank positions if we want continuous cycling
    return ''.join(result)


# =============================================================================
# PUZZLE SOLVING CHECKLIST
# =============================================================================

SOLVING_CHECKLIST = """
VISUAL/WORD PUZZLE SOLVING CHECKLIST
====================================

STEP 1: IDENTIFY THE PUZZLE TYPE
- [ ] Is this a visual puzzle with images/symbols?
- [ ] Is this a word/text puzzle?
- [ ] Is there a grid structure?
- [ ] Are there selections/highlights?

STEP 2: LOOK FOR ENCODING MECHANISMS
- [ ] Binary encoding (selected/unselected = 1/0)?
- [ ] Position/coordinate encoding?
- [ ] First letters of words?
- [ ] Indexing into names using numbers?
- [ ] Caesar cipher or letter shifting?
- [ ] Alternative alphabet (Braille, Morse)?
- [ ] Structural encoding (rows x cols = spatial info)?

STEP 3: CHECK FOR MULTI-LAYER ENCODING
- [ ] Does first decode look like instructions?
- [ ] Are there multiple steps implied in the puzzle?
- [ ] Is there a phrase to complete?
- [ ] Is there wordplay in the decoded text?

STEP 4: VERIFY AND ITERATE
- [ ] Does the answer format match what's expected?
- [ ] Have you used all the information given?
- [ ] Is there an "aha" moment or elegant solution?

COMMON ANSWER FORMATS
- Single word (often a game, concept, or phrase completion)
- Coordinates or card notation
- A sentence or phrase
- A number or mathematical expression
"""


# =============================================================================
# TESTING THE HELPER FUNCTIONS
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("VISUAL AND WORD PUZZLE LEARNINGS - FUNCTION TESTS")
    print("=" * 60)

    # Test binary encoding
    print("\n1. Binary Row to Letter:")
    print(f"   [T,F,F,F,F] (10000 = 16) -> {binary_row_to_letter([True,False,False,False,False])}")
    print(f"   [F,F,F,F,T] (00001 = 1) -> {binary_row_to_letter([False,False,False,False,True])}")

    # Test Caesar cipher
    print("\n2. Caesar Shift:")
    print(f"   'THE CANINE' shifted by -3 -> {caesar_shift('THE CANINE', -3)}")
    print(f"   'QEB ZXKFKB' shifted by +3 -> {caesar_shift('QEB ZXKFKB', 3)}")

    # Test coordinate extraction
    print("\n3. Coordinates to Letters:")
    coords = [(19, 21), (13, 15), (6, 3)]  # (S,U), (M,O), (F,C)
    print(f"   [(19,21), (13,15), (6,3)] -> {coordinates_to_letters(coords)}")

    # Test Scrabble scoring
    print("\n4. Scrabble Scores:")
    test_words = ["QUIZ", "JAZZ", "HELLO", "WORLD"]
    for word in test_words:
        print(f"   {word}: {scrabble_score(word)} points")

    # Test middle letter
    print("\n5. Middle Letters:")
    odd_words = ["HELLO", "CAT", "ABCDEFG"]
    for word in odd_words:
        print(f"   {word} -> '{middle_letter(word)}'")

    # Test first letter extraction
    print("\n6. First Letters:")
    items = ["Yellow", "Orange", "Umbrella", "Soda", "Umbrella", "Nest", "Kite", "Milk", "Yak"]
    print(f"   {items}")
    print(f"   -> {extract_first_letters(items)}")

    print("\n" + "=" * 60)
    print("KEY INSIGHTS SUMMARY")
    print("=" * 60)

    for name, technique in KEY_TECHNIQUES.items():
        print(f"\n{name.upper().replace('_', ' ')}:")
        print(f"   {technique['description']}")
        print(f"   Use when: {technique['when_to_use']}")

    print("\n" + "=" * 60)
    print("TOP MISTAKES TO AVOID")
    print("=" * 60)

    for name, mistake in MISTAKES_AND_MISCONCEPTIONS.items():
        print(f"\n{name.upper().replace('_', ' ')}:")
        print(f"   Problem: {mistake['description']}")
        print(f"   Fix: {mistake['fix']}")
