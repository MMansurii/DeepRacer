# Custom Racing Line Creator for AWS DeepRacer

An interactive web tool for creating custom optimal racing lines for AWS DeepRacer tracks. Design your perfect racing strategy by clicking and visualizing track waypoints with precision.

## 🏁 Features

### ✨ **Interactive Racing Line Creation**
- **Click-to-Create**: Build your optimal racing line by clicking anywhere on the track
- **Drag-to-Edit**: Move existing points with precision using edit mode
- **Real-time Visualization**: See your racing line rendered instantly as a red path
- **Point Management**: Add, remove, and reorder racing line points easily

### 📊 **Advanced Track Analysis**
- **Waypoint Information**: Click on track waypoints to see detailed analysis
- **Curvature Analysis**: View turn severity and recommended speeds
- **Track Geometry**: Access precise boundary coordinates and track width
- **Racing Metrics**: Get steering angles, speeds, and turn classifications

### 🔧 **Developer-Friendly Export**
- **Reward Function Ready**: Export coordinates in copy-paste format
- **High Precision**: 6-decimal accuracy for exact positioning
- **JSON Format**: Compatible with AWS DeepRacer reward functions
- **Instant Export**: Generate coordinate arrays with one click

## 🚀 Live Demo

**[Try it now!](https://mmansurii.github.io/DeepRacer/)**

## 🏁 Features

### ✨ **Interactive Racing Line Creation**
- **Click-to-Create**: Build your optimal racing line by clicking anywhere on the track
- **Drag-to-Edit**: Move existing points with precision using edit mode
- **Real-time Visualization**: See your racing line rendered instantly as a red path
- **Point Management**: Add, remove, and reorder racing line points easily

### 📊 **Advanced Track Analysis**
- **Waypoint Information**: Click on track waypoints to see detailed analysis
- **Curvature Analysis**: View turn severity and recommended speeds
- **Track Geometry**: Access precise boundary coordinates and track width
- **Racing Metrics**: Get steering angles, speeds, and turn classifications

### 🔧 **Developer-Friendly Export**
- **Reward Function Ready**: Export coordinates in copy-paste format
- **High Precision**: 6-decimal accuracy for exact positioning
- **JSON Format**: Compatible with AWS DeepRacer reward functions
- **Instant Export**: Generate coordinate arrays with one click

## 📋 Quick Start

### 1. **Load Track Data**
```
Paste your track waypoint data into the text area
Click "Process Data" to load the track
```

### 2. **Create Your Racing Line**
```
• Select "Create Path Mode" (default)
• Click anywhere on the track to add points
• Points automatically connect to form your racing line
• Use "Edit Path Mode" to adjust existing points
```

### 3. **Export for DeepRacer**
```
Click "Export Path" to get coordinates
Copy the generated code into your reward function
Use the coordinates to calculate distance rewards
```

## 🎮 Controls & Interface

| Mode | Action | Description |
|------|---------|------------|
| **Create Path** | Click on track | Add new point to racing line |
| **Edit Path** | Click & drag red points | Move existing racing line points |
| **Both Modes** | Click gray waypoints | View detailed track information |

### 🔧 **Toolbar Commands**
- **Clear Path**: Remove all racing line points
- **Undo Last**: Remove the most recently added point
- **Export Path**: Generate coordinate array for reward functions

## 📊 Track Data Analysis

When you click on any gray waypoint marker, you'll see:

- **Position Coordinates**: Exact center, left, and right boundary positions
- **Track Geometry**: Width, curvature, and turn classification
- **Racing Recommendations**: Suggested speeds and steering angles
- **Turn Analysis**: Left/right/straight classification with severity

## 🔄 Supported Track Formats

The tool accepts waypoint data in the following format:
```python
[[ center_x, center_y, left_x, left_y, right_x, right_y ],
 [ center_x, center_y, left_x, left_y, right_x, right_y ],
 ...]
```

### Example Data Sources:
- AWS DeepRacer Console waypoint exports
- Track geometry files from DeepRacer community
- Custom track waypoint arrays

## 🎯 Integration with Reward Functions

### Basic Distance Reward Example:
```python
def reward_function(params):
    # Your custom racing line points (exported from tool)
    optimal_line = [
        [3.408315, 1.471770],
        [3.278316, 1.471245],
        # ... more points from export
    ]
    
    # Calculate distance to optimal line
    current_pos = [params['x'], params['y']]
    closest_point = find_closest_point(current_pos, optimal_line)
    distance = calculate_distance(current_pos, closest_point)
    
    # Reward closer adherence to your custom line
    if distance < 0.1:
        return 10.0
    elif distance < 0.3:
        return 5.0
    else:
        return 1.0
```

## 🛠️ Technical Details

### Built With:
- **HTML5 Canvas**: For interactive track visualization
- **Vanilla JavaScript**: No dependencies, runs anywhere
- **Responsive Design**: Works on desktop and mobile browsers

### Browser Compatibility:
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📁 File Structure

```
deepracer-racing-line-creator/
├── index.html              # Main application file
├── README.md               # This documentation
└── track-data/             # Example track data files
    ├── 2024_reinvent_champ_ccw.txt
    ├── oval_track.txt
    └── sample_tracks.md
```

## 🚀 Getting Started

### Option 1: Use Online (Recommended)
1. Visit the [live demo link](https://mmansurii.github.io/DeepRacer/)
2. Paste your track waypoint data
3. Start creating your racing line!

### Option 2: Run Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/deepracer-racing-line-creator.git
   ```
2. Open `index.html` in your web browser
3. Load your track data and start designing!

## 📝 Usage Tips

### 🎯 **Creating Effective Racing Lines**
- **Apex Strategy**: Place points at the inside of turns for shortest path
- **S-Curves**: Create straight connections between opposite turns
- **Speed Zones**: Consider track curvature when placing points
- **Consistency**: Maintain smooth transitions between points

### 🔧 **Technical Best Practices**
- Start with fewer points and add detail as needed
- Use waypoint information to understand track characteristics
- Export frequently to test different line variations
- Consider track width when planning inside/outside positioning

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 

### Development Setup:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- AWS DeepRacer Community for track data formats
- Racing line optimization principles from motorsport theory
- Canvas API documentation and examples

## 📞 Support & Questions

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join the conversation in GitHub Discussions
- **Community**: Connect with other DeepRacer enthusiasts

---

**Ready to create your winning racing line? [Get started now!](https://mmansurii.github.io/DeepRacer/)**
