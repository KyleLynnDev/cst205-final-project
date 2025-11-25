"""
Wave Function Collapse Implementation in Python 
Simple tile-based image generation
"""

from PIL import Image
import os


class Cell:
    """
    Represents a single cell in the WFC grid.
    Each cell can be in a collapsed or uncollapsed state.
    """
    
    def __init__(self, options):
        """
        Initialize a cell with possible tile options.
        
        Args:
            options: List of tile indices that could be placed in this cell
        """
        self.options = options.copy()  # List of possible tile indices
        self.collapsed = False  # Whether this cell has been determined
        self.tile_index = None  # The chosen tile index (when collapsed)
    
    def collapse(self, tile_index):
        """
        Collapse this cell to a specific tile.
        
        Args:
            tile_index: Index of the tile to place in this cell
        """
        self.collapsed = True
        self.tile_index = tile_index
        self.options = [tile_index]  # Only one option remains
    
    def is_collapsed(self):
        """Check if this cell is collapsed."""
        return self.collapsed
    
    def get_entropy(self):
        """
        Get the entropy (number of possible options) for this cell.
        Lower entropy = fewer options = should be collapsed sooner.
        """
        if self.collapsed:
            return 0
        return len(self.options)
    
    def __repr__(self):
        if self.collapsed:
            return f"Cell(collapsed, tile={self.tile_index})"
        else:
            return f"Cell({len(self.options)} options)"








def load_tiles(tiles_folder=None):

    """
    Load all tile images from a folder into an array.
    
    Args:
        tiles_folder: Path to folder containing tile PNG images
    
    Returns:
        List of dictionaries, each containing:
            - 'index': tile index number
            - 'name': filename without extension
            - 'image': PIL Image object
            - 'path': full path to the image
    """


    # Default to basic_tiles folder - use absolute path from script location
    if tiles_folder is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tiles_folder = os.path.join(script_dir, "..", "static", "images", "WFC", "WFCTiles", "basic_tiles")
        tiles_folder = os.path.normpath(tiles_folder)  # Clean up the path
    

    tiles = []
    
    print(f"Loading tiles from: {tiles_folder}")
    
    # Check if folder exists
    if not os.path.exists(tiles_folder):
        print(f"ERROR: Tiles folder not found: {tiles_folder}")
        return tiles
    

    # Get all PNG files in the folder
    tile_files = [f for f in os.listdir(tiles_folder) if f.endswith('.png')]
    tile_files.sort()  # Sort for consistent ordering
    
    print(f"Found {len(tile_files)} tile files")
    print("\nTile Index | Name           | Size")
    print("-" * 45)
    
    # Load each tile with enumeration
    for index, tile_file in enumerate(tile_files):
        tile_path = os.path.join(tiles_folder, tile_file)
        tile_name = os.path.splitext(tile_file)[0]  # Remove .png extension
        
        try:
            tile_image = Image.open(tile_path)
            tiles.append({
                'index': index,
                'name': tile_name,
                'image': tile_image,
                'path': tile_path
            })
            print(f"    {index:2d}     | {tile_name:14s} | {tile_image.size[0]}x{tile_image.size[1]}")
        except Exception as e:
            print(f"    {index:2d}     | {tile_name:14s} | ERROR: {e}")
    
    print(f"\nSuccessfully loaded {len(tiles)} tiles (indices 0-{len(tiles)-1})")
    return tiles


