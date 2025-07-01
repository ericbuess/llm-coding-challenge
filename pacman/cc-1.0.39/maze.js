class Maze {
    constructor(level = 1) {
        this.level = level;
        this.layout = this.getMazeLayout();
        this.pellets = [];
        this.powerPellets = [];
        this.totalPellets = 0;
        this.initializePellets();
    }
    
    getMazeLayout() {
        return [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
            [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1],
            [0,0,0,0,0,1,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,1,0,0,0,0,0],
            [1,1,1,1,1,1,2,1,1,2,1,1,1,0,0,1,1,1,2,1,1,2,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,2,1,1,2,1,0,0,0,0,0,0,1,2,1,1,2,1,1,1,1,1,1],
            [0,0,0,0,0,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,0,0,0,0,0],
            [1,1,1,1,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
            [1,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,1],
            [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
            [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
            [1,3,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,3,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ];
    }
    
    initializePellets() {
        this.pellets = [];
        this.powerPellets = [];
        this.totalPellets = 0;
        
        for (let y = 0; y < this.layout.length; y++) {
            for (let x = 0; x < this.layout[y].length; x++) {
                if (this.layout[y][x] === 2) {
                    this.pellets.push({ x, y, eaten: false });
                    this.totalPellets++;
                } else if (this.layout[y][x] === 3) {
                    this.powerPellets.push({ x, y, eaten: false });
                    this.totalPellets++;
                }
            }
        }
    }
    
    isWall(x, y) {
        const tileX = Math.floor(x);
        const tileY = Math.floor(y);
        
        if (tileY < 0 || tileY >= this.layout.length || 
            tileX < 0 || tileX >= this.layout[0].length) {
            return true;
        }
        
        return this.layout[tileY][tileX] === 1;
    }
    
    canMove(x, y, direction) {
        const nextX = x + direction.x * 0.5;
        const nextY = y + direction.y * 0.5;
        
        const corners = [
            { x: nextX - 0.4, y: nextY - 0.4 },
            { x: nextX + 0.4, y: nextY - 0.4 },
            { x: nextX - 0.4, y: nextY + 0.4 },
            { x: nextX + 0.4, y: nextY + 0.4 }
        ];
        
        return corners.every(corner => !this.isWall(corner.x, corner.y));
    }
    
    checkPelletCollision(x, y) {
        const tileX = Math.floor(x);
        const tileY = Math.floor(y);
        
        for (let pellet of this.pellets) {
            if (!pellet.eaten && pellet.x === tileX && pellet.y === tileY) {
                pellet.eaten = true;
                return { type: 'pellet', points: CONSTANTS.POINTS.PELLET };
            }
        }
        
        for (let powerPellet of this.powerPellets) {
            if (!powerPellet.eaten && powerPellet.x === tileX && powerPellet.y === tileY) {
                powerPellet.eaten = true;
                return { type: 'powerPellet', points: CONSTANTS.POINTS.POWER_PELLET };
            }
        }
        
        return null;
    }
    
    getRemainingPellets() {
        const remainingPellets = this.pellets.filter(p => !p.eaten).length;
        const remainingPowerPellets = this.powerPellets.filter(p => !p.eaten).length;
        return remainingPellets + remainingPowerPellets;
    }
    
    getTileAt(x, y) {
        const tileX = Math.floor(x);
        const tileY = Math.floor(y);
        
        if (tileY >= 0 && tileY < this.layout.length && 
            tileX >= 0 && tileX < this.layout[0].length) {
            return this.layout[tileY][tileX];
        }
        
        return 1;
    }
}