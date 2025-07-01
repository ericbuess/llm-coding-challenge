class InputManager {
    constructor() {
        this.keys = {};
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        window.addEventListener('keydown', (e) => {
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
                e.preventDefault();
                this.keys[e.key] = true;
            }
        });
        
        window.addEventListener('keyup', (e) => {
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
                e.preventDefault();
                this.keys[e.key] = false;
            }
        });
    }
    
    isKeyPressed(key) {
        return this.keys[key] || false;
    }
    
    consumeKey(key) {
        const wasPressed = this.keys[key] || false;
        this.keys[key] = false;
        return wasPressed;
    }
}