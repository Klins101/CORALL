# User Guide

## Getting Started

### Basic Usage

The simplest way to run a simulation:
```bash
python main.py
```

This runs Case 1 with default parameters (450 seconds, animation enabled).

### Command Line Options

```bash
python main.py [OPTIONS]
```

Available options:
- `--case_number INT`: Test scenario (1-23, default: 1)
- `--sim_time FLOAT`: Simulation duration in seconds (default: 450.0)
- `--dt FLOAT`: Time step size (default: 0.1)
- `--no_animation`: Disable real-time animation
- `--output_dir PATH`: Output directory (default: img/)
- `--llm INT`: Enable LLM decision making (0=off, 1=on, default: 0)

### Example Commands

```bash
# Quick test without animation
python main.py --no_animation --sim_time 60

# Run specific case with extended time
python main.py --case_number 8 --sim_time 600

# Save to custom directory
python main.py --output_dir results/test1/

# Enable LLM decision making
python main.py --llm 1 --case_number 2
```

## Understanding the Simulation

### Test Cases (Imazu Scenarios)

The simulation includes 23 predefined test cases representing different maritime encounters:

1. **Case 1**: Head-on encounter
2. **Case 2**: Crossing situation (starboard)
3. **Case 3**: Crossing situation (port)
4. **Case 8**: Overtaking scenario
5. **Case 15**: Multi-vessel encounter
6. **Cases 4-23**: Various complex scenarios

### Simulation Parameters

#### Vessel Configuration
- **Own Ship**: 30m length, 16m beam, typical merchant vessel
- **Target Ships**: 80m length, 30m beam, various speeds and headings
- **Speed**: Typical operating speed ~8-10 knots

#### Navigation
- **Waypoints**: Predefined path from origin to destination
- **Collision Avoidance**: Reactive avoidance based on CPA calculations
- **Safety Distances**: Configurable based on vessel dimensions

#### Control System
- **Heading Control**: PID controller for course keeping
- **Speed Control**: Constant speed with emergency capabilities
- **Actuator Limits**: Realistic rudder angle and rate limits

## Output Files

Each simulation generates several output files:

### 1. Animation (`scenario_animation{case}.gif`)
- Real-time visualization of vessel movements
- Shows collision avoidance maneuvers
- Risk zones and safety boundaries
- Waypoint navigation

### 2. Analysis Plots (`plot_dcpa_tcpa_risk_{case}.png/.eps`)
Four-panel plot showing:
- **DCPA**: Distance at Closest Point of Approach over time
- **Distance**: Current distance to all obstacles
- **TCPA**: Time to Closest Point of Approach
- **Risk**: Calculated collision risk metrics

### 3. Trajectory Plot (`simulation_result{case}.png/.eps`)
- Final vessel trajectories
- Waypoint achievements
- Collision avoidance paths
- Final positions

## Interpreting Results

### DCPA (Distance at Closest Point of Approach)
- **Good**: DCPA > 0.5 nmi (safe passing)
- **Caution**: DCPA 0.2-0.5 nmi (close encounter)
- **Danger**: DCPA < 0.2 nmi (collision risk)

### TCPA (Time to Closest Point of Approach)
- **Positive**: Vessels are approaching
- **Negative**: Vessels are separating
- **Zero**: Moment of closest approach

### Risk Values
- **0.0-0.3**: Low risk (normal operation)
- **0.3-0.7**: Medium risk (increased vigilance)
- **0.7-1.0**: High risk (evasive action required)

### Collision Avoidance Behavior
- **Stand-on**: Vessel maintains course and speed
- **Give-way**: Vessel alters course to avoid collision
- **Emergency**: Immediate evasive action

## Advanced Features

### LLM-Based Decision Making

Enable with `--llm 1`:
```bash
python main.py --llm 1 --case_number 2
```

**Requirements:**
- Install: `pip install langchain_openai langchain`
- Configure OpenAI API key

**Features:**
- COLREGs-compliant decision making
- Natural language reasoning
- Contextual situation assessment
- Adaptive behavior based on encounter type

### Custom Scenarios

You can modify scenarios by editing the obstacle configurations in `src/utils/imazu_cases.py`.

Example custom obstacle:
```python
# Add to obstacle_cases dictionary
case_custom = {
    'Xob': [1000, 2000],  # X positions in meters
    'Yob': [500, -500],   # Y positions in meters
    'Vob': [4.0, 6.0],    # Velocities in m/s
    'psiob': [np.pi/4, -np.pi/4]  # Headings in radians
}
```

### Performance Optimization

For faster simulations:
- Use `--no_animation` flag
- Reduce `--sim_time`
- Increase `--dt` (less precision, faster execution)

For higher precision:
- Decrease `--dt` (more precision, slower execution)
- Increase `--sim_time` for complete scenarios

## Troubleshooting

### Common Issues

1. **Simulation runs slowly**
   - Use `--no_animation` flag
   - Reduce simulation time
   - Close other applications

2. **Animation window not showing**
   - Check display configuration
   - Try different matplotlib backend
   - Use `--no_animation` as fallback

3. **Memory issues with long simulations**
   - Reduce `--sim_time`
   - Increase `--dt`
   - Monitor system memory

4. **LLM features not working**
   - Install required dependencies
   - Check API key configuration
   - Verify internet connection

### Getting Help

- Check the API reference for function details
- Review example scripts in `examples/`
- Examine output plots for simulation behavior
- Enable debug output for detailed information

## Best Practices

1. **Start Simple**: Begin with short simulations and no animation
2. **Understand Output**: Review all generated plots and files
3. **Test Systematically**: Try different cases to understand behavior
4. **Monitor Performance**: Check simulation speed and memory usage
5. **Validate Results**: Compare with maritime navigation principles
