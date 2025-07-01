# Pac-Man Browser Game

A fully-featured browser-based Pac-Man game with automated testing and validation.

## Features

- Classic Pac-Man gameplay with 5 progressive difficulty levels
- Four unique ghost AI behaviors (Blinky, Pinky, Inky, Clyde)
- Power pellets and frightened ghost mode
- Portal/tunnel mechanics
- Sound effects using Web Audio API
- Smooth 60 FPS performance
- Responsive keyboard controls

## How to Play

1. Start the game server:
   ```bash
   npm start
   ```

2. Open your browser to `http://localhost:8000`

3. Controls:
   - **Space**: Start game / Continue after game over
   - **Arrow Keys**: Move Pac-Man

## Game Mechanics

- **Pellets**: 10 points each
- **Power Pellets**: 50 points each, makes ghosts vulnerable
- **Eating Ghosts**: 200, 400, 800, 1600 points (consecutive)
- **Lives**: Start with 3 lives
- **Levels**: 5 levels with increasing difficulty

## Ghost Behaviors

- **Blinky (Red)**: Direct chase - always targets Pac-Man's position
- **Pinky (Pink)**: Ambush - targets 4 tiles ahead of Pac-Man
- **Inky (Cyan)**: Flanking - uses Blinky's position to calculate target
- **Clyde (Orange)**: Shy - chases when far, scatters when close

## Testing

### Automated Testing
```bash
npm test
```

Runs comprehensive automated tests including:
- Game initialization
- Movement controls
- Pellet collection
- Ghost collision
- Power pellet effects
- Portal functionality
- Level progression
- Performance benchmarks

### Independent Validation
```bash
npm run validate
```

Runs unbiased validation testing:
- All 5 levels playability
- User experience validation
- Performance monitoring
- Bug detection

## Development

### Project Structure
```
├── index.html          # Game container
├── constants.js        # Game constants and configuration
├── game.js            # Main game logic and state management
├── entities.js        # Pac-Man entity
├── ghosts.js          # Ghost AI and behaviors
├── maze.js            # Maze layout and collision detection
├── renderer.js        # Canvas rendering engine
├── sounds.js          # Sound effects manager
├── input.js           # Keyboard input handling
├── test/              # Automated testing suite
└── validation/        # Independent validation
```

### Performance

The game maintains 60+ FPS performance through:
- Efficient collision detection
- Optimized rendering pipeline
- Smart ghost AI pathfinding
- Minimal DOM manipulation

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (may need to enable Web Audio)

## Known Issues

- Sound may not work on first interaction in some browsers (user gesture required)
- High DPI displays may show slight rendering artifacts

## Credits

Classic Pac-Man game mechanics recreation for educational purposes.