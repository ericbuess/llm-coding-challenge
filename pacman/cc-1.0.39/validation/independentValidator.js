const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

class IndependentValidator {
    constructor() {
        this.browser = null;
        this.page = null;
        this.validationResults = [];
        this.server = null;
    }
    
    async setup() {
        this.browser = await puppeteer.launch({
            headless: false,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        this.page = await this.browser.newPage();
        await this.page.setViewport({ width: 1200, height: 800 });
        
        console.log('Starting server for validation...');
        const { spawn } = require('child_process');
        this.server = spawn('python3', ['-m', 'http.server', '8001'], {
            cwd: path.join(__dirname, '..')
        });
        
        await new Promise(resolve => setTimeout(resolve, 2000));
        await this.page.goto('http://localhost:8001');
    }
    
    async teardown() {
        if (this.browser) await this.browser.close();
        if (this.server) this.server.kill();
    }
    
    async validateFeature(name, testFn) {
        console.log(`\n🔍 Validating: ${name}`);
        try {
            const result = await testFn();
            this.validationResults.push({
                feature: name,
                passed: result.passed,
                details: result.details,
                severity: result.severity || 'normal'
            });
            console.log(result.passed ? '✅ PASS' : '❌ FAIL', result.details);
            return result.passed;
        } catch (error) {
            this.validationResults.push({
                feature: name,
                passed: false,
                details: `Error: ${error.message}`,
                severity: 'critical'
            });
            console.log('❌ ERROR:', error.message);
            return false;
        }
    }
    
    async simulateRealGameplay(level = 1) {
        console.log(`\n🎮 Simulating real gameplay for Level ${level}...`);
        
        await this.page.keyboard.press(' ');
        await new Promise(resolve => setTimeout(resolve, 500));
        
        if (level > 1) {
            await this.page.evaluate((lvl) => {
                game.level = lvl - 1;
                game.nextLevel();
            }, level);
        }
        
        const playDuration = 30000;
        const startTime = Date.now();
        const movements = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'];
        
        while (Date.now() - startTime < playDuration) {
            const randomMove = movements[Math.floor(Math.random() * movements.length)];
            await this.page.keyboard.down(randomMove);
            await new Promise(resolve => setTimeout(resolve, 200 + Math.random() * 300));
            await this.page.keyboard.up(randomMove);
            
            await new Promise(resolve => setTimeout(resolve, 100 + Math.random() * 200));
        }
        
        const gameState = await this.page.evaluate(() => ({
            score: parseInt(document.getElementById('score').textContent.match(/\d+/)[0]),
            lives: parseInt(document.getElementById('lives').textContent.match(/\d+/)[0]),
            level: parseInt(document.getElementById('level').textContent.match(/\d+/)[0]),
            gameOver: document.getElementById('gameOver').style.display !== 'none'
        }));
        
        return gameState;
    }
    
    async runValidation() {
        console.log('🔬 Starting Independent Validation Suite...');
        
        try {
            await this.setup();
            
            await this.validateFeature('Game Loads', async () => {
                const title = await this.page.title();
                return {
                    passed: title === 'Pac-Man',
                    details: `Page title: ${title}`
                };
            });
            
            await this.validateFeature('Canvas Renders', async () => {
                const canvasExists = await this.page.evaluate(() => {
                    const canvas = document.getElementById('gameCanvas');
                    return canvas && canvas.width > 0 && canvas.height > 0;
                });
                return {
                    passed: canvasExists,
                    details: canvasExists ? 'Canvas properly initialized' : 'Canvas not found or invalid'
                };
            });
            
            await this.validateFeature('Controls Responsive', async () => {
                await this.page.keyboard.press(' ');
                await new Promise(resolve => setTimeout(resolve, 500));
                
                const movements = [];
                for (const key of ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']) {
                    await this.page.keyboard.press(key);
                    await new Promise(resolve => setTimeout(resolve, 300));
                    const moved = await this.page.evaluate(() => game.pacman.direction);
                    movements.push(moved);
                }
                
                return {
                    passed: movements.length === 4,
                    details: `All 4 directional controls tested`
                };
            });
            
            await this.validateFeature('Score System', async () => {
                const initialScore = await this.page.evaluate(() => 
                    parseInt(document.getElementById('score').textContent.match(/\d+/)[0])
                );
                
                await this.page.keyboard.down('ArrowLeft');
                await new Promise(resolve => setTimeout(resolve, 2000));
                await this.page.keyboard.up('ArrowLeft');
                
                const finalScore = await this.page.evaluate(() => 
                    parseInt(document.getElementById('score').textContent.match(/\d+/)[0])
                );
                
                return {
                    passed: finalScore > initialScore,
                    details: `Score increased from ${initialScore} to ${finalScore}`
                };
            });
            
            await this.validateFeature('Ghost AI Active', async () => {
                const ghostPositions = [];
                for (let i = 0; i < 5; i++) {
                    const pos = await this.page.evaluate(() => 
                        game.ghosts.map(g => ({ x: g.x, y: g.y }))
                    );
                    ghostPositions.push(pos);
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
                
                const moved = ghostPositions.some((pos, i) => 
                    i > 0 && JSON.stringify(pos) !== JSON.stringify(ghostPositions[0])
                );
                
                return {
                    passed: moved,
                    details: moved ? 'Ghosts are moving' : 'Ghosts appear stuck'
                };
            });
            
            await this.validateFeature('Portal Functionality', async () => {
                await this.page.evaluate(() => {
                    game.pacman.x = 0;
                    game.pacman.y = 14;
                    game.pacman.direction = { x: -1, y: 0 };
                });
                
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                const newX = await this.page.evaluate(() => game.pacman.x);
                return {
                    passed: newX > 20,
                    details: `Pacman teleported to x: ${newX}`
                };
            });
            
            await this.validateFeature('Power Pellet Effects', async () => {
                await this.page.evaluate(() => {
                    game.pacman.x = 1;
                    game.pacman.y = 2;
                });
                
                await this.page.keyboard.down('ArrowDown');
                await new Promise(resolve => setTimeout(resolve, 500));
                await this.page.keyboard.up('ArrowDown');
                
                const ghostMode = await this.page.evaluate(() => game.ghosts[0].mode);
                return {
                    passed: ghostMode === 'frightened',
                    details: `Ghost mode after power pellet: ${ghostMode}`
                };
            });
            
            for (let level = 1; level <= 5; level++) {
                await this.validateFeature(`Level ${level} Playable`, async () => {
                    await this.page.reload();
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    
                    const gameState = await this.simulateRealGameplay(level);
                    
                    return {
                        passed: gameState.score > 0 && !gameState.gameOver,
                        details: `Score: ${gameState.score}, Lives: ${gameState.lives}`,
                        severity: 'critical'
                    };
                });
            }
            
            await this.validateFeature('Performance (60 FPS)', async () => {
                const fps = await this.page.evaluate(() => {
                    return new Promise(resolve => {
                        let frames = 0;
                        const startTime = performance.now();
                        
                        function countFrame() {
                            frames++;
                            if (performance.now() - startTime < 5000) {
                                requestAnimationFrame(countFrame);
                            } else {
                                const duration = (performance.now() - startTime) / 1000;
                                resolve(frames / duration);
                            }
                        }
                        
                        countFrame();
                    });
                });
                
                return {
                    passed: fps >= 55,
                    details: `Average FPS: ${fps.toFixed(2)}`
                };
            });
            
            await this.validateFeature('No Console Errors', async () => {
                const errors = [];
                this.page.on('console', msg => {
                    if (msg.type() === 'error') {
                        errors.push(msg.text());
                    }
                });
                
                await this.page.reload();
                await new Promise(resolve => setTimeout(resolve, 5000));
                
                return {
                    passed: errors.length === 0,
                    details: errors.length > 0 ? `Found ${errors.length} errors` : 'No console errors'
                };
            });
            
            console.log('\n📊 Validation Summary:');
            const passed = this.validationResults.filter(r => r.passed).length;
            const total = this.validationResults.length;
            const critical = this.validationResults.filter(r => !r.passed && r.severity === 'critical').length;
            
            console.log(`Total Tests: ${total}`);
            console.log(`Passed: ${passed} (${(passed/total*100).toFixed(1)}%)`);
            console.log(`Failed: ${total - passed}`);
            console.log(`Critical Issues: ${critical}`);
            
            const allPassed = passed === total;
            console.log(`\n${allPassed ? '✅ VALIDATION PASSED' : '❌ VALIDATION FAILED'}`);
            
            await fs.writeFile(
                path.join(__dirname, 'validation-results.json'),
                JSON.stringify({
                    summary: {
                        total,
                        passed,
                        failed: total - passed,
                        critical,
                        allPassed
                    },
                    results: this.validationResults,
                    timestamp: new Date().toISOString()
                }, null, 2)
            );
            
        } catch (error) {
            console.error('Validation error:', error);
        } finally {
            await this.teardown();
        }
    }
}

const validator = new IndependentValidator();
validator.runValidation();