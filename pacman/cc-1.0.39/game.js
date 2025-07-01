class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.renderer = new Renderer(this.canvas);
        this.inputManager = new InputManager();
        this.soundManager = new SoundManager();
        
        this.state = CONSTANTS.GAME_STATES.MENU;
        this.level = 1;
        this.score = 0;
        this.lives = 3;
        this.ghostsEaten = 0;
        
        this.maze = null;
        this.pacman = null;
        this.ghosts = [];
        
        this.modeTimer = 0;
        this.currentGhostMode = CONSTANTS.GHOST_MODES.SCATTER;
        
        this.lastTime = 0;
        this.init();
    }
    
    init() {
        this.setupLevel();
        this.gameLoop(0);
    }
    
    setupLevel() {
        this.maze = new Maze(this.level);
        this.pacman = new Pacman(14, 17);
        
        this.ghosts = [
            new Ghost('blinky', 14, 11, CONSTANTS.COLORS.BLINKY, { x: 25, y: 0 }),
            new Ghost('pinky', 14, 13, CONSTANTS.COLORS.PINKY, { x: 2, y: 0 }),
            new Ghost('inky', 12, 13, CONSTANTS.COLORS.INKY, { x: 27, y: 31 }),
            new Ghost('clyde', 16, 13, CONSTANTS.COLORS.CLYDE, { x: 0, y: 31 })
        ];
        
        this.ghosts.forEach(ghost => {
            ghost.speed = CONSTANTS.SPEEDS.GHOST_NORMAL + (this.level - 1) * 0.02;
        });
        
        this.modeTimer = CONSTANTS.TIMERS.SCATTER_TIME;
        this.currentGhostMode = CONSTANTS.GHOST_MODES.SCATTER;
    }
    
    gameLoop(currentTime) {
        const deltaTime = currentTime - this.lastTime;
        this.lastTime = currentTime;
        
        this.update(deltaTime);
        this.render();
        
        requestAnimationFrame((time) => this.gameLoop(time));
    }
    
    update(deltaTime) {
        if (this.state === CONSTANTS.GAME_STATES.MENU) {
            if (this.inputManager.consumeKey(' ')) {
                this.state = CONSTANTS.GAME_STATES.PLAYING;
                this.soundManager.play('start');
            }
            return;
        }
        
        if (this.state === CONSTANTS.GAME_STATES.GAME_OVER) {
            if (this.inputManager.consumeKey(' ')) {
                this.resetGame();
            }
            return;
        }
        
        if (this.state === CONSTANTS.GAME_STATES.LEVEL_COMPLETE) {
            if (this.inputManager.consumeKey(' ')) {
                this.nextLevel();
            }
            return;
        }
        
        if (this.state === CONSTANTS.GAME_STATES.PLAYING) {
            this.updateGhostMode(deltaTime);
            
            const pelletResult = this.pacman.update(this.maze, this.inputManager);
            if (pelletResult) {
                this.score += pelletResult.points;
                this.updateScore();
                
                if (pelletResult.type === 'powerPellet') {
                    this.soundManager.play('powerPellet');
                    this.ghostsEaten = 0;
                    this.ghosts.forEach(ghost => ghost.setFrightened());
                } else {
                    this.soundManager.play('chomp');
                }
            }
            
            this.ghosts.forEach(ghost => {
                ghost.update(this.maze, this.pacman, this.ghosts, this.level);
            });
            
            this.checkCollisions();
            
            if (this.maze.getRemainingPellets() === 0) {
                this.state = CONSTANTS.GAME_STATES.LEVEL_COMPLETE;
            }
        }
    }
    
    updateGhostMode(deltaTime) {
        if (this.modeTimer > 0) {
            this.modeTimer -= deltaTime;
            
            if (this.modeTimer <= 0) {
                if (this.currentGhostMode === CONSTANTS.GHOST_MODES.SCATTER) {
                    this.currentGhostMode = CONSTANTS.GHOST_MODES.CHASE;
                    this.modeTimer = CONSTANTS.TIMERS.CHASE_TIME;
                } else {
                    this.currentGhostMode = CONSTANTS.GHOST_MODES.SCATTER;
                    this.modeTimer = CONSTANTS.TIMERS.SCATTER_TIME;
                }
                
                this.ghosts.forEach(ghost => {
                    if (ghost.mode !== CONSTANTS.GHOST_MODES.FRIGHTENED && !ghost.eaten) {
                        ghost.mode = this.currentGhostMode;
                    }
                });
            }
        }
    }
    
    checkCollisions() {
        const pacmanTileX = Math.floor(this.pacman.x);
        const pacmanTileY = Math.floor(this.pacman.y);
        
        this.ghosts.forEach(ghost => {
            const ghostTileX = Math.floor(ghost.x);
            const ghostTileY = Math.floor(ghost.y);
            
            if (Math.abs(this.pacman.x - ghost.x) < 0.8 && 
                Math.abs(this.pacman.y - ghost.y) < 0.8) {
                
                if (ghost.mode === CONSTANTS.GHOST_MODES.FRIGHTENED && !ghost.eaten) {
                    ghost.setEaten();
                    this.score += CONSTANTS.POINTS.GHOST[Math.min(this.ghostsEaten, 3)];
                    this.ghostsEaten++;
                    this.updateScore();
                    this.soundManager.play('eatGhost');
                } else if (!ghost.eaten) {
                    this.loseLife();
                }
            }
        });
    }
    
    loseLife() {
        this.lives--;
        this.updateLives();
        this.soundManager.play('death');
        
        if (this.lives === 0) {
            this.state = CONSTANTS.GAME_STATES.GAME_OVER;
            document.getElementById('gameOver').style.display = 'block';
        } else {
            this.pacman.reset();
            this.ghosts.forEach(ghost => ghost.reset());
            this.modeTimer = CONSTANTS.TIMERS.SCATTER_TIME;
            this.currentGhostMode = CONSTANTS.GHOST_MODES.SCATTER;
        }
    }
    
    nextLevel() {
        this.level++;
        this.updateLevel();
        this.setupLevel();
        this.state = CONSTANTS.GAME_STATES.PLAYING;
    }
    
    resetGame() {
        this.level = 1;
        this.score = 0;
        this.lives = 3;
        this.ghostsEaten = 0;
        
        this.updateScore();
        this.updateLives();
        this.updateLevel();
        
        document.getElementById('gameOver').style.display = 'none';
        
        this.setupLevel();
        this.state = CONSTANTS.GAME_STATES.PLAYING;
    }
    
    render() {
        this.renderer.clear();
        
        if (this.state === CONSTANTS.GAME_STATES.MENU) {
            this.renderer.drawGameState(this.state);
        } else {
            this.renderer.drawMaze(this.maze);
            this.renderer.drawPellets(this.maze);
            this.renderer.drawPacman(this.pacman);
            this.ghosts.forEach(ghost => this.renderer.drawGhost(ghost));
            
            if (this.state === CONSTANTS.GAME_STATES.LEVEL_COMPLETE) {
                this.renderer.ctx.fillStyle = 'white';
                this.renderer.ctx.font = '24px Arial';
                this.renderer.ctx.textAlign = 'center';
                this.renderer.ctx.fillText(
                    `Level ${this.level} Complete! Press SPACE`,
                    this.canvas.width / 2,
                    this.canvas.height / 2
                );
            }
        }
    }
    
    updateScore() {
        document.getElementById('score').textContent = `Score: ${this.score}`;
    }
    
    updateLives() {
        document.getElementById('lives').textContent = `Lives: ${this.lives}`;
    }
    
    updateLevel() {
        document.getElementById('level').textContent = `Level: ${this.level}`;
    }
}

const game = new Game();