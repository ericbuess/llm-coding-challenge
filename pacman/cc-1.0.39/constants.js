const CONSTANTS = {
    TILE_SIZE: 20,
    MAZE_WIDTH: 28,
    MAZE_HEIGHT: 31,
    
    DIRECTIONS: {
        UP: { x: 0, y: -1 },
        DOWN: { x: 0, y: 1 },
        LEFT: { x: -1, y: 0 },
        RIGHT: { x: 1, y: 0 }
    },
    
    COLORS: {
        WALL: '#0000ff',
        PELLET: '#ffb8ae',
        POWER_PELLET: '#ffb8ae',
        PACMAN: '#ffff00',
        BLINKY: '#ff0000',
        PINKY: '#ffb8ff',
        INKY: '#00ffff',
        CLYDE: '#ffb852',
        SCARED_GHOST: '#0000ff',
        SCARED_GHOST_WHITE: '#ffffff'
    },
    
    POINTS: {
        PELLET: 10,
        POWER_PELLET: 50,
        GHOST: [200, 400, 800, 1600],
        FRUIT: {
            CHERRY: 100,
            STRAWBERRY: 300,
            ORANGE: 500,
            APPLE: 700,
            MELON: 1000
        }
    },
    
    GAME_STATES: {
        MENU: 'menu',
        PLAYING: 'playing',
        PAUSED: 'paused',
        GAME_OVER: 'game_over',
        LEVEL_COMPLETE: 'level_complete'
    },
    
    GHOST_MODES: {
        SCATTER: 'scatter',
        CHASE: 'chase',
        FRIGHTENED: 'frightened',
        EATEN: 'eaten'
    },
    
    SPEEDS: {
        PACMAN: 0.2,
        GHOST_NORMAL: 0.15,
        GHOST_FRIGHTENED: 0.1,
        GHOST_EATEN: 0.3
    },
    
    TIMERS: {
        FRIGHTENED_TIME: 6000,
        SCATTER_TIME: 7000,
        CHASE_TIME: 20000
    }
};