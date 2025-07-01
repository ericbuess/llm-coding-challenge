class Pacman {
    constructor(x, y) {
        this.startX = x;
        this.startY = y;
        this.x = x;
        this.y = y;
        this.direction = CONSTANTS.DIRECTIONS.LEFT;
        this.nextDirection = null;
        this.speed = CONSTANTS.SPEEDS.PACMAN;
        this.animationFrame = 0;
        this.animationCounter = 0;
        this.mouthOpen = true;
    }
    
    update(maze, inputManager) {
        this.handleInput(inputManager);
        
        if (this.nextDirection && maze.canMove(this.x, this.y, this.nextDirection)) {
            this.direction = this.nextDirection;
            this.nextDirection = null;
        }
        
        if (maze.canMove(this.x, this.y, this.direction)) {
            this.x += this.direction.x * this.speed;
            this.y += this.direction.y * this.speed;
            
            this.handlePortals();
            
            this.animationCounter++;
            if (this.animationCounter % 5 === 0) {
                this.mouthOpen = !this.mouthOpen;
            }
        }
        
        return maze.checkPelletCollision(this.x, this.y);
    }
    
    handleInput(inputManager) {
        if (inputManager.isKeyPressed('ArrowUp')) {
            this.nextDirection = CONSTANTS.DIRECTIONS.UP;
        } else if (inputManager.isKeyPressed('ArrowDown')) {
            this.nextDirection = CONSTANTS.DIRECTIONS.DOWN;
        } else if (inputManager.isKeyPressed('ArrowLeft')) {
            this.nextDirection = CONSTANTS.DIRECTIONS.LEFT;
        } else if (inputManager.isKeyPressed('ArrowRight')) {
            this.nextDirection = CONSTANTS.DIRECTIONS.RIGHT;
        }
    }
    
    handlePortals() {
        if (this.x < 0) {
            this.x = CONSTANTS.MAZE_WIDTH - 1;
        } else if (this.x >= CONSTANTS.MAZE_WIDTH) {
            this.x = 0;
        }
    }
    
    reset() {
        this.x = this.startX;
        this.y = this.startY;
        this.direction = CONSTANTS.DIRECTIONS.LEFT;
        this.nextDirection = null;
        this.animationFrame = 0;
        this.animationCounter = 0;
        this.mouthOpen = true;
    }
    
    getRotationAngle() {
        if (this.direction === CONSTANTS.DIRECTIONS.RIGHT) return 0;
        if (this.direction === CONSTANTS.DIRECTIONS.DOWN) return Math.PI / 2;
        if (this.direction === CONSTANTS.DIRECTIONS.LEFT) return Math.PI;
        if (this.direction === CONSTANTS.DIRECTIONS.UP) return Math.PI * 1.5;
        return 0;
    }
}