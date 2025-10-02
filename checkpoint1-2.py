import pygame
import numpy as np
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
LIME = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 255)
ORANGE = (255, 165, 0)

# Game settings
MAP_SIZE = 100
NUM_TRASH = 15
WIN_SCORE = 1000
SHIP_SIZE = 40

OBSTACLE_TYPES = {
    "meteor": {"size": 20, "speed": 5, "color": RED, "damage": 20},
    "satellite": {"size": 50, "speed": 2, "color": GRAY, "damage": 30}
}

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TrashSpace")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 20)
        
        # Game state
        self.points = 0
        self.upgrades = {"armor": 0, "maneuver": 0, "laser": 0}
        self.scene = "menu"
        
        # Flight mission state
        self.reset_flight()
        
        # Trash mission state
        self.reset_trash()
        
    def reset_flight(self):
        self.ship_x = SCREEN_WIDTH // 2 - SHIP_SIZE // 2
        self.ship_y = SCREEN_HEIGHT - 100
        self.obstacles = []
        self.hp = 100 + self.upgrades["armor"] * 20
        self.max_hp = 100 + self.upgrades["armor"] * 20
        self.score_flight = 0
        self.speed_factor = 1
        self.game_won = False
        self.hit_obstacles = set()
        self.frame_count = 0
        
    def reset_trash(self):
        self.trash = np.random.randint(-MAP_SIZE, MAP_SIZE, (NUM_TRASH, 2))
        self.score_trash = 0
        self.shots_fired = 0
        self.last_target = None
        self.mission_complete = False
        self.input_text = ""
        self.laser_animation = []
        
    def draw_text(self, text, x, y, font=None, color=WHITE, center=False):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        if center:
            rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, rect)
        else:
            self.screen.blit(text_surface, (x, y))
    
    def draw_button(self, text, x, y, width, height, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        is_hover = x < mouse[0] < x + width and y < mouse[1] < y + height
        
        button_color = hover_color if is_hover else color
        pygame.draw.rect(self.screen, button_color, (x, y, width, height))
        pygame.draw.rect(self.screen, WHITE, (x, y, width, height), 2)
        
        self.draw_text(text, x + width // 2, y + height // 2, self.small_font, WHITE, center=True)
        
        if is_hover and click[0] == 1 and action:
            pygame.time.wait(100)
            return action()
        return None
    
    def menu_scene(self):
        self.screen.fill(BLACK)
        
        # Title
        self.draw_text("TRASHSPACE", SCREEN_WIDTH // 2, 80, self.font, CYAN, center=True)
        self.draw_text(f"Points: {self.points}", SCREEN_WIDTH // 2, 130, self.small_font, YELLOW, center=True)
        
        # Instructions
        y = 200
        self.draw_text("MISSIONS:", 100, y, self.small_font, LIME)
        y += 40
        self.draw_text("Flight to Mars - Avoid obstacles", 120, y, self.tiny_font, WHITE)
        y += 30
        self.draw_text("Trash Collection - Use coordinates to shoot laser", 120, y, self.tiny_font, WHITE)
        y += 30
        self.draw_text("Upgrade - Improve your ship", 120, y, self.tiny_font, WHITE)
        
        # Upgrades display
        y += 60
        self.draw_text("CURRENT UPGRADES:", 100, y, self.small_font, PURPLE)
        y += 35
        self.draw_text(f"Armor: {self.upgrades['armor']} | Maneuver: {self.upgrades['maneuver']} | Laser: {self.upgrades['laser']}", 
                      120, y, self.tiny_font, WHITE)
        
        # Buttons
        if self.draw_button("FLIGHT MISSION", 250, 400, 300, 50, BLUE, CYAN, lambda: "flight"):
            self.scene = "flight"
            self.reset_flight()
        
        if self.draw_button("TRASH COLLECTION", 250, 460, 300, 50, BLUE, CYAN, lambda: "trash"):
            self.scene = "trash"
            self.reset_trash()
        
        if self.draw_button("UPGRADE", 250, 520, 300, 50, PURPLE, (255, 0, 255), lambda: "upgrade"):
            self.scene = "upgrade"
    
    def flight_scene(self):
        self.screen.fill(BLACK)
        
        # Game logic
        self.frame_count += 1
        
        # Spawn obstacles
        if random.random() < 0.02 and not self.game_won:
            o_type = random.choice(list(OBSTACLE_TYPES.keys()))
            spec = OBSTACLE_TYPES[o_type]
            new_obstacle = {
                "x": random.randint(0, SCREEN_WIDTH - spec["size"]),
                "y": -spec["size"],
                "type": o_type,
                "id": random.random()
            }
            self.obstacles.append(new_obstacle)
        
        # Move obstacles
        new_obs = []
        for obs in self.obstacles:
            spec = OBSTACLE_TYPES[obs["type"]]
            obs["y"] += spec["speed"] * self.speed_factor
            if obs["y"] < SCREEN_HEIGHT:
                new_obs.append(obs)
            else:
                self.hit_obstacles.discard(obs["id"])
        self.obstacles = new_obs
        
        # Collision detection
        for obs in self.obstacles:
            if obs["id"] not in self.hit_obstacles:
                spec = OBSTACLE_TYPES[obs["type"]]
                ship_center_x = self.ship_x + SHIP_SIZE // 2
                ship_center_y = self.ship_y + SHIP_SIZE // 2
                obs_center_x = obs["x"] + spec["size"] // 2
                obs_center_y = obs["y"] + spec["size"] // 2
                
                if (abs(ship_center_x - obs_center_x) < (SHIP_SIZE + spec["size"]) // 2 and
                    abs(ship_center_y - obs_center_y) < (SHIP_SIZE + spec["size"]) // 2):
                    self.hp -= spec["damage"]
                    self.hit_obstacles.add(obs["id"])
        
        # Update score
        if not self.game_won and self.hp > 0:
            self.score_flight += 1
        
        # Check win/lose
        if self.score_flight >= WIN_SCORE and not self.game_won:
            self.game_won = True
            reward = 50 + self.hp // 2
            self.points += reward
        
        if self.hp <= 0 and not self.game_won:
            reward = self.score_flight // 10
            self.points += reward
        
        # Draw obstacles
        for obs in self.obstacles:
            spec = OBSTACLE_TYPES[obs["type"]]
            pygame.draw.ellipse(self.screen, spec["color"], 
                              (obs["x"], obs["y"], spec["size"], spec["size"]))
            pygame.draw.ellipse(self.screen, WHITE, 
                              (obs["x"], obs["y"], spec["size"], spec["size"]), 2)
        
        # Draw ship
        pygame.draw.rect(self.screen, BLUE, 
                        (self.ship_x, self.ship_y, SHIP_SIZE, SHIP_SIZE))
        pygame.draw.rect(self.screen, CYAN, 
                        (self.ship_x, self.ship_y, SHIP_SIZE, SHIP_SIZE), 3)
        
        # Draw stats
        self.draw_text(f"HP: {max(0, self.hp)}/{self.max_hp}", 10, 10, self.small_font, RED if self.hp < 30 else WHITE)
        self.draw_text(f"Score: {self.score_flight}/{WIN_SCORE}", SCREEN_WIDTH - 250, 10, self.small_font, LIME)
        self.draw_text(f"Speed: {self.speed_factor}x", SCREEN_WIDTH // 2 - 60, 10, self.small_font, YELLOW)
        
        # Controls info
        self.draw_text("Arrow Keys: Move | Up: Boost | Down: Slow | R: Reset | ESC: Menu", 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20, self.tiny_font, WHITE, center=True)
        
        # Win/Lose message
        if self.game_won:
            self.draw_text("VICTORY!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                          self.font, LIME, center=True)
            reward = 50 + max(0, self.hp) // 2
            self.draw_text(f"Earned {reward} points!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, 
                          self.small_font, YELLOW, center=True)
        elif self.hp <= 0:
            self.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                          self.font, RED, center=True)
            reward = self.score_flight // 10
            self.draw_text(f"Earned {reward} points", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, 
                          self.small_font, YELLOW, center=True)
        
        # Handle input
        keys = pygame.key.get_pressed()
        movement = 5 + self.upgrades["maneuver"]
        if keys[pygame.K_LEFT]:
            self.ship_x = max(0, self.ship_x - movement)
        if keys[pygame.K_RIGHT]:
            self.ship_x = min(SCREEN_WIDTH - SHIP_SIZE, self.ship_x + movement)
        if keys[pygame.K_UP]:
            self.speed_factor = 2
        if keys[pygame.K_DOWN]:
            self.speed_factor = 0.5
    
    def trash_scene(self):
        self.screen.fill(BLACK)
        
        # Draw radar
        radar_x, radar_y = 50, 50
        radar_size = 400
        scale = radar_size / (2 * MAP_SIZE)
        
        # Radar background
        pygame.draw.rect(self.screen, (20, 20, 20), (radar_x, radar_y, radar_size, radar_size))
        
        # Grid
        for i in range(-MAP_SIZE, MAP_SIZE + 1, 20):
            # Vertical lines
            x = radar_x + (i + MAP_SIZE) * scale
            pygame.draw.line(self.screen, (50, 50, 50), (x, radar_y), (x, radar_y + radar_size), 1)
            # Horizontal lines
            y = radar_y + (MAP_SIZE - i) * scale
            pygame.draw.line(self.screen, (50, 50, 50), (radar_x, y), (radar_x + radar_size, y), 1)
        
        # Axes
        center_x = radar_x + radar_size // 2
        center_y = radar_y + radar_size // 2
        pygame.draw.line(self.screen, WHITE, (center_x, radar_y), (center_x, radar_y + radar_size), 2)
        pygame.draw.line(self.screen, WHITE, (radar_x, center_y), (radar_x + radar_size, center_y), 2)
        
        # Draw coordinate labels
        for i in range(-MAP_SIZE, MAP_SIZE + 1, 10):
            if i == 0:
                continue
            # X-axis labels
            x_pos = center_x + i * scale
            if radar_x < x_pos < radar_x + radar_size:
                self.draw_text(str(i), x_pos, radar_y + radar_size + 5, self.tiny_font, GRAY, center=True)
            
            # Y-axis labels
            y_pos = center_y - i * scale
            if radar_y < y_pos < radar_y + radar_size:
                self.draw_text(str(i), radar_x - 15, y_pos, self.tiny_font, GRAY, center=True)
        
        # Origin label
        self.draw_text("0", center_x - 10, center_y + 5, self.tiny_font, WHITE)
        
        # Ship at origin
        pygame.draw.polygon(self.screen, CYAN, [
            (center_x, center_y - 10),
            (center_x - 8, center_y + 10),
            (center_x + 8, center_y + 10)
        ])
        
        # Draw trash
        for tx, ty in self.trash:
            screen_x = center_x + tx * scale
            screen_y = center_y - ty * scale
            pygame.draw.circle(self.screen, LIME, (int(screen_x), int(screen_y)), 6)
            pygame.draw.circle(self.screen, WHITE, (int(screen_x), int(screen_y)), 6, 1)
        
        # Draw laser animations
        new_animations = []
        for anim in self.laser_animation:
            if anim["timer"] > 0:
                tx, ty = anim["pos"]
                screen_x = center_x + tx * scale
                screen_y = center_y - ty * scale
                
                # Laser line
                pygame.draw.line(self.screen, RED, (center_x, center_y), 
                               (screen_x, screen_y), 2)
                
                # Blast radius
                laser_radius = (5 + self.upgrades["laser"] * 2) * scale
                pygame.draw.circle(self.screen, RED, (int(screen_x), int(screen_y)), 
                                 int(laser_radius), 2)
                
                anim["timer"] -= 1
                new_animations.append(anim)
        self.laser_animation = new_animations
        
        # Stats panel
        panel_x = 500
        self.draw_text("STATISTICS", panel_x, 50, self.small_font, YELLOW)
        self.draw_text(f"Trash Remaining: {len(self.trash)}", panel_x, 90, self.tiny_font, WHITE)
        self.draw_text(f"Score: {self.score_trash}", panel_x, 120, self.tiny_font, WHITE)
        self.draw_text(f"Shots Fired: {self.shots_fired}", panel_x, 150, self.tiny_font, WHITE)
        laser_r = 5 + self.upgrades["laser"] * 2
        self.draw_text(f"Laser Radius: {laser_r}", panel_x, 180, self.tiny_font, WHITE)
        
        # Hint
        if len(self.trash) > 0:
            nearest = self.trash[0]
            self.draw_text(f"Hint:", panel_x, 220, self.tiny_font, LIME)
            self.draw_text(f"({nearest[0]}, {nearest[1]})", panel_x, 245, self.tiny_font, LIME)
        
        # Input box
        self.draw_text("ENTER COORDINATES (X Y):", panel_x, 290, self.tiny_font, CYAN)
        pygame.draw.rect(self.screen, WHITE, (panel_x, 320, 250, 40), 2)
        self.draw_text(self.input_text, panel_x + 10, 330, self.small_font, WHITE)
        
        # Fire button
        if self.draw_button("FIRE", panel_x, 380, 120, 40, RED, ORANGE, lambda: "fire"):
            self.fire_laser()
        
        # Reset button
        if self.draw_button("RESET", panel_x + 130, 380, 120, 40, PURPLE, (255, 0, 255), lambda: "reset"):
            self.reset_trash()
        
        # Back button
        self.draw_text("ESC: Back to Menu", panel_x, 450, self.tiny_font, WHITE)
        
        # Mission complete
        if self.mission_complete:
            self.draw_text("MISSION COMPLETE!", SCREEN_WIDTH // 2, 500, 
                          self.font, LIME, center=True)
    
    def fire_laser(self):
        try:
            coords = self.input_text.replace(",", " ").split()
            x_input, y_input = int(coords[0]), int(coords[1])
            
            self.shots_fired += 1
            self.laser_animation.append({"pos": (x_input, y_input), "timer": 20})
            
            laser_radius = 5 + self.upgrades["laser"] * 2
            hit_indices = []
            
            for i, (tx, ty) in enumerate(self.trash):
                dist = math.sqrt((x_input - tx) ** 2 + (y_input - ty) ** 2)
                if dist <= laser_radius:
                    hit_indices.append(i)
            
            if hit_indices:
                self.score_trash += len(hit_indices) * 5
                self.trash = np.delete(self.trash, hit_indices, axis=0)
            
            if len(self.trash) == 0 and not self.mission_complete:
                self.mission_complete = True
                accuracy = (self.score_trash // 5) / self.shots_fired if self.shots_fired > 0 else 0
                bonus = int(50 * accuracy)
                total_reward = self.score_trash + bonus
                self.points += total_reward
            
            self.input_text = ""
        except:
            pass
    
    def upgrade_scene(self):
        self.screen.fill(BLACK)
        
        self.draw_text("UPGRADE STATION", SCREEN_WIDTH // 2, 50, self.font, PURPLE, center=True)
        self.draw_text(f"Points: {self.points}", SCREEN_WIDTH // 2, 100, self.small_font, YELLOW, center=True)
        
        y = 180
        
        # Armor
        self.draw_text(f"ARMOR - Level {self.upgrades['armor']}", 100, y, self.small_font, WHITE)
        self.draw_text(f"Effect: +{self.upgrades['armor'] * 20} Max HP", 100, y + 30, self.tiny_font, CYAN)
        cost = 20 + self.upgrades["armor"] * 5
        if self.draw_button(f"Upgrade ({cost}pts)", 500, y, 200, 40, BLUE, CYAN, lambda: "armor"):
            if self.points >= cost:
                self.upgrades["armor"] += 1
                self.points -= cost
        
        y += 100
        
        # Maneuver
        self.draw_text(f"MANEUVER - Level {self.upgrades['maneuver']}", 100, y, self.small_font, WHITE)
        self.draw_text(f"Effect: +{self.upgrades['maneuver'] * 3} Movement Speed", 100, y + 30, self.tiny_font, CYAN)
        cost = 15 + self.upgrades["maneuver"] * 5
        if self.draw_button(f"Upgrade ({cost}pts)", 500, y, 200, 40, BLUE, CYAN, lambda: "maneuver"):
            if self.points >= cost:
                self.upgrades["maneuver"] += 1
                self.points -= cost
        
        y += 100
        
        # Laser
        self.draw_text(f"LASER - Level {self.upgrades['laser']}", 100, y, self.small_font, WHITE)
        self.draw_text(f"Effect: +{self.upgrades['laser'] * 2} Laser Radius", 100, y + 30, self.tiny_font, CYAN)
        cost = 10 + self.upgrades["laser"] * 5
        if self.draw_button(f"Upgrade ({cost}pts)", 500, y, 200, 40, BLUE, CYAN, lambda: "laser"):
            if self.points >= cost:
                self.upgrades["laser"] += 1
                self.points -= cost
        
        # Back button
        if self.draw_button("BACK TO MENU", 300, 520, 200, 50, PURPLE, (255, 0, 255), lambda: "menu"):
            self.scene = "menu"
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.scene = "menu"
                    
                    if self.scene == "flight" and event.key == pygame.K_r:
                        self.reset_flight()
                    
                    if self.scene == "trash":
                        if event.key == pygame.K_RETURN:
                            self.fire_laser()
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        elif event.unicode.isprintable():
                            self.input_text += event.unicode
            
            if self.scene == "menu":
                self.menu_scene()
            elif self.scene == "flight":
                self.flight_scene()
            elif self.scene == "trash":
                self.trash_scene()
            elif self.scene == "upgrade":
                self.upgrade_scene()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()