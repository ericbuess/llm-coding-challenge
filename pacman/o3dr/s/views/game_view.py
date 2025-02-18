"""Main game view for Pac-Man."""
import arcade
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, Direction, GhostState,
    PELLET_SCORE, POWER_PELLET_SCORE, GHOST_SCORE,
    POWER_PELLET_DURATION, TILE_SIZE, WALL_COLOR,
    TRANSPARENT
)
from player import Pacman
from ghost import Ghost
from utils.asset_manager import assets

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        
        # Game state
        self.paused = False
        self.power_pellet_timer = 0
        
        # Sprite lists
        self.scene = None
        self.player = None
        self.ghosts = None
        self.physics_engine = None
        
        # Create Text objects
        self.score_text = arcade.Text(
            "Score: 0",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            24
        )
        
        self.pause_text = arcade.Text(
            "PAUSED",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            64,
            anchor_x="center",
            anchor_y="center"
        )

    def setup(self):
        """Set up the game."""
        # Create the scene
        self.scene = arcade.Scene()
        
        # Create sprite lists
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Pellets", use_spatial_hash=True)
        self.scene.add_sprite_list("PowerPellets", use_spatial_hash=True)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Ghosts")
        
        # Create a basic maze programmatically
        self._create_basic_maze()
        
        # Set up the player
        player_texture = assets.get_texture("pacman.png")
        self.player = Pacman(player_texture)  # Will create default texture if None
        self.player.center_x = TILE_SIZE * 1.5
        self.player.center_y = TILE_SIZE * 1.5
        self.scene.add_sprite("Player", self.player)
        
        # Create ghost sprites
        self.ghosts = arcade.SpriteList()
        ghost_types = ["blinky", "pinky", "inky", "clyde"]
        ghost_positions = [
            (SCREEN_WIDTH - TILE_SIZE * 1.5, SCREEN_HEIGHT - TILE_SIZE * 1.5),
            (TILE_SIZE * 1.5, SCREEN_HEIGHT - TILE_SIZE * 1.5),
            (SCREEN_WIDTH - TILE_SIZE * 1.5, TILE_SIZE * 1.5),
            (TILE_SIZE * 1.5, SCREEN_HEIGHT - TILE_SIZE * 3.5)
        ]
        
        for ghost_type, pos in zip(ghost_types, ghost_positions):
            ghost_texture = assets.get_texture(f"{ghost_type}.png")
            ghost = Ghost(ghost_texture, ghost_type)  # Will create default texture if None
            ghost.position = pos
            ghost.spawn_point = pos
            self.ghosts.append(ghost)
            self.scene.add_sprite("Ghosts", ghost)
        
        # Add pellets in open spaces
        self._add_pellets()
        
        # Set up the physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.scene.get_sprite_list("Walls")
        )

    def _create_basic_maze(self):
        """Create a basic maze layout."""
        # Create outer walls
        for x in range(0, SCREEN_WIDTH + TILE_SIZE, TILE_SIZE):
            self._create_wall(x, 0)  # Bottom wall
            self._create_wall(x, SCREEN_HEIGHT - TILE_SIZE)  # Top wall
        
        for y in range(0, SCREEN_HEIGHT + TILE_SIZE, TILE_SIZE):
            self._create_wall(0, y)  # Left wall
            self._create_wall(SCREEN_WIDTH - TILE_SIZE, y)  # Right wall
        
        # Add some inner walls for a basic maze
        for x in range(TILE_SIZE * 3, SCREEN_WIDTH - TILE_SIZE * 3, TILE_SIZE * 3):
            for y in range(TILE_SIZE * 3, SCREEN_HEIGHT - TILE_SIZE * 3, TILE_SIZE * 3):
                self._create_wall(x, y)

    def _create_wall(self, x: float, y: float):
        """Create a wall sprite at the specified position."""
        wall = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, WALL_COLOR)
        wall.center_x = x
        wall.center_y = y
        self.scene.add_sprite("Walls", wall)

    def _add_pellets(self):
        """Add pellets to open spaces in the maze."""
        pellet_spacing = TILE_SIZE * 1.5
        
        for x in range(int(TILE_SIZE * 1.5), int(SCREEN_WIDTH - TILE_SIZE), int(pellet_spacing)):
            for y in range(int(TILE_SIZE * 1.5), int(SCREEN_HEIGHT - TILE_SIZE), int(pellet_spacing)):
                # Check if space is empty (no walls)
                temp_sprite = arcade.SpriteSolidColor(4, 4, TRANSPARENT)
                temp_sprite.center_x = x
                temp_sprite.center_y = y
                
                if not arcade.check_for_collision_with_list(temp_sprite, self.scene.get_sprite_list("Walls")):
                    pellet = arcade.SpriteSolidColor(4, 4, arcade.color.WHITE)
                    pellet.center_x = x
                    pellet.center_y = y
                    self.scene.add_sprite("Pellets", pellet)
                    
                    # Add some power pellets in corners
                    if (x < TILE_SIZE * 3 and y < TILE_SIZE * 3) or \
                       (x < TILE_SIZE * 3 and y > SCREEN_HEIGHT - TILE_SIZE * 3) or \
                       (x > SCREEN_WIDTH - TILE_SIZE * 3 and y < TILE_SIZE * 3) or \
                       (x > SCREEN_WIDTH - TILE_SIZE * 3 and y > SCREEN_HEIGHT - TILE_SIZE * 3):
                        power_pellet = arcade.SpriteSolidColor(8, 8, arcade.color.WHITE)
                        power_pellet.center_x = x
                        power_pellet.center_y = y
                        self.scene.add_sprite("PowerPellets", power_pellet)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        
        # Draw all game elements
        self.scene.draw()
        
        # Update and draw score
        self.score_text.text = f"Score: {self.player.score}"
        self.score_text.draw()
        
        # Draw the lives
        pacman_texture = assets.get_texture("pacman.png")
        for i in range(self.player.lives):
            if pacman_texture:
                arcade.draw_texture_rectangle(
                    30 + i * 30,
                    SCREEN_HEIGHT - 60,
                    20,
                    20,
                    pacman_texture
                )
            else:
                arcade.draw_circle_filled(
                    30 + i * 30,
                    SCREEN_HEIGHT - 60,
                    10,
                    arcade.color.YELLOW
                )
        
        # Draw pause text if paused
        if self.paused:
            self.pause_text.draw()

    def on_update(self, delta_time: float):
        """Update game state."""
        if self.paused:
            return
            
        # Update player movement
        self.player.update(delta_time, self.scene)
        
        # Update physics engine after moving the player to handle collisions
        self.physics_engine.update()
        
        # Update power pellet timer
        if self.power_pellet_timer > 0:
            self.power_pellet_timer -= delta_time
            if self.power_pellet_timer <= 0:
                for ghost in self.ghosts:
                    ghost.exit_frightened_mode()
        
        # Check for pellet collisions
        pellets_hit = arcade.check_for_collision_with_list(
            self.player,
            self.scene.get_sprite_list("Pellets")
        )
        for pellet in pellets_hit:
            pellet.remove_from_sprite_lists()
            self.player.score += PELLET_SCORE
        
        # Check for power pellet collisions
        power_pellets_hit = arcade.check_for_collision_with_list(
            self.player,
            self.scene.get_sprite_list("PowerPellets")
        )
        for power_pellet in power_pellets_hit:
            power_pellet.remove_from_sprite_lists()
            self.player.score += POWER_PELLET_SCORE
            self.power_pellet_timer = POWER_PELLET_DURATION
            for ghost in self.ghosts:
                ghost.enter_frightened_mode()
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(
                delta_time,
                self.scene.get_sprite_list("Walls"),
                self.player
            )
            
            # Check for collisions with ghosts
            if arcade.check_for_collision(self.player, ghost):
                if ghost.state == GhostState.FRIGHTENED:
                    ghost.reset_position()
                    self.player.score += GHOST_SCORE
                else:
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        from views.gameover_view import GameOverView
                        game_over = GameOverView(self.player.score)
                        self.window.show_view(game_over)
                    else:
                        self._reset_level()
        
        # Check win condition
        if len(self.scene.get_sprite_list("Pellets")) == 0:
            from views.gameover_view import GameOverView
            game_over = GameOverView(self.player.score, won=True)
            self.window.show_view(game_over)

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.P:
            self.paused = not self.paused
        elif key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            self.window.show_view(MenuView())
        elif not self.paused:
            if key in (arcade.key.UP, arcade.key.W):
                self.player.set_intended_direction(Direction.UP)
            elif key in (arcade.key.DOWN, arcade.key.S):
                self.player.set_intended_direction(Direction.DOWN)
            elif key in (arcade.key.LEFT, arcade.key.A):
                self.player.set_intended_direction(Direction.LEFT)
            elif key in (arcade.key.RIGHT, arcade.key.D):
                self.player.set_intended_direction(Direction.RIGHT)

    def _reset_level(self):
        """Reset player and ghost positions after losing a life."""
        self.player.reset_position(400, 100)  # Example starting position
        for ghost in self.ghosts:
            ghost.reset_position() 