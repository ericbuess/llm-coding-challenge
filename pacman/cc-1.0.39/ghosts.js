class Ghost {
    constructor(name, x, y, color, scatterTarget) {
        this.name = name;
        this.startX = x;
        this.startY = y;
        this.x = x;
        this.y = y;
        this.color = color;
        this.direction = CONSTANTS.DIRECTIONS.UP;
        this.mode = CONSTANTS.GHOST_MODES.SCATTER;
        this.previousMode = null;
        this.scatterTarget = scatterTarget;
        this.speed = CONSTANTS.SPEEDS.GHOST_NORMAL;
        this.frightenedTimer = 0;
        this.eaten = false;
        this.animationFrame = 0;
        this.animationCounter = 0;
    }
    
    update(maze, pacman, ghosts, level) {
        this.animationCounter++;
        if (this.animationCounter % 10 === 0) {
            this.animationFrame = (this.animationFrame + 1) % 2;
        }
        
        if (this.frightenedTimer > 0) {
            this.frightenedTimer--;
            if (this.frightenedTimer === 0 && this.mode === CONSTANTS.GHOST_MODES.FRIGHTENED) {
                this.mode = this.previousMode || CONSTANTS.GHOST_MODES.SCATTER;
                this.speed = CONSTANTS.SPEEDS.GHOST_NORMAL + (level - 1) * 0.02;
            }
        }
        
        const target = this.getTarget(pacman, ghosts);
        const nextDirection = this.getNextDirection(maze, target);
        
        if (nextDirection) {
            this.direction = nextDirection;
        }
        
        if (maze.canMove(this.x, this.y, this.direction)) {
            this.x += this.direction.x * this.speed;
            this.y += this.direction.y * this.speed;
            
            this.handlePortals();
        }
        
        if (this.eaten && Math.abs(this.x - this.startX) < 0.5 && Math.abs(this.y - this.startY) < 0.5) {
            this.eaten = false;
            this.mode = this.previousMode || CONSTANTS.GHOST_MODES.SCATTER;
            this.speed = CONSTANTS.SPEEDS.GHOST_NORMAL + (level - 1) * 0.02;
        }
    }
    
    getTarget(pacman, ghosts) {
        if (this.eaten) {
            return { x: this.startX, y: this.startY };
        }
        
        if (this.mode === CONSTANTS.GHOST_MODES.FRIGHTENED) {
            return {
                x: Math.random() * CONSTANTS.MAZE_WIDTH,
                y: Math.random() * CONSTANTS.MAZE_HEIGHT
            };
        }
        
        if (this.mode === CONSTANTS.GHOST_MODES.SCATTER) {
            return this.scatterTarget;
        }
        
        switch (this.name) {
            case 'blinky':
                return { x: pacman.x, y: pacman.y };
                
            case 'pinky':
                return {
                    x: pacman.x + pacman.direction.x * 4,
                    y: pacman.y + pacman.direction.y * 4
                };
                
            case 'inky':
                const blinky = ghosts.find(g => g.name === 'blinky');
                const pivotX = pacman.x + pacman.direction.x * 2;
                const pivotY = pacman.y + pacman.direction.y * 2;
                return {
                    x: pivotX * 2 - blinky.x,
                    y: pivotY * 2 - blinky.y
                };
                
            case 'clyde':
                const distance = Math.sqrt(
                    Math.pow(pacman.x - this.x, 2) + 
                    Math.pow(pacman.y - this.y, 2)
                );
                if (distance < 8) {
                    return this.scatterTarget;
                }
                return { x: pacman.x, y: pacman.y };
                
            default:
                return { x: pacman.x, y: pacman.y };
        }
    }
    
    getNextDirection(maze, target) {
        const possibleDirections = this.getPossibleDirections(maze);
        
        if (possibleDirections.length === 0) {
            return null;
        }
        
        if (this.mode === CONSTANTS.GHOST_MODES.FRIGHTENED && !this.eaten) {
            return possibleDirections[Math.floor(Math.random() * possibleDirections.length)];
        }
        
        let bestDirection = null;
        let bestDistance = Infinity;
        
        for (let dir of possibleDirections) {
            const nextX = this.x + dir.x;
            const nextY = this.y + dir.y;
            const distance = Math.sqrt(
                Math.pow(target.x - nextX, 2) + 
                Math.pow(target.y - nextY, 2)
            );
            
            if (distance < bestDistance) {
                bestDistance = distance;
                bestDirection = dir;
            }
        }
        
        return bestDirection;
    }
    
    getPossibleDirections(maze) {
        const opposite = this.getOppositeDirection(this.direction);
        const directions = [];
        
        for (let key in CONSTANTS.DIRECTIONS) {
            const dir = CONSTANTS.DIRECTIONS[key];
            if (dir !== opposite && maze.canMove(this.x, this.y, dir)) {
                directions.push(dir);
            }
        }
        
        if (directions.length === 0 && maze.canMove(this.x, this.y, opposite)) {
            directions.push(opposite);
        }
        
        return directions;
    }
    
    getOppositeDirection(direction) {
        if (direction === CONSTANTS.DIRECTIONS.UP) return CONSTANTS.DIRECTIONS.DOWN;
        if (direction === CONSTANTS.DIRECTIONS.DOWN) return CONSTANTS.DIRECTIONS.UP;
        if (direction === CONSTANTS.DIRECTIONS.LEFT) return CONSTANTS.DIRECTIONS.RIGHT;
        if (direction === CONSTANTS.DIRECTIONS.RIGHT) return CONSTANTS.DIRECTIONS.LEFT;
        return null;
    }
    
    handlePortals() {
        if (this.x < 0) {
            this.x = CONSTANTS.MAZE_WIDTH - 1;
        } else if (this.x >= CONSTANTS.MAZE_WIDTH) {
            this.x = 0;
        }
    }
    
    setFrightened() {
        if (!this.eaten) {
            this.previousMode = this.mode;
            this.mode = CONSTANTS.GHOST_MODES.FRIGHTENED;
            this.speed = CONSTANTS.SPEEDS.GHOST_FRIGHTENED;
            this.frightenedTimer = CONSTANTS.TIMERS.FRIGHTENED_TIME / 16;
            this.direction = this.getOppositeDirection(this.direction);
        }
    }
    
    setEaten() {
        this.eaten = true;
        this.mode = CONSTANTS.GHOST_MODES.EATEN;
        this.speed = CONSTANTS.SPEEDS.GHOST_EATEN;
    }
    
    reset() {
        this.x = this.startX;
        this.y = this.startY;
        this.direction = CONSTANTS.DIRECTIONS.UP;
        this.mode = CONSTANTS.GHOST_MODES.SCATTER;
        this.previousMode = null;
        this.speed = CONSTANTS.SPEEDS.GHOST_NORMAL;
        this.frightenedTimer = 0;
        this.eaten = false;
        this.animationFrame = 0;
        this.animationCounter = 0;
    }
}