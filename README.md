This is Kairyou's game project with AI assistant. All the idea is belong to Kairyou.
The project was made whhile handling the NASA SPACE APP CHALLENGE 2025.

---
# Game TRASH SPACE 

> An educational space cleanup and recycling game built with Pygame

TrashSpace is an engaging arcade-style game that combines space navigation, precision shooting, and environmental education. Navigate through space debris, collect cosmic trash, and learn about proper recycling practices while managing adaptive difficulty mechanics.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Mechanics](#game-mechanics)
- [Missions](#missions)
- [Scoring System](#scoring-system)
- [Controls](#controls)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Three Unique Missions**: Flight navigation, trash collection, and recycling sorting
- **Adaptive Difficulty System**: Game difficulty adjusts based on your performance
- **Educational Content**: Learn about space debris and recycling with 50 real items
- **Dynamic Obstacles**: Regular obstacles plus foreign objects with diagonal movement
- **Upgrade System**: Improve your ship's armor, maneuverability, and laser range
- **Combo System**: Earn bonus points for consecutive high-value recycling
- **Rarity-Based Spawning**: Realistic item distribution based on rarity values

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Kairyou-ML/SpaceTrash.git
```

2. Install required dependencies:
```bash
pip install pygame numpy
```

3. Run the game:
```bash
python checkpoint2.py 
```
NOTE: change name file with the last checkpoint if it exists. (For instance, use ```python checkpoint3.py ```)

##  How to Play

### Getting Started

1. Launch the game and you'll see the main menu
2. Choose from three available missions:
   - **Flight Mission**: Navigate to Mars while avoiding obstacles
   - **Trash Collection**: Use coordinates to shoot down space debris
   - **Recycle Trash**: Sort collected items into proper bins (unlocked after collection)
3. Earn points to upgrade your ship's capabilities

### Missions Overview

#### 🚀 Flight Mission
Navigate your spaceship to Mars while avoiding:
- **Meteors** (red circles): Fast-moving, 20 damage
- **Satellites** (gray circles): Slow-moving, 30 damage
- **Foreign Objects** (colored triangles): Move diagonally, 15 damage

**Objective**: Score 1,000 points without losing all HP

#### 🔫 Trash Collection
Use your ship's laser to collect space debris:
1. Enter coordinates (X, Y) on the radar
2. Fire your laser to collect trash within the blast radius
3. Collect all debris to complete the mission

**Bonus**: Higher accuracy = bigger rewards!

#### ♻️ Recycle Mission
Sort collected trash into three categories:
1. **Rocket/Rover Parts** (Blue bin): Spacecraft components
2. **Metal/Meteorite** (Gray bin): Metal fragments and space rocks
3. **Biological/Waste** (Green bin): Organic matter and gases

**Tip**: Hover over items to see their names and properties!

## Game Mechanics

### Foreign Object System

**Rule 1**: Crashes spawn foreign objects
- Each crash in Flight Mission adds **+1 triangular foreign object** to the next flight
- Foreign objects move **diagonally** and bounce off screen edges
- Different colors indicate different objects (variety increases with difficulty)

**Rule 2**: Scaling difficulty
- Number of trash pieces = Base (15) + Foreign object count
- More crashes = More debris to collect

**Rule 3**: Redemption mechanic
- Successfully recycling items reduces foreign object count
- Clean recycling = Easier future flights

### Adaptive Difficulty

The game adjusts challenge based on performance:

| Performance | Effect |
|-------------|--------|
| 1 Perfect Run | +5% ship speed |
| 2 Perfect Runs | +1 foreign object |
| 3 Perfect Runs | +10% speed + 1 object (counter resets) |
| 1 Crash | -10% speed OR remove 1 object |

**Perfect Run**: Complete Flight Mission with HP > 0

### Scoring System

#### Trash Collection
- **Base**: 5 points per item hit
- **Completion Bonus**: 50 × accuracy percentage

#### Recycling Formula
```
Item Score = ⌊(Rarity + Usefulness) / 50⌋ + Usefulness
```

- **Correct Bin**: Add calculated score
- **Wrong Bin**: "TECHNICAL ERROR" - Lose (Usefulness / 2) points
- **Combo Bonus**: +10 points for 3 consecutive items with Usefulness > 80

#### Flight Mission
- **Score**: 1 point per frame survived
- **Completion**: 50 + (Remaining HP / 2) points
- **Crash**: (Score / 10) points

##  Controls

### Flight Mission
| Key | Action |
|-----|--------|
| ← → | Move ship left/right |
| ↑ | Boost speed (2x) |
| ↓ | Slow down (0.5x) |
| R | Reset mission |
| ESC | Return to menu |

### Trash Collection
| Key | Action |
|-----|--------|
| Type coordinates | Enter X Y values (e.g., "10 20") |
| ENTER | Fire laser |
| ESC | Return to menu |

### Recycle Mission
| Action | Control |
|--------|---------|
| View item info | Hover over item |
| Pick up item | Click and hold |
| Drop item | Release in bin |
| ESC | Return to menu |

##  Requirements

```
python>=3.7
pygame>=2.0.0
numpy>=1.19.0
```

##  Project Structure

```
trashspace/
├── checkpoint[n].py          # Main game file lastupdated after n temps
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── LICENSE               # License information
└── Other files          # Process from basic idea to final production
```

## 🎓 Educational Content

The game features **50 real space debris items** across three categories:

### Rocket/Rover Parts (16 items)
Spacecraft components like solar panels, robotic arms, thrusters, and control systems.

### Metal/Meteorite (17 items)
Metal fragments, meteorite samples, and alloy pieces with varying rarity.

### Biological/Waste (17 items)
Organic waste, gas emissions, and biological materials from space missions.

Each item has:
- **Name**: Real-world identification
- **Rarity** (0-100): How rare the item is
- **Usefulness** (0-100): Value for recycling/reuse
- **Color**: Visual identification

## 🏆 Tips & Strategies

1. **Start with upgrades**: Invest in Maneuver first for better control
2. **Learn patterns**: Obstacles spawn randomly, but foreign objects are predictable
3. **Accuracy matters**: Better aim in Trash Collection = More bonus points
4. **Study items**: Memorize which items belong in which bin
5. **Combo chain**: Target high-usefulness items consecutively for bonuses
6. **Risk vs. Reward**: Boost speed for faster completion but higher crash risk

## Known Issues

- None currently reported

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Future Enhancements

- [ ] Sound effects and background music
- [ ] High score leaderboard
- [ ] Additional mission types
- [ ] Multiplayer co-op mode
- [ ] Save/load game progress
- [ ] Achievement system
- [ ] Tutorial mode for beginners

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments

- Inspired by real space debris challenges
- Educational content based on actual spacecraft components
- Built with Python and Pygame

## 📞 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: work.pibangbon@gmail.com

---

⭐ **Star this repository if you enjoyed the game!** ⭐

Made with Python 🐍 and Pygame 🎮
