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
PINK = (255, 105, 180)
GREEN = (0, 200, 100)
DARK_GREEN = (0, 100, 50)
BROWN = (139, 69, 19)

# Game settings
MAP_SIZE = 100
NUM_TRASH = 15
WIN_SCORE = 1000
SHIP_SIZE = 40

OBSTACLE_TYPES = {
    "meteor": {"size": 20, "speed": 5, "color": RED, "damage": 20},
    "satellite": {"size": 50, "speed": 2, "color": GRAY, "damage": 30}
}

# Trash Database with Rarity and Usefulness
TRASH_DATABASE = {
    "Rocket/Rover Parts": [
        {"name": "Broken solar panel", "rarity": 65, "usefulness": 85, "color": BLUE},
        {"name": "Broken robotic arm", "rarity": 70, "usefulness": 80, "color": CYAN},
        {"name": "Dented rover frame", "rarity": 60, "usefulness": 75, "color": GRAY},
        {"name": "Burnt circuit board", "rarity": 55, "usefulness": 70, "color": GREEN},
        {"name": "Old battery casing", "rarity": 40, "usefulness": 65, "color": YELLOW},
        {"name": "Broken antenna", "rarity": 75, "usefulness": 90, "color": ORANGE},
        {"name": "Damaged rover wheel", "rarity": 50, "usefulness": 60, "color": BLACK},
        {"name": "Rusted fuel pipe", "rarity": 35, "usefulness": 55, "color": BROWN},
        {"name": "Cracked control panel", "rarity": 45, "usefulness": 65, "color": PURPLE},
        {"name": "Old rover camera", "rarity": 60, "usefulness": 70, "color": LIME},
        {"name": "Rocket thruster shell", "rarity": 85, "usefulness": 95, "color": RED},
        {"name": "Burnt heat shield", "rarity": 50, "usefulness": 55, "color": ORANGE},
        {"name": "Severed wiring", "rarity": 30, "usefulness": 50, "color": YELLOW},
        {"name": "Signal control box", "rarity": 55, "usefulness": 70, "color": BLUE},
        {"name": "Empty oxygen tank", "rarity": 40, "usefulness": 60, "color": WHITE},
        {"name": "Outdated computer chip", "rarity": 70, "usefulness": 85, "color": CYAN},
    ],
    "Metal/Meteorite": [
        {"name": "Titanium alloy fragment", "rarity": 65, "usefulness": 90, "color": GRAY},
        {"name": "Rocket bolt base", "rarity": 20, "usefulness": 40, "color": (100, 100, 100)},
        {"name": "Aluminum bar", "rarity": 25, "usefulness": 45, "color": (200, 200, 200)},
        {"name": "Rusty steel shell", "rarity": 30, "usefulness": 50, "color": BROWN},
        {"name": "Hollow metal plate", "rarity": 35, "usefulness": 55, "color": GRAY},
        {"name": "Copper alloy core", "rarity": 55, "usefulness": 70, "color": ORANGE},
        {"name": "Broken bolt", "rarity": 20, "usefulness": 35, "color": (80, 80, 80)},
        {"name": "Titanium screw", "rarity": 40, "usefulness": 60, "color": (150, 150, 150)},
        {"name": "Iron meteorite fragment", "rarity": 70, "usefulness": 85, "color": (60, 60, 60)},
        {"name": "Silicon meteorite", "rarity": 65, "usefulness": 75, "color": (100, 100, 120)},
        {"name": "Nickel ore", "rarity": 80, "usefulness": 95, "color": (180, 180, 160)},
        {"name": "Magnesium compound", "rarity": 50, "usefulness": 70, "color": (220, 220, 220)},
        {"name": "Carbon alloy shell", "rarity": 75, "usefulness": 85, "color": BLACK},
        {"name": "Aluminum-lithium alloy", "rarity": 85, "usefulness": 95, "color": (230, 230, 230)},
        {"name": "Green rusted metal", "rarity": 45, "usefulness": 60, "color": (0, 150, 100)},
        {"name": "Bent metal frame", "rarity": 30, "usefulness": 50, "color": GRAY},
        {"name": "Ferrite compound core", "rarity": 70, "usefulness": 80, "color": (120, 100, 100)},
    ],
    "Biological/Waste": [
        {"name": "Leaking CO2 tank", "rarity": 40, "usefulness": 65, "color": (200, 255, 200)},
        {"name": "Methane from system", "rarity": 60, "usefulness": 80, "color": (255, 255, 200)},
        {"name": "Empty food package", "rarity": 15, "usefulness": 25, "color": (255, 200, 150)},
        {"name": "Frozen urine bag", "rarity": 30, "usefulness": 70, "color": (255, 255, 150)},
        {"name": "Dirty rubber glove", "rarity": 25, "usefulness": 40, "color": (200, 200, 150)},
        {"name": "Old sweat towel", "rarity": 20, "usefulness": 35, "color": (150, 150, 100)},
        {"name": "Rotting vegetables", "rarity": 25, "usefulness": 55, "color": GREEN},
        {"name": "Household wastewater", "rarity": 35, "usefulness": 65, "color": (150, 150, 255)},
        {"name": "Medical plastic wrap", "rarity": 40, "usefulness": 50, "color": (200, 200, 255)},
        {"name": "Plastic bag fragment", "rarity": 20, "usefulness": 30, "color": (220, 220, 220)},
        {"name": "Used toilet paper", "rarity": 15, "usefulness": 25, "color": (240, 240, 200)},
        {"name": "Empty plastic bottle", "rarity": 20, "usefulness": 40, "color": (200, 230, 255)},
        {"name": "Moldy leftover food", "rarity": 25, "usefulness": 45, "color": DARK_GREEN},
        {"name": "NO2 emissions", "rarity": 65, "usefulness": 85, "color": (255, 150, 100)},
        {"name": "Expired fertilizer", "rarity": 30, "usefulness": 60, "color": BROWN},
        {"name": "Biodegradable plastic", "rarity": 25, "usefulness": 50, "color": (180, 255, 180)},
        {"name": "Microbial waste", "rarity": 80, "usefulness": 95, "color": (100, 255, 100)},
    ]
}