def setup_adjacency_rules(tiles):
    """
    Define which tiles can be adjacent to each other.
    This defines the "rules" of the Wave Function Collapse.
    
    For each tile, we specify which tiles can be:
    - up: above it
    - down: below it  
    - left: to the left of it
    - right: to the right of it
    
    Args:
        tiles: List of tile dictionaries
    
    Returns:
        Dictionary mapping tile indices to their valid neighbors
    """
    
    # Create a dictionary to store adjacency rules
    # Format: {tile_index: {'up': [list], 'down': [list], 'left': [list], 'right': [list]}}
    adjacency = {}
    
    print("\n=== Setting up Adjacency Rules ===")
    
    # Initialize adjacency for each tile
    for tile in tiles:
        tile_idx = tile['index']
        tile_name = tile['name']
        
        # Start with all tiles as valid neighbors (we'll restrict this)
        adjacency[tile_idx] = {
            'up': [],
            'down': [],
            'left': [],
            'right': []
        }
        
        # Define rules based on tile names
        # This is where you define the logic of which tiles can be next to each other
        
        if tile_name == 'blank':
            # Blank can only connect to matching directional tiles
            adjacency[tile_idx]['up'] = [4]      # Only 'up' tile above (blank accepts up line from below)
            adjacency[tile_idx]['down'] = [1]    # Only 'down' tile below (blank accepts down line from above)
            adjacency[tile_idx]['left'] = [2]    # Only 'left' tile to the left (blank accepts left line from right)
            adjacency[tile_idx]['right'] = [3]   # Only 'right' tile to the right (blank accepts right line from left)
        
        elif tile_name == 'up':
            # Up tile has lines going: up, left, right (NO down line)
            adjacency[tile_idx]['up'] = [1, 2, 3]  # above needs down line: down, left, right (NOT up!)
            adjacency[tile_idx]['down'] = [0]      # below needs up line: only blank
            adjacency[tile_idx]['left'] = [1, 3, 4]  # left needs right line: down, right, up (NOT left!)
            adjacency[tile_idx]['right'] = [1, 2, 4]  # right needs left line: down, left, up (NOT right!)
        
        elif tile_name == 'down':
            # Down tile has lines going: down, left, right (NO up line)
            adjacency[tile_idx]['up'] = [0]  # above needs down line: only blank
            adjacency[tile_idx]['down'] = [2, 3, 4]  # below needs up line: left, right, up (NOT down!)
            adjacency[tile_idx]['left'] = [1, 3, 4]  # left needs right line: down, right, up (NOT left!)
            adjacency[tile_idx]['right'] = [1, 2, 4]  # right needs left line: down, left, up (NOT right!)
        
        elif tile_name == 'left':
            # Left tile has lines going: left, up, down (NO right line)
            # Left has UP line, so tile above must have DOWN line
            adjacency[tile_idx]['up'] = [1, 2, 3]  # above needs down line: down(1), left(2), right(3) - NOT up(4) or blank(0)!
            adjacency[tile_idx]['down'] = [2, 3, 4]  # below needs up line: left, right, up (NOT down!)
            adjacency[tile_idx]['left'] = [1, 3, 4]  # left needs right line: down, right, up (NOT left!)
            adjacency[tile_idx]['right'] = [0]  # right needs left line: only blank
        
        elif tile_name == 'right':
            # Right tile has lines going: right, up, down (NO left line)
            # Right has UP line, so tile above must have DOWN line
            adjacency[tile_idx]['up'] = [1, 2, 3]  # above needs down line: down(1), left(2), right(3) - NOT up(4) or blank(0)!
            adjacency[tile_idx]['down'] = [2, 3, 4]  # below needs up line: left, right, up (NOT down!)
            adjacency[tile_idx]['left'] = [0]  # left needs right line: only blank
            adjacency[tile_idx]['right'] = [1, 2, 4]  # right needs left line: down, left, up (NOT right!)
        
        print(f"Tile {tile_idx} ({tile_name:8s}): up={adjacency[tile_idx]['up']}, "
              f"down={adjacency[tile_idx]['down']}, "
              f"left={adjacency[tile_idx]['left']}, "
              f"right={adjacency[tile_idx]['right']}")
    
    print(f"Adjacency rules configured for {len(adjacency)} tiles\n")
    return adjacency


def analyze_entropy(grid, tiles_x, tiles_y):
    """
    Analyze the entropy of all cells in the grid.
    Entropy = number of possible options for a cell.
    Lower entropy means the cell is more constrained.
    
    Args:
        grid: 2D array of Cell objects
        tiles_x: Width of grid
        tiles_y: Height of grid
    
    Returns:
        Statistics about the grid entropy
    """
    total_entropy = 0
    uncollapsed_count = 0
    collapsed_count = 0
    
    for y in range(tiles_y):
        for x in range(tiles_x):
            cell = grid[y][x]
            if cell.is_collapsed():
                collapsed_count += 1
            else:
                uncollapsed_count += 1
                total_entropy += cell.get_entropy()
    
    avg_entropy = total_entropy / uncollapsed_count if uncollapsed_count > 0 else 0
    
    return {
        'collapsed': collapsed_count,
        'uncollapsed': uncollapsed_count,
        'total_entropy': total_entropy,
        'average_entropy': avg_entropy
    }


