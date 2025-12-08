# Wave Function Collapse - Tile Configuration Guide

## Overview
The WFC system now uses a **config-based approach** where tiles and their adjacency rules are automatically generated from a configuration dictionary. This makes it easy to add new tiles without hard-coding rules!

## How It Works

### 1. Tile Connections
Each tile defines which **directions** it has connections in:
- `up`: Connection pointing upward
- `down`: Connection pointing downward
- `left`: Connection pointing leftward
- `right`: Connection pointing rightward

Connection values can be:
- `None`: No connection in this direction (endpoint)
- `'road'`: Road connection
- `'grass'`: Grass/field connection
- `'building'`: Building connection
- Or any custom string you want!

### 2. Adjacency Rule Generation
The system **automatically** determines which tiles can be adjacent by checking if their **facing connections match**:

```
Tile A can be to the RIGHT of Tile B if:
  Tile B's RIGHT connection == Tile A's LEFT connection
```

### 3. Adding New Tiles

Simply add an entry to `TILE_CONFIGS` in `classes/WFC.py`:

```python
TILE_CONFIGS = {
    'your_tile_name': {
        'file': 'your_tile.png',      # PNG file in basic_tiles folder
        'connections': {
            'up': 'road',              # or None, or another type
            'down': None,
            'left': 'grass',
            'right': 'building'
        },
        'description': 'Your tile description'
    }
}
```

## Example: Building a City

### Current Tiles (Roads)
```python
'blank': {
    'file': 'blank.png',
    'connections': {'up': None, 'down': None, 'left': None, 'right': None}
}
# This is an endpoint - connects to nothing

'road_vertical': {
    'file': 'up.png',
    'connections': {'up': 'road', 'down': None, 'left': 'road', 'right': 'road'}
}
# Has road going up, left, and right

'road_horizontal': {
    'file': 'down.png',
    'connections': {'up': None, 'down': 'road', 'left': 'road', 'right': 'road'}
}
# Has road going down, left, and right
```

### Adding New City Tiles

#### 1. Road Intersection (4-way)
```python
'road_4way': {
    'file': 'road_4way.png',
    'connections': {
        'up': 'road',
        'down': 'road',
        'left': 'road',
        'right': 'road'
    },
    'description': '4-way road intersection'
}
```

#### 2. Building with Door on Bottom
```python
'building_south_door': {
    'file': 'building_s.png',
    'connections': {
        'up': 'building',
        'down': 'road',      # Door faces road
        'left': 'building',
        'right': 'building'
    },
    'description': 'Building with south-facing door'
}
```

#### 3. Grass/Field
```python
'grass': {
    'file': 'grass.png',
    'connections': {
        'up': 'grass',
        'down': 'grass',
        'left': 'grass',
        'right': 'grass'
    },
    'description': 'Grass field tile'
}
```

#### 4. Grass-to-Road Transition
```python
'grass_road_transition': {
    'file': 'grass_road.png',
    'connections': {
        'up': 'grass',
        'down': 'road',
        'left': 'grass',
        'right': 'grass'
    },
    'description': 'Transition from grass to road'
}
```

## Connection Type Strategy

### For a City Theme:
- `None`: Empty/void spaces (endpoints)
- `'road'`: All road tiles
- `'building'`: Building walls/edges
- `'grass'`: Grass/field areas
- `'sidewalk'`: Sidewalks next to roads
- `'water'`: Rivers/ponds
- `'fence'`: Fences around properties

### Example City Block:
```python
# Road tiles with 'road' connections
# Building tiles with 'building' on 3 sides, 'road' on door side
# Grass tiles with 'grass' connections
# Fence tiles with 'fence' on outside, 'grass' on inside
```

## Benefits

✅ **No Hard-Coding**: Add tiles without touching adjacency logic
✅ **Flexible**: Mix and match connection types
✅ **Scalable**: Add hundreds of tiles easily
✅ **Clear**: Easy to see what connects to what
✅ **Maintainable**: Change one tile's connections, rules update automatically

## Testing Your Tiles

1. Add your config entry to `TILE_CONFIGS`
2. Create the PNG file in `static/images/WFC/WFCTiles/basic_tiles/`
3. Run `python classes\WFC.py`
4. Check the output and adjacency rules printout
5. View step-by-step at http://127.0.0.1:5000/wfc-steps

## Tips

- Start with a small set of tiles and test
- Use consistent connection type names
- Draw tiles at 16x16 pixels for now
- Make sure tile edges visually match their connections
- Test frequently to catch connection mismatches early

Happy tile building! 🎨🏙️
