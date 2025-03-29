class Timer:
    def __init__(self, duration, callback=None, repeat=False):
        self.duration = duration
        self.callback = callback
        self.repeat = repeat
        self.elapsed = 0
        self.active = False
    
    def start(self):
        self.elapsed = 0
        self.active = True
    
    def update(self, dt):
        if not self.active:
            return
        
        self.elapsed += dt
        if self.elapsed >= self.duration:
            if self.callback:
                self.callback()
            
            if self.repeat:
                self.elapsed = 0
            else:
                self.active = False