def find_lowest_entropy_cell(grid, tiles_x, tiles_y):
    """
    Find the uncollapsed cell with the lowest entropy.
    This is the cell we should collapse next.
    
    Args:
        grid: 2D array of Cell objects
        tiles_x: Width of grid
        tiles_y: Height of grid
    
    Returns:
        Tuple of (x, y) coordinates, or None if all cells are collapsed
    """
    min_entropy = float('inf')
    candidates = []
    
    for y in range(tiles_y):
        for x in range(tiles_x):
            cell = grid[y][x]
            if not cell.is_collapsed():
                entropy = cell.get_entropy()
                
                if entropy < min_entropy:
                    min_entropy = entropy
                    candidates = [(x, y)]
                elif entropy == min_entropy:
                    candidates.append((x, y))
    
    if not candidates:
        return None
    
    # If multiple cells have same entropy, pick randomly
    import random
    return random.choice(candidates)


def propagate_constraints(grid, x, y, adjacency, tiles_x, tiles_y):
    """
    Propagate constraints from a collapsed cell to its neighbors.
    This reduces the options for neighboring cells based on adjacency rules.
    
    Args:
        grid: 2D array of Cell objects
        x, y: Coordinates of the just-collapsed cell
        adjacency: Dictionary of adjacency rules
        tiles_x: Width of grid
        tiles_y: Height of grid
    
    Returns:
        Number of cells that were constrained
    """
    changes = 0
    stack = [(x, y)]
    
    while stack:
        cx, cy = stack.pop()
        current_cell = grid[cy][cx]
        
        if not current_cell.is_collapsed():
            continue
        
        current_tile = current_cell.tile_index
        
        # Check all four neighbors
        neighbors = [
            (cx, cy - 1, 'up'),      # Cell above
            (cx, cy + 1, 'down'),    # Cell below
            (cx - 1, cy, 'left'),    # Cell to left
            (cx + 1, cy, 'right')    # Cell to right
        ]
        
        for nx, ny, direction in neighbors:
            # Check if neighbor is in bounds
            if nx < 0 or nx >= tiles_x or ny < 0 or ny >= tiles_y:
                continue
            
            neighbor_cell = grid[ny][nx]
            
            # Skip if already collapsed
            if neighbor_cell.is_collapsed():
                continue
            
            # Get valid tiles for this direction
            valid_tiles = adjacency[current_tile][direction]
            
            # Constrain neighbor's options
            old_options = neighbor_cell.options.copy()
            neighbor_cell.options = [t for t in neighbor_cell.options if t in valid_tiles]
            
            # If options changed, add to stack to propagate further
            if neighbor_cell.options != old_options:
                changes += 1
                if (nx, ny) not in stack:
                    stack.append((nx, ny))
                    
                # Check for contradiction (no valid options)
                if len(neighbor_cell.options) == 0:
                    # Contradiction! This shouldn't happen with good rules
                    # For now, reset to all options
                    neighbor_cell.options = list(range(len(adjacency)))
    
    return changes


def render_grid_snapshot(grid, tiles, tiles_x, tiles_y, tile_size, output_path):
    """
    Render the current state of the grid to an image.
    Uncollapsed cells are shown with a grey placeholder.
    
    Args:
        grid: 2D array of Cell objects
        tiles: List of tile dictionaries
        tiles_x: Width of grid
        tiles_y: Height of grid
        tile_size: Size of each tile in pixels
        output_path: Path to save the snapshot
    """
    img_width = tiles_x * tile_size
    img_height = tiles_y * tile_size
    img = Image.new('RGB', (img_width, img_height), color='white')
    
    for y in range(tiles_y):
        for x in range(tiles_x):
            cell = grid[y][x]
            
            if cell.is_collapsed():
                # Use the actual tile
                tile_img = tiles[cell.tile_index]['image']
            else:
                # Use a grey square for uncollapsed cells
                tile_img = Image.new('RGB', (tile_size, tile_size), color=(200, 200, 200))
            
            paste_x = x * tile_size
            paste_y = y * tile_size
            img.paste(tile_img, (paste_x, paste_y))
    
    # Scale up 2x
    scaled_width = img_width * 2
    scaled_height = img_height * 2
    img = img.resize((scaled_width, scaled_height), Image.NEAREST)
    img.save(output_path)


def collapse_wfc(grid, tiles, adjacency, tiles_x, tiles_y, max_iterations=1000, save_steps=False, tile_size=16):
    """
    Main Wave Function Collapse algorithm.
    Iteratively collapses cells starting with lowest entropy.
    
    Args:
        grid: 2D array of Cell objects
        tiles: List of tile dictionaries
        adjacency: Dictionary of adjacency rules
        tiles_x: Width of grid
        tiles_y: Height of grid
        max_iterations: Maximum iterations to prevent infinite loops
        save_steps: Whether to save intermediate snapshots
        tile_size: Size of tiles for rendering snapshots
    
    Returns:
        Number of iterations used
    """
    import random
    import os
    
    print("\n=== Starting Wave Function Collapse ===")
    
    # Create steps directory if saving snapshots
    if save_steps:
        steps_dir = "static/images/WFC/WFCOutput/steps"
        os.makedirs(steps_dir, exist_ok=True)
        print(f"  Saving step-by-step snapshots to {steps_dir}/")
    
    iteration = 0
    while iteration < max_iterations:
        # Find cell with lowest entropy
        cell_coords = find_lowest_entropy_cell(grid, tiles_x, tiles_y)
        
        if cell_coords is None:
            print(f"All cells collapsed after {iteration} iterations!")
            break
        
        x, y = cell_coords
        cell = grid[y][x]
        
        # Collapse this cell to a random valid option
        if len(cell.options) == 0:
            print(f"ERROR: Cell at ({x},{y}) has no valid options!")
            break
        
        chosen_tile = random.choice(cell.options)
        cell.collapse(chosen_tile)
        
        # Propagate constraints to neighbors
        changes = propagate_constraints(grid, x, y, adjacency, tiles_x, tiles_y)
        
        iteration += 1
        
        # Save snapshot after each collapse if enabled
        if save_steps:
            snapshot_path = f"static/images/WFC/WFCOutput/steps/step_{iteration:03d}.png"
            render_grid_snapshot(grid, tiles, tiles_x, tiles_y, tile_size, snapshot_path)
        
        # Progress update every 10 iterations
        if iteration % 10 == 0:
            stats = analyze_entropy(grid, tiles_x, tiles_y)
            print(f"  Iteration {iteration}: Collapsed {stats['collapsed']}/{tiles_x * tiles_y}, "
                  f"Avg Entropy: {stats['average_entropy']:.2f}")
    
    # Save final snapshot if enabled
    if save_steps:
        print(f"  Saved {iteration + 1} snapshots (one per collapse)")
    
    return iteration









def setup(tile_size=16, output_width=160, output_height=160, input_image_path=None, save_steps=False):
   
   
    """
    Setup function to initialize parameters and start the WFC process.
    
    Args:
        tile_size: Size of each tile in pixels (e.g., 16x16)
        output_width: Width of output image in pixels
        output_height: Height of output image in pixels
        input_image_path: Path to the input tileset image
        save_steps: Whether to save step-by-step collapse snapshots
    
    Returns:
        Path to the generated output image
    """


    print(f"Setup: tile_size={tile_size}, output={output_width}x{output_height}")
    
    # Load tiles
    tiles = load_tiles()
    
    # Setup adjacency rules
    adjacency = setup_adjacency_rules(tiles)
    
    # Set default input path if none provided
    if input_image_path is None:
        input_image_path = "static/images/WFC/test.png"
    
    # Set output path
    output_path = "static/images/WFC/WFCOutput/output.png"
    
    # Ensure output directory exists
    os.makedirs("static/images/WFC/WFCOutput", exist_ok=True)
    
    # Call draw function to create the image
    draw(tiles, adjacency, tile_size, output_width, output_height, input_image_path, output_path, save_steps)
    
    return output_path









