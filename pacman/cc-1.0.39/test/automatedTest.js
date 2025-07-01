const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

class PacmanAutomatedTest {
    constructor() {
        this.browser = null;
        this.page = null;
        this.testResults = [];
        this.screenshotDir = path.join(__dirname, 'screenshots');
    }
    
    async setup() {
        await fs.mkdir(this.screenshotDir, { recursive: true });
        
        this.browser = await puppeteer.launch({
            headless: false,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        this.page = await this.browser.newPage();
        await this.page.setViewport({ width: 1200, height: 800 });
        
        console.log('Starting local server...');
        const { spawn } = require('child_process');
        this.server = spawn('python3', ['-m', 'http.server', '8000'], {
            cwd: path.join(__dirname, '..')
        });
        
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        await this.page.goto('http://localhost:8000');
        console.log('Test environment ready');
    }
    
    async teardown() {
        if (this.browser) {
            await this.browser.close();
        }
        if (this.server) {
            this.server.kill();
        }
    }
    
    async captureScreenshot(name) {
        const screenshotPath = path.join(this.screenshotDir, `${name}.png`);
        await this.page.screenshot({ path: screenshotPath });
        console.log(`Screenshot saved: ${name}.png`);
        return screenshotPath;
    }
    
    async injectKeyPress(key, duration = 100) {
        await this.page.keyboard.down(key);
        await new Promise(resolve => setTimeout(resolve, duration));
        await this.page.keyboard.up(key);
    }
    
    async getGameState() {
        return await this.page.evaluate(() => {
            const score = document.getElementById('score').textContent;
            const lives = document.getElementById('lives').textContent;
            const level = document.getElementById('level').textContent;
            const gameOverVisible = document.getElementById('gameOver').style.display !== 'none';
            
            return {
                score: parseInt(score.match(/\d+/)[0]),
                lives: parseInt(lives.match(/\d+/)[0]),
                level: parseInt(level.match(/\d+/)[0]),
                gameOverVisible
            };
        });
    }
    
    async waitForGameState(expectedState, timeout = 5000) {
        const startTime = Date.now();
        while (Date.now() - startTime < timeout) {
            const state = await this.getGameState();
            if (JSON.stringify(state) === JSON.stringify(expectedState)) {
                return true;
            }
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        return false;
    }
    
    addTestResult(testName, passed, details = '') {
        this.testResults.push({
            test: testName,
            passed,
            details,
            timestamp: new Date().toISOString()
        });
        console.log(`${passed ? '✅' : '❌'} ${testName} ${details ? `- ${details}` : ''}`);
    }
    
    async testGameStart() {
        console.log('\n🎮 Testing Game Start...');
        
        await this.captureScreenshot('01-menu');
        
        await this.injectKeyPress(' ');
        await new Promise(resolve => setTimeout(resolve, 500));
        
        await this.captureScreenshot('02-game-started');
        const state = await this.getGameState();
        
        this.addTestResult(
            'Game Start',
            state.score === 0 && state.lives === 3 && state.level === 1,
            `Score: ${state.score}, Lives: ${state.lives}, Level: ${state.level}`
        );
    }
    
    async testMovement() {
        console.log('\n🕹️ Testing Movement...');
        
        const movements = [
            { key: 'ArrowLeft', name: 'left', duration: 1000 },
            { key: 'ArrowRight', name: 'right', duration: 1000 },
            { key: 'ArrowUp', name: 'up', duration: 500 },
            { key: 'ArrowDown', name: 'down', duration: 500 }
        ];
        
        for (const move of movements) {
            await this.injectKeyPress(move.key);
            await new Promise(resolve => setTimeout(resolve, move.duration));
            await this.captureScreenshot(`03-movement-${move.name}`);
        }
        
        const state = await this.getGameState();
        this.addTestResult(
            'Movement Controls',
            state.score > 0,
            `Score after movement: ${state.score}`
        );
    }
    
    async testPelletCollection() {
        console.log('\n🟡 Testing Pellet Collection...');
        
        const initialState = await this.getGameState();
        
        await this.injectKeyPress('ArrowLeft');
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        const afterState = await this.getGameState();
        await this.captureScreenshot('04-pellet-collection');
        
        this.addTestResult(
            'Pellet Collection',
            afterState.score > initialState.score,
            `Score increased from ${initialState.score} to ${afterState.score}`
        );
    }
    
    async testPortals() {
        console.log('\n🌀 Testing Portals...');
        
        await this.page.evaluate(() => {
            game.pacman.x = 0.5;
            game.pacman.y = 14;
            game.pacman.direction = { x: -1, y: 0 };
        });
        
        await this.captureScreenshot('05-portal-before');
        await new Promise(resolve => setTimeout(resolve, 500));
        await this.captureScreenshot('06-portal-after');
        
        const pacmanX = await this.page.evaluate(() => game.pacman.x);
        this.addTestResult(
            'Portal Functionality',
            pacmanX > 20,
            `Pacman teleported to x: ${pacmanX}`
        );
    }
    
    async testGhostCollision() {
        console.log('\n👻 Testing Ghost Collision...');
        
        const initialLives = (await this.getGameState()).lives;
        
        await this.page.evaluate(() => {
            game.ghosts[0].x = game.pacman.x;
            game.ghosts[0].y = game.pacman.y;
        });
        
        await new Promise(resolve => setTimeout(resolve, 500));
        await this.captureScreenshot('07-ghost-collision');
        
        const afterLives = (await this.getGameState()).lives;
        this.addTestResult(
            'Ghost Collision',
            afterLives === initialLives - 1,
            `Lives decreased from ${initialLives} to ${afterLives}`
        );
    }
    
    async testPowerPellet() {
        console.log('\n⚡ Testing Power Pellet...');
        
        await this.page.evaluate(() => {
            game.pacman.x = 1;
            game.pacman.y = 3;
            game.ghosts[0].x = 3;
            game.ghosts[0].y = 3;
        });
        
        await this.injectKeyPress('ArrowDown');
        await new Promise(resolve => setTimeout(resolve, 100));
        
        const ghostMode = await this.page.evaluate(() => game.ghosts[0].mode);
        await this.captureScreenshot('08-power-pellet');
        
        this.addTestResult(
            'Power Pellet Effect',
            ghostMode === 'frightened',
            `Ghost mode: ${ghostMode}`
        );
    }
    
    async testLevelProgression() {
        console.log('\n📈 Testing Level Progression...');
        
        await this.page.evaluate(() => {
            game.maze.pellets.forEach(p => p.eaten = true);
            game.maze.powerPellets.forEach(p => p.eaten = true);
        });
        
        await new Promise(resolve => setTimeout(resolve, 500));
        await this.captureScreenshot('09-level-complete');
        
        await this.injectKeyPress(' ');
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const state = await this.getGameState();
        await this.captureScreenshot('10-next-level');
        
        this.addTestResult(
            'Level Progression',
            state.level === 2,
            `Advanced to level: ${state.level}`
        );
    }
    
    async testPerformance() {
        console.log('\n⚡ Testing Performance...');
        
        const metrics = await this.page.evaluate(() => {
            return new Promise(resolve => {
                let frameCount = 0;
                let lastTime = performance.now();
                const frameRates = [];
                
                function measureFrame() {
                    frameCount++;
                    const currentTime = performance.now();
                    const deltaTime = currentTime - lastTime;
                    
                    if (deltaTime >= 1000) {
                        frameRates.push(frameCount);
                        frameCount = 0;
                        lastTime = currentTime;
                    }
                    
                    if (frameRates.length < 5) {
                        requestAnimationFrame(measureFrame);
                    } else {
                        const avgFPS = frameRates.reduce((a, b) => a + b) / frameRates.length;
                        resolve({
                            avgFPS,
                            minFPS: Math.min(...frameRates),
                            maxFPS: Math.max(...frameRates)
                        });
                    }
                }
                
                measureFrame();
            });
        });
        
        this.addTestResult(
            'Performance (60 FPS)',
            metrics.avgFPS >= 55,
            `Average FPS: ${metrics.avgFPS.toFixed(2)}, Min: ${metrics.minFPS}, Max: ${metrics.maxFPS}`
        );
    }
    
    async runAllTests() {
        console.log('🚀 Starting Pac-Man Automated Tests...');
        
        try {
            await this.setup();
            
            await this.testGameStart();
            await this.testMovement();
            await this.testPelletCollection();
            await this.testPortals();
            await this.testGhostCollision();
            await this.testPowerPellet();
            await this.testLevelProgression();
            await this.testPerformance();
            
            console.log('\n📊 Test Summary:');
            const passed = this.testResults.filter(r => r.passed).length;
            const total = this.testResults.length;
            console.log(`Passed: ${passed}/${total} (${(passed/total*100).toFixed(1)}%)`);
            
            await fs.writeFile(
                path.join(__dirname, 'test-results.json'),
                JSON.stringify(this.testResults, null, 2)
            );
            
        } catch (error) {
            console.error('Test failed:', error);
        } finally {
            await this.teardown();
        }
    }
}

const tester = new PacmanAutomatedTest();
tester.runAllTests();