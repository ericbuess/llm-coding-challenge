class Renderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.canvas.width = CONSTANTS.MAZE_WIDTH * CONSTANTS.TILE_SIZE;
        this.canvas.height = CONSTANTS.MAZE_HEIGHT * CONSTANTS.TILE_SIZE;
    }
    
    clear() {
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    drawMaze(maze) {
        for (let y = 0; y < maze.layout.length; y++) {
            for (let x = 0; x < maze.layout[y].length; x++) {
                if (maze.layout[y][x] === 1) {
                    this.drawWall(x, y);
                }
            }
        }
    }
    
    drawWall(x, y) {
        this.ctx.fillStyle = CONSTANTS.COLORS.WALL;
        this.ctx.fillRect(
            x * CONSTANTS.TILE_SIZE,
            y * CONSTANTS.TILE_SIZE,
            CONSTANTS.TILE_SIZE,
            CONSTANTS.TILE_SIZE
        );
        
        this.ctx.strokeStyle = '#000';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(
            x * CONSTANTS.TILE_SIZE,
            y * CONSTANTS.TILE_SIZE,
            CONSTANTS.TILE_SIZE,
            CONSTANTS.TILE_SIZE
        );
    }
    
    drawPellets(maze) {
        for (let pellet of maze.pellets) {
            if (!pellet.eaten) {
                this.drawPellet(pellet.x, pellet.y);
            }
        }
        
        for (let powerPellet of maze.powerPellets) {
            if (!powerPellet.eaten) {
                this.drawPowerPellet(powerPellet.x, powerPellet.y);
            }
        }
    }
    
    drawPellet(x, y) {
        this.ctx.fillStyle = CONSTANTS.COLORS.PELLET;
        this.ctx.beginPath();
        this.ctx.arc(
            x * CONSTANTS.TILE_SIZE + CONSTANTS.TILE_SIZE / 2,
            y * CONSTANTS.TILE_SIZE + CONSTANTS.TILE_SIZE / 2,
            3,
            0,
            Math.PI * 2
        );
        this.ctx.fill();
    }
    
    drawPowerPellet(x, y) {
        this.ctx.fillStyle = CONSTANTS.COLORS.POWER_PELLET;
        this.ctx.beginPath();
        this.ctx.arc(
            x * CONSTANTS.TILE_SIZE + CONSTANTS.TILE_SIZE / 2,
            y * CONSTANTS.TILE_SIZE + CONSTANTS.TILE_SIZE / 2,
            6,
            0,
            Math.PI * 2
        );
        this.ctx.fill();
    }
    
    drawPacman(pacman) {
        const centerX = pacman.x * CONSTANTS.TILE_SIZE + CONSTANTS.TILE_SIZE / 2;
        const centerY = pacman.y * CONSTANTS.TILE_SIZE + CONSTANTS.TILE_SIZE / 2;
        const radius = CONSTANTS.TILE_SIZE / 2 - 2;
        
        this.ctx.save();
        this.ctx.translate(centerX, centerY);
        this.ctx.rotate(pacman.getRotationAngle());
        
        this.ctx.fillStyle = CONSTANTS.COLORS.PACMAN;
        this.ctx.beginPath();
        
        if (pacman.mouthOpen) {
            this.ctx.arc(0, 0, radius, 0.2 * Math.PI, 1.8 * Math.PI);
            this.ctx.lineTo(0, 0);
        } else {
            this.ctx.arc(0, 0, radius, 0, Math.PI * 2);
        }
        
        this.ctx.closePath();
        this.ctx.fill();
        
        this.ctx.restore();
    }
    
    drawGhost(ghost) {
        const centerX = ghost.x * CONSTANTS.TILE_SIZE + CONSTANTS.TILE_SIZE / 2;
        const centerY = ghost.y * CONSTANTS.TILE_SIZE + CONSTANTS.TILE_SIZE / 2;
        const radius = CONSTANTS.TILE_SIZE / 2 - 2;
        
        let color = ghost.color;
        if (ghost.eaten) {
            this.drawEatenGhost(centerX, centerY);
            return;
        } else if (ghost.mode === CONSTANTS.GHOST_MODES.FRIGHTENED) {
            if (ghost.frightenedTimer < 120 && Math.floor(ghost.frightenedTimer / 20) % 2 === 0) {
                color = CONSTANTS.COLORS.SCARED_GHOST_WHITE;
            } else {
                color = CONSTANTS.COLORS.SCARED_GHOST;
            }
        }
        
        this.ctx.fillStyle = color;
        
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY - radius / 2, radius, Math.PI, 0);
        this.ctx.lineTo(centerX + radius, centerY + radius / 2);
        
        for (let i = 0; i < 3; i++) {
            const x = centerX + radius - (i + 1) * (radius * 2 / 3);
            const y = centerY + radius / 2;
            this.ctx.lineTo(x, y - 4);
            this.ctx.lineTo(x - radius * 2 / 3, y);
        }
        
        this.ctx.lineTo(centerX - radius, centerY + radius / 2);
        this.ctx.closePath();
        this.ctx.fill();
        
        this.drawGhostEyes(centerX, centerY, ghost.direction);
    }
    
    drawGhostEyes(centerX, centerY, direction) {
        const eyeRadius = 3;
        const pupilRadius = 1.5;
        const eyeOffsetX = 5;
        const eyeOffsetY = -5;
        
        this.ctx.fillStyle = 'white';
        this.ctx.beginPath();
        this.ctx.arc(centerX - eyeOffsetX, centerY + eyeOffsetY, eyeRadius, 0, Math.PI * 2);
        this.ctx.arc(centerX + eyeOffsetX, centerY + eyeOffsetY, eyeRadius, 0, Math.PI * 2);
        this.ctx.fill();
        
        let pupilOffsetX = direction.x * 2;
        let pupilOffsetY = direction.y * 2;
        
        this.ctx.fillStyle = 'black';
        this.ctx.beginPath();
        this.ctx.arc(
            centerX - eyeOffsetX + pupilOffsetX,
            centerY + eyeOffsetY + pupilOffsetY,
            pupilRadius,
            0,
            Math.PI * 2
        );
        this.ctx.arc(
            centerX + eyeOffsetX + pupilOffsetX,
            centerY + eyeOffsetY + pupilOffsetY,
            pupilRadius,
            0,
            Math.PI * 2
        );
        this.ctx.fill();
    }
    
    drawEatenGhost(centerX, centerY) {
        this.drawGhostEyes(centerX, centerY, { x: 0, y: 0 });
    }
    
    drawGameState(state) {
        if (state === CONSTANTS.GAME_STATES.MENU) {
            this.ctx.fillStyle = 'white';
            this.ctx.font = '24px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(
                'Press SPACE to Start',
                this.canvas.width / 2,
                this.canvas.height / 2
            );
        }
    }
}