def draw(tiles, adjacency, tile_size, output_width, output_height, input_path, output_path, save_steps=False):
    
    
    """
    Create and save a Pillow image using tiles.
    
    Args:
        tiles: Array of tile dictionaries loaded from load_tiles()
        adjacency: Dictionary of adjacency rules
        tile_size: Size of each tile
        output_width: Width of output image in pixels
        output_height: Height of output image in pixels
        input_path: Path to input image
        output_path: Path to save output image
        save_steps: Whether to save step-by-step snapshots
    """

    
    print(f"Drawing image...")
    print(f"  Input: {input_path}")
    print(f"  Output: {output_path}")
    print(f"  Using {len(tiles)} tiles")
    
    if len(tiles) == 0:
        print("ERROR: No tiles loaded!")
        return
    
    # Calculate how many tiles fit in the output
    tiles_x = output_width // tile_size
    tiles_y = output_height // tile_size
    
    print(f"  Grid: {tiles_x}x{tiles_y} tiles ({tiles_x * tiles_y} total)")
    
    # Initialize the grid with cells
    # Each cell starts with all tiles as options
    grid = []
    all_tile_indices = list(range(len(tiles)))  # [0, 1, 2, 3, 4] for 5 tiles
    
    for y in range(tiles_y):
        row = []
        for x in range(tiles_x):
            # Create a new cell with all tiles as possible options
            cell = Cell(all_tile_indices)
            row.append(cell)
        grid.append(row)
    
    print(f"  Created {tiles_y}x{tiles_x} grid with {tiles_y * tiles_x} cells")
    print(f"  Each cell starts with {len(all_tile_indices)} possible options")
    
    # Analyze initial entropy
    stats = analyze_entropy(grid, tiles_x, tiles_y)
    print(f"\n  Initial State:")
    print(f"    Collapsed: {stats['collapsed']}")
    print(f"    Uncollapsed: {stats['uncollapsed']}")
    print(f"    Average Entropy: {stats['average_entropy']:.2f}")
    
    # Run the Wave Function Collapse algorithm
    iterations = collapse_wfc(grid, tiles, adjacency, tiles_x, tiles_y, 
                              save_steps=save_steps, tile_size=tile_size)
    
    # Analyze final entropy
    stats = analyze_entropy(grid, tiles_x, tiles_y)
    print(f"\n  Final State:")
    print(f"    Collapsed: {stats['collapsed']}")
    print(f"    Uncollapsed: {stats['uncollapsed']}")
    print(f"    Used {iterations} iterations")
    
    # Now render the grid to an image
    img = Image.new('RGB', (output_width, output_height), color='white')
    
    for y in range(tiles_y):
        for x in range(tiles_x):
            cell = grid[y][x]
            
            if cell.is_collapsed():
                # Get the tile for this cell
                tile_img = tiles[cell.tile_index]['image']
                
                # Calculate position to paste
                paste_x = x * tile_size
                paste_y = y * tile_size
                
                # Paste the tile
                img.paste(tile_img, (paste_x, paste_y))
    
    print(f"  Rendered all cells to image")
    
    # Scale up the image by 2x for better readability
    scaled_width = output_width * 2
    scaled_height = output_height * 2
    img = img.resize((scaled_width, scaled_height), Image.NEAREST)
    print(f"  Scaled image to {scaled_width}x{scaled_height} (2x)")
    
    img.save(output_path)
    print(f"Saved image to {output_path}")
if __name__ == "__main__":
    # Test the functions
    print("Testing WFC.py...")
    output = setup(tile_size=16, output_width=160, output_height=160, save_steps=True)
    print(f"Done! Check {output}")
    print(f"Step-by-step snapshots saved to static/images/WFC/WFCOutput/steps/")