# Foreign object colors for variety
FOREIGN_COLORS = [PINK, PURPLE, ORANGE, CYAN, YELLOW, LIME]

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
        
        # Foreign object tracking (Rule 1)
        self.foreign_objects_count = 0  # Number of triangles to spawn in next flight
        self.collected_trash_items = []  # Trash collected in last garbage collection
        
        # Difficulty tracking (Rule 4)
        self.perfect_runs = 0  # Consecutive perfect runs
        self.base_ship_speed = 1.0  # Base speed multiplier
        self.last_flight_crashed = False  # Track if last flight crashed
        
        # Flight mission state
        self.reset_flight()
        
        # Trash mission state
        self.reset_trash()
        
        # Recycle mission state
        self.recycle_items = []
        self.bins = {
            "Rocket/Rover Parts": {"rect": pygame.Rect(50, 450, 200, 100), "color": BLUE},
            "Metal/Meteorite": {"rect": pygame.Rect(300, 450, 200, 100), "color": GRAY},
            "Biological/Waste": {"rect": pygame.Rect(550, 450, 200, 100), "color": GREEN}
        }
        self.dragging_item = None
        self.drag_offset = (0, 0)
        self.recycle_score = 0
        self.combo_count = 0
        self.last_three_usefulness = []
        
    def reset_flight(self):
        self.ship_x = SCREEN_WIDTH // 2 - SHIP_SIZE // 2
        self.ship_y = SCREEN_HEIGHT - 100
        self.obstacles = []
        self.foreign_objects = []  # Triangular foreign objects
        self.hp = 100 + self.upgrades["armor"] * 20
        self.max_hp = 100 + self.upgrades["armor"] * 20
        self.score_flight = 0
        self.speed_factor = self.base_ship_speed
        self.game_won = False
        self.hit_obstacles = set()
        self.hit_foreign = set()
        self.frame_count = 0
        
        # Spawn foreign objects based on count (Rule 1)
        for i in range(self.foreign_objects_count):
            self.spawn_foreign_object(i)
        
    def spawn_foreign_object(self, index):
        """Spawn a triangular foreign object that moves diagonally"""
        color_index = index % len(FOREIGN_COLORS)
        direction = random.choice([-1, 1])  # Left or right diagonal
        foreign_obj = {
            "x": random.randint(50, SCREEN_WIDTH - 50),
            "y": -30,
            "dx": direction * 2,  # Diagonal movement X
            "dy": 3,  # Diagonal movement Y
            "size": 25,
            "color": FOREIGN_COLORS[color_index],
            "id": random.random()
        }
        self.foreign_objects.append(foreign_obj)
        
    def reset_trash(self):
        # Rule 2: Number of trash = base + foreign objects count
        total_trash = NUM_TRASH + self.foreign_objects_count
        self.trash = np.random.randint(-MAP_SIZE, MAP_SIZE, (total_trash, 2))
        self.score_trash = 0
        self.shots_fired = 0
        self.last_target = None
        self.mission_complete = False
        self.input_text = ""
        self.laser_animation = []
        self.collected_trash_items = []  # Reset collected items
        
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
        self.draw_text("TRASHSPACE", SCREEN_WIDTH // 2, 60, self.font, CYAN, center=True)
        self.draw_text(f"Points: {self.points}", SCREEN_WIDTH // 2, 100, self.small_font, YELLOW, center=True)
        
        # Difficulty info (Rule 4)
        y = 140
        self.draw_text(f"Perfect Runs: {self.perfect_runs} | Speed: {self.base_ship_speed:.1f}x | Foreign Objects: {self.foreign_objects_count}", 
                      SCREEN_WIDTH // 2, y, self.tiny_font, ORANGE, center=True)
        
        # Instructions
        y = 180
        self.draw_text("MISSIONS:", 100, y, self.small_font, LIME)
        y += 35
        self.draw_text("Flight to Mars - Avoid obstacles and triangles", 120, y, self.tiny_font, WHITE)
        y += 25
        self.draw_text("Trash Collection - Use coordinates to shoot laser", 120, y, self.tiny_font, WHITE)
        y += 25
        self.draw_text("Recycle Trash - Sort collected items into bins", 120, y, self.tiny_font, WHITE)
        y += 25
        self.draw_text("Upgrade - Improve your ship", 120, y, self.tiny_font, WHITE)
        
        # Upgrades display
        y += 40
        self.draw_text("CURRENT UPGRADES:", 100, y, self.small_font, PURPLE)
        y += 30
        self.draw_text(f"Armor: {self.upgrades['armor']} | Maneuver: {self.upgrades['maneuver']} | Laser: {self.upgrades['laser']}", 
                      120, y, self.tiny_font, WHITE)
        
        # Buttons
        if self.draw_button("FLIGHT MISSION", 250, 370, 300, 45, BLUE, CYAN, lambda: "flight"):
            self.scene = "flight"
            self.reset_flight()
        
        if self.draw_button("TRASH COLLECTION", 250, 425, 300, 45, BLUE, CYAN, lambda: "trash"):
            self.scene = "trash"
            self.reset_trash()
        
        # Recycle button only unlocked after collecting trash
        button_color = GREEN if len(self.collected_trash_items) > 0 else DARK_GREEN
        hover_color = LIME if len(self.collected_trash_items) > 0 else GREEN
        if self.draw_button(f"RECYCLE TRASH ({len(self.collected_trash_items)})", 250, 480, 300, 45, button_color, hover_color, lambda: "recycle"):
            if len(self.collected_trash_items) > 0:
                self.scene = "recycle"
                self.setup_recycle_mission()
        
        if self.draw_button("UPGRADE", 250, 535, 300, 45, PURPLE, (255, 0, 255), lambda: "upgrade"):
            self.scene = "upgrade"
    
    def flight_scene(self):
        self.screen.fill(BLACK)
        
        # Game logic
        self.frame_count += 1
        
        # Spawn regular obstacles
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
        
        # Move regular obstacles
        new_obs = []
        for obs in self.obstacles:
            spec = OBSTACLE_TYPES[obs["type"]]
            obs["y"] += spec["speed"] * self.speed_factor
            if obs["y"] < SCREEN_HEIGHT:
                new_obs.append(obs)
            else:
                self.hit_obstacles.discard(obs["id"])
        self.obstacles = new_obs
        
        # Move foreign objects diagonally (Rule 1)
        new_foreign = []
        for fobj in self.foreign_objects:
            fobj["x"] += fobj["dx"] * self.speed_factor
            fobj["y"] += fobj["dy"] * self.speed_factor
            
            # Bounce off walls
            if fobj["x"] <= 0 or fobj["x"] >= SCREEN_WIDTH - fobj["size"]:
                fobj["dx"] *= -1
            
            if fobj["y"] < SCREEN_HEIGHT:
                new_foreign.append(fobj)
            else:
                self.hit_foreign.discard(fobj["id"])
        self.foreign_objects = new_foreign
        
        # Collision detection with regular obstacles
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
        
        # Collision detection with foreign objects (Rule 1)
        for fobj in self.foreign_objects:
            if fobj["id"] not in self.hit_foreign:
                ship_center_x = self.ship_x + SHIP_SIZE // 2
                ship_center_y = self.ship_y + SHIP_SIZE // 2
                fobj_center_x = fobj["x"] + fobj["size"] // 2
                fobj_center_y = fobj["y"] + fobj["size"] // 2
                
                if (abs(ship_center_x - fobj_center_x) < (SHIP_SIZE + fobj["size"]) // 2 and
                    abs(ship_center_y - fobj_center_y) < (SHIP_SIZE + fobj["size"]) // 2):
                    self.hp -= 15  # Foreign objects do damage
                    self.hit_foreign.add(fobj["id"])
        
        # Update score
        if not self.game_won and self.hp > 0:
            self.score_flight += 1
        
        # Check win/lose
        if self.score_flight >= WIN_SCORE and not self.game_won:
            self.game_won = True
            reward = 50 + self.hp // 2
            self.points += reward
            self.last_flight_crashed = False
            
            # Rule 4: Adaptive difficulty after perfect run
            self.perfect_runs += 1
            if self.perfect_runs == 1:
                self.base_ship_speed += 0.05
            elif self.perfect_runs == 2:
                self.foreign_objects_count += 1
            elif self.perfect_runs >= 3:
                self.base_ship_speed += 0.10
                self.foreign_objects_count += 1
                self.perfect_runs = 0  # Reset counter
        
        if self.hp <= 0 and not self.game_won:
            reward = self.score_flight // 10
            self.points += reward
            
            # Rule 1: If crashed, add a foreign object for next flight
            if not self.last_flight_crashed:
                self.foreign_objects_count += 1
                self.last_flight_crashed = True
            
            # Rule 4: Reduce difficulty slightly on crash
            self.perfect_runs = 0
            self.base_ship_speed = max(1.0, self.base_ship_speed - 0.10)
            if self.foreign_objects_count > 0:
                self.foreign_objects_count = max(0, self.foreign_objects_count - 1)
        
        # Draw regular obstacles
        for obs in self.obstacles:
            spec = OBSTACLE_TYPES[obs["type"]]
            pygame.draw.ellipse(self.screen, spec["color"], 
                              (obs["x"], obs["y"], spec["size"], spec["size"]))
            pygame.draw.ellipse(self.screen, WHITE, 
                              (obs["x"], obs["y"], spec["size"], spec["size"]), 2)
        
        # Draw foreign objects as triangles (Rule 1)
        for fobj in self.foreign_objects:
            size = fobj["size"]
            cx, cy = fobj["x"] + size // 2, fobj["y"] + size // 2
            points = [
                (cx, cy - size // 2),
                (cx - size // 2, cy + size // 2),
                (cx + size // 2, cy + size // 2)
            ]
            pygame.draw.polygon(self.screen, fobj["color"], points)
            pygame.draw.polygon(self.screen, WHITE, points, 2)
        
        # Draw ship
        pygame.draw.rect(self.screen, BLUE, 
                        (self.ship_x, self.ship_y, SHIP_SIZE, SHIP_SIZE))
        pygame.draw.rect(self.screen, CYAN, 
                        (self.ship_x, self.ship_y, SHIP_SIZE, SHIP_SIZE), 3)
        
        # Draw stats
        self.draw_text(f"HP: {max(0, self.hp)}/{self.max_hp}", 10, 10, self.small_font, RED if self.hp < 30 else WHITE)
        self.draw_text(f"Score: {self.score_flight}/{WIN_SCORE}", SCREEN_WIDTH - 250, 10, self.small_font, LIME)
        self.draw_text(f"Triangles: {len(self.foreign_objects)}", SCREEN_WIDTH // 2 - 70, 10, self.small_font, PINK)
        
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
            self.draw_text("CRASHED!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                          self.font, RED, center=True)
            reward = self.score_flight // 10
            self.draw_text(f"Earned {reward} points | +1 Triangle next flight", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, 
                          self.small_font, YELLOW, center=True)
        
        # Handle input
        keys = pygame.key.get_pressed()
        movement = 5 + self.upgrades["maneuver"]
        if keys[pygame.K_LEFT]:
            self.ship_x = max(0, self.ship_x - movement)
        if keys[pygame.K_RIGHT]:
            self.ship_x = min(SCREEN_WIDTH - SHIP_SIZE, self.ship_x + movement)
        if keys[pygame.K_UP]:
            self.speed_factor = self.base_ship_speed * 2
        if keys[pygame.K_DOWN]:
            self.speed_factor = self.base_ship_speed * 0.5
    
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
        self.draw_text(f"Collected: {len(self.collected_trash_items)}", panel_x, 210, self.tiny_font, LIME)
        
        # Hint
        if len(self.trash) > 0:
            nearest = self.trash[0]
            self.draw_text(f"Hint:", panel_x, 250, self.tiny_font, LIME)
            self.draw_text(f"({nearest[0]}, {nearest[1]})", panel_x, 275, self.tiny_font, LIME)
        
        # Input box
        self.draw_text("ENTER COORDINATES (X Y):", panel_x, 310, self.tiny_font, CYAN)
        pygame.draw.rect(self.screen, WHITE, (panel_x, 340, 250, 40), 2)
        self.draw_text(self.input_text, panel_x + 10, 350, self.small_font, WHITE)
        
        # Fire button
        if self.draw_button("FIRE", panel_x, 400, 120, 40, RED, ORANGE, lambda: "fire"):
            self.fire_laser()
        
        # Reset button
        if self.draw_button("RESET", panel_x + 130, 400, 120, 40, PURPLE, (255, 0, 255), lambda: "reset"):
            self.reset_trash()
        
        # Back button
        self.draw_text("ESC: Back to Menu", panel_x, 460, self.tiny_font, WHITE)
        
        # Mission complete
        if self.mission_complete:
            self.draw_text("MISSION COMPLETE!", SCREEN_WIDTH // 2, 500, 
                          self.font, LIME, center=True)
            self.draw_text(f"Collected {len(self.collected_trash_items)} items!", SCREEN_WIDTH // 2, 540, 
                          self.small_font, YELLOW, center=True)
    
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
                # Rule 2 & 3: Track collected items
                for _ in hit_indices:
                    self.collected_trash_items.append(self.generate_trash_item())
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
    
    def generate_trash_item(self):
        """Generate a trash item based on rarity (Rule 6 & 7)"""
        # Choose category
        category = random.choice(list(TRASH_DATABASE.keys()))
        items = TRASH_DATABASE[category]
        
        # Weighted selection based on rarity (higher rarity = lower spawn chance)
        weights = [100 - item["rarity"] for item in items]
        selected_item = random.choices(items, weights=weights, k=1)[0]
        
        return {
            "name": selected_item["name"],
            "category": category,
            "rarity": selected_item["rarity"],
            "usefulness": selected_item["usefulness"],
            "color": selected_item["color"],
            "x": random.randint(100, SCREEN_WIDTH - 100),
            "y": random.randint(100, 350)
        }
    
    def setup_recycle_mission(self):
        """Setup recycle mission with collected items (Rule 5)"""
        self.recycle_items = self.collected_trash_items.copy()
        self.recycle_score = 0
        self.combo_count = 0
        self.last_three_usefulness = []
        self.error_message = None
        self.error_timer = 0
    
    def recycle_scene(self):
        self.screen.fill(BLACK)
        
        # Title
        self.draw_text("RECYCLE MISSION", SCREEN_WIDTH // 2, 30, self.font, GREEN, center=True)
        self.draw_text(f"Score: {self.recycle_score} | Combo: {self.combo_count}", 
                      SCREEN_WIDTH // 2, 70, self.small_font, YELLOW, center=True)
        
        # Draw bins (Rule 5)
        for bin_name, bin_data in self.bins.items():
            rect = bin_data["rect"]
            color = bin_data["color"]
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, WHITE, rect, 3)
            
            # Bin label
            label_y = rect.y + rect.height // 2
            self.draw_text(bin_name.split('/')[0], rect.centerx, label_y - 10, 
                          self.tiny_font, WHITE, center=True)
            self.draw_text(bin_name.split('/')[1] if '/' in bin_name else "", 
                          rect.centerx, label_y + 10, self.tiny_font, WHITE, center=True)
        
        # Draw trash items (Rule 5)
        mouse_pos = pygame.mouse.get_pos()
        hovered_item = None
        
        for item in self.recycle_items:
            if self.dragging_item == item:
                continue
                
            # Draw circle
            pygame.draw.circle(self.screen, item["color"], (item["x"], item["y"]), 20)
            pygame.draw.circle(self.screen, WHITE, (item["x"], item["y"]), 20, 2)
            
            # Check hover (Rule 5: show name on hover)
            dist = math.sqrt((mouse_pos[0] - item["x"]) ** 2 + (mouse_pos[1] - item["y"]) ** 2)
            if dist <= 20:
                hovered_item = item
        
        # Draw dragging item
        if self.dragging_item:
            mouse_x, mouse_y = mouse_pos
            x = mouse_x + self.drag_offset[0]
            y = mouse_y + self.drag_offset[1]
            pygame.draw.circle(self.screen, self.dragging_item["color"], (x, y), 20)
            pygame.draw.circle(self.screen, WHITE, (x, y), 20, 2)
        
        # Show item name on hover (Rule 5)
        if hovered_item:
            self.draw_text(hovered_item["name"], SCREEN_WIDTH // 2, 110, 
                          self.small_font, CYAN, center=True)
            self.draw_text(f"Rarity: {hovered_item['rarity']} | Usefulness: {hovered_item['usefulness']}", 
                          SCREEN_WIDTH // 2, 140, self.tiny_font, WHITE, center=True)
        
        # Show error message (Rule 6)
        if self.error_timer > 0:
            self.draw_text("TECHNICAL ERROR!", SCREEN_WIDTH // 2, 200, 
                          self.font, RED, center=True)
            self.error_timer -= 1
        
        # Instructions
        self.draw_text("Drag and drop trash into correct bins", SCREEN_WIDTH // 2, 
                      SCREEN_HEIGHT - 30, self.tiny_font, WHITE, center=True)
        self.draw_text("ESC: Back to Menu", 10, SCREEN_HEIGHT - 30, self.tiny_font, WHITE)
        
        # Handle mouse events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if clicking on an item
                for item in self.recycle_items:
                    dist = math.sqrt((event.pos[0] - item["x"]) ** 2 + (event.pos[1] - item["y"]) ** 2)
                    if dist <= 20:
                        self.dragging_item = item
                        self.drag_offset = (item["x"] - event.pos[0], item["y"] - event.pos[1])
                        break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging_item:
                    # Check which bin it's dropped in
                    dropped_in_bin = None
                    for bin_name, bin_data in self.bins.items():
                        if bin_data["rect"].collidepoint(event.pos):
                            dropped_in_bin = bin_name
                            break
                    
                    if dropped_in_bin:
                        self.check_recycle_sort(self.dragging_item, dropped_in_bin)
                        self.recycle_items.remove(self.dragging_item)
                    
                    self.dragging_item = None
        
        # Check if mission complete
        if len(self.recycle_items) == 0 and len(self.collected_trash_items) > 0:
            self.draw_text("RECYCLING COMPLETE!", SCREEN_WIDTH // 2, 250, 
                          self.font, LIME, center=True)
            self.draw_text(f"Final Score: {self.recycle_score}", SCREEN_WIDTH // 2, 300, 
                          self.small_font, YELLOW, center=True)
            self.points += self.recycle_score
            
            # Rule 3: Foreign objects collected reduce triangle count
            self.collected_trash_items = []
    
    def check_recycle_sort(self, item, bin_name):
        """Check if item is sorted correctly and calculate score (Rule 6)"""
        correct = item["category"] == bin_name
        
        if correct:
            # Calculate score using formula (Rule 6)
            rarity = item["rarity"]
            usefulness = item["usefulness"]
            base_score = (rarity + usefulness) // 50 + usefulness
            self.recycle_score += base_score
            
            # Track for combo (Rule 6)
            self.last_three_usefulness.append(usefulness)
            if len(self.last_three_usefulness) > 3:
                self.last_three_usefulness.pop(0)
            
            # Check combo: 3 consecutive items with usefulness > 80
            if len(self.last_three_usefulness) == 3:
                if all(u > 80 for u in self.last_three_usefulness):
                    self.recycle_score += 10
                    self.combo_count += 1
                    self.last_three_usefulness = []
            
            # Rule 3: If this was a foreign object, reduce count
            if random.random() < 0.3:  # 30% chance item is a foreign object
                self.foreign_objects_count = max(0, self.foreign_objects_count - 1)
        else:
            # Wrong bin - show error and subtract points (Rule 6)
            self.error_message = "TECHNICAL ERROR"
            self.error_timer = 60
            penalty = item["usefulness"] // 2
            self.recycle_score = max(0, self.recycle_score - penalty)
            self.last_three_usefulness = []  # Reset combo
    
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
                
                # Handle recycle scene mouse events separately
                if self.scene == "recycle":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if clicking on an item
                        for item in self.recycle_items:
                            dist = math.sqrt((event.pos[0] - item["x"]) ** 2 + (event.pos[1] - item["y"]) ** 2)
                            if dist <= 20:
                                self.dragging_item = item
                                self.drag_offset = (item["x"] - event.pos[0], item["y"] - event.pos[1])
                                break
                    
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.dragging_item:
                            # Check which bin it's dropped in
                            dropped_in_bin = None
                            for bin_name, bin_data in self.bins.items():
                                if bin_data["rect"].collidepoint(event.pos):
                                    dropped_in_bin = bin_name
                                    break
                            
                            if dropped_in_bin:
                                self.check_recycle_sort(self.dragging_item, dropped_in_bin)
                                self.recycle_items.remove(self.dragging_item)
                            
                            self.dragging_item = None
            
            if self.scene == "menu":
                self.menu_scene()
            elif self.scene == "flight":
                self.flight_scene()
            elif self.scene == "trash":
                self.trash_scene()
            elif self.scene == "recycle":
                self.recycle_scene()
            elif self.scene == "upgrade":
                self.upgrade_scene()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()