class Animation:
    def __init__(self, frames, frame_duration=0.1, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.elapsed_time = 0
        self.finished = False
    
    def update(self, dt):
        """Update animation state"""
        if self.finished:
            return
        
        self.elapsed_time += dt
        
        if self.elapsed_time >= self.frame_duration:
            frames_to_advance = int(self.elapsed_time / self.frame_duration)
            self.elapsed_time %= self.frame_duration
            
            self.current_frame += frames_to_advance
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame %= len(self.frames)
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
    
    def get_current_frame(self):
        """Get the current frame of the animation"""
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reset the animation to the beginning"""
        self.current_frame = 0
        self.elapsed_time = 0
        self.finished = False