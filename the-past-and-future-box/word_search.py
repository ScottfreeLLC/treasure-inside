import nltk
from nltk.corpus import words

# Download NLTK words if not already downloaded
nltk.download('words')

# Load the NLTK words dictionary
valid_words = set(word.upper() for word in words.words())

# Direction labels and corresponding vectors
DIRECTIONS = {
    (0, 1): "Right",
    (1, 0): "Down",
    (0, -1): "Left",
    (-1, 0): "Up",
    (1, 1): "Diagonal Down-Right",
    (1, -1): "Diagonal Down-Left",
    (-1, 1): "Diagonal Up-Right",
    (-1, -1): "Diagonal Up-Left",
}

def load_matrix_from_file():
    """Load a matrix of letters from 'matrix.txt'."""
    file_path = "matrix.txt"
    try:
        with open(file_path, 'r') as file:
            matrix = [line.strip().split() for line in file]
        return matrix
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit()

def is_within_bounds(r, c, rows, cols):
    """Check if the position is within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def is_plural(word):
    """Determine if a word is a plural form (heuristic: ends with 'S' and singular form is valid)."""
    return word.endswith("S") and word[:-1] in valid_words

def find_all_words_in_grid(matrix, valid_words, min_length=4):
    """Search for all valid non-plural words in the grid."""
    rows, cols = len(matrix), len(matrix[0])
    found_words = []

    # Generate all possible words in all directions from each position
    for row in range(rows):
        for col in range(cols):
            for (dr, dc), direction_label in DIRECTIONS.items():
                word = ""
                for length in range(1, len(matrix[0]) + 1):  # Adjust max length to the matrix's width
                    new_row, new_col = row + dr * (length - 1), col + dc * (length - 1)
                    if not is_within_bounds(new_row, new_col, rows, cols):
                        break  # Out of bounds, stop this direction
                    
                    # Build the word letter by letter
                    word += matrix[new_row][new_col]
                    
                    # Strictly enforce minimum length (>= 4) and non-plural filter
                    if len(word) >= min_length and word in valid_words and not is_plural(word):
                        found_words.append({
                            "word": word,
                            "start_row": row + 1,  # Convert to 1-based index
                            "start_col": col + 1,  # Convert to 1-based index
                            "length": len(word),
                            "direction": direction_label
                        })

    return found_words

# Main program execution
if __name__ == "__main__":
    print("Loading matrix from 'matrix.txt'...")
    matrix = load_matrix_from_file()
    
    print("\nMatrix loaded:")
    for row in matrix:
        print(" ".join(row))
    
    print("\nSearching for words...")
    found_words = find_all_words_in_grid(matrix, valid_words, min_length=4)
    
    print("\nFound words:")
    for entry in found_words:
        print(f"Word: {entry['word']}, Row: {entry['start_row']}, Column: {entry['start_col']}, "
              f"Length: {entry['length']}, Direction: {entry['direction']}")
    print(f"\nTotal Number of Words Found: {len(found_words)}")
