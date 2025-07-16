# CORALL: COLREGs-Guided Risk-Aware LLM for Maritime Autonomous Navigation

CORALL is a novel framework that integrates Large Language Models with real-time risk assessment for autonomous maritime navigation. The system combines LLM-based decision-making with traditional motion planning to enable COLREGs-compliant collision avoidance in autonomous surface vessels.

This repository contains the complete implementation of the CORALL framework as published in our research paper, providing researchers and practitioners with a comprehensive tool for studying LLM-guided autonomous maritime navigation.

## Features

- **LLM-based COLREGs Interpretation**: Advanced decision-making using OpenAI GPT and Claude models
- **Real-time Risk Assessment**: DCPA/TCPA calculations and comprehensive risk metrics
- **Multi-vessel Encounter Handling**: Complex scenarios with multiple target vessels
- **Explainable Navigation Decisions**: Transparent reasoning for autonomous maneuvers
- **Standardized Test Scenarios**: Validation across 22 Imazu test scenarios
- **Dynamic Path Planning**: Intelligent waypoint navigation and trajectory optimization
- **Vessel Dynamics Simulation**: Realistic modeling of marine vessel movement and control
- **Comparison Mode**: Side-by-side analysis of LLM vs baseline navigation decisions
- **Real-time Animation**: Interactive visualization of vessel movements and decisions
- **Modular Architecture**: Clean, extensible codebase with clear separation of concerns

## Project Structure

```
CORALL/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── setup.py               # Package installation
├── README.md              # This file
├── .gitignore            # Git ignore rules
│
├── src/                   # Source code
│   ├── core/             # Core simulation components
│   │   ├── simulation.py # Main simulation loop
│   │   └── integration.py # Numerical integration
│   │
│   ├── dynamics/         # Vessel dynamics and control
│   │   ├── vessel_dynamics.py
│   │   ├── controller.py
│   │   └── actuator_modeling.py
│   │
│   ├── navigation/       # Navigation and path planning
│   │   ├── planning.py
│   │   ├── obstacle_sim.py
│   │   └── reactive_avoidance.py
│   │
│   ├── risk_assessment/  # Risk and collision analysis
│   │   ├── cpa_calculations.py
│   │   ├── cpa_calculations_0speed.py
│   │   ├── cpa_calculations2.py
│   │   └── risk_calculations.py
│   │
│   ├── decision_making/  # Autonomous decision systems
│   │   ├── decision_making.py
│   │   ├── decision_makingllm.py
│   │   └── decision_makingllm1.py
│   │
│   ├── visualization/    # Rendering and animation
│   │   ├── animate.py
│   │   ├── rendering.py
│   │   └── save_animation.py
│   │
│   └── utils/           # Utilities and helpers
│       ├── imazu_cases.py
│       └── validation.py
│
├── tests/               # Test suite
├── docs/                # Documentation
├── examples/            # Example simulations
├── config/              # Configuration files
└── img/                 # Output images and animations
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key (get from: https://platform.openai.com/api-keys)
- Claude API key (get from: https://console.anthropic.com/)
- Internet connection for LLM API calls

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Klins101/CORALL
cd CORALL
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up API keys and configuration:

Create a `.env` file in the root directory with your API keys:
```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=50

# Claude Configuration  
CLAUDE_API_KEY=your-claude-api-key-here
CLAUDE_MODEL=claude-3-sonnet-20240229
CLAUDE_TEMPERATURE=0.1
CLAUDE_MAX_TOKENS=50

# Default LLM Provider
LLM_PROVIDER=openai
```

**Note**: The `.env` file is not included in the repository for security reasons. You must create it yourself with your own API keys.

5. Run a simulation:
```bash
python main.py
```


## Usage

### Basic Usage

Run the default simulation (Case 1):
```bash
python main.py
```

### Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --case_number INT    Simulation scenario (default: 1)
  --sim_time FLOAT     Simulation duration in seconds (default: 450.0)
  --dt FLOAT           Time step size (default: 0.1)
  --no_animation       Disable real-time animation
  --output_dir PATH    Output directory for results (default: img/)
  --llm INT           Enable LLM decision making (0=off, 1=on, default: 0)
  --llm_provider STR   LLM provider (openai, claude)
  --compare            Run comparison between LLM and baseline simulation
```

### Examples

1. **Run Case 2 with extended simulation time:**
```bash
python main.py --case_number 2 --sim_time 600
```

2. **Quick simulation without animation:**
```bash
python main.py --no_animation --sim_time 300
```

3. **Run with LLM-based decision making:**
```bash
python main.py --llm 1 --case_number 3
```

4. **Custom output directory:**
```bash
python main.py --output_dir results/experiment1/
```

5. **Run LLM vs Baseline comparison:**
```bash
python main.py --compare --llm_provider claude --case_number 1
python main.py --compare --llm_provider openai --case_number 2
```

## Simulation Cases

The system includes several predefined test scenarios (Imazu cases) that represent common marine navigation situations:

- **Case 1**: Head-on encounter
- **Case 2**: Crossing situation
- **Case 3**: Overtaking scenario
- **Case 4**: Multiple vessel encounter
- **Case 5-15**: Various complex scenarios

## Output

Each simulation run generates:

1. **Animation**: `scenario_animation{case_number}.gif`
   - Real-time visualization of vessel movements
   - Obstacle positions and trajectories
   - Risk zones and avoidance maneuvers

2. **Analysis Plots**: `plot_dcpa_tcpa_risk_{case_number}.png`
   - DCPA (Distance at Closest Point of Approach)
   - TCPA (Time to Closest Point of Approach)
   - Distance to obstacles over time
   - Risk metrics evolution

3. **Simulation Results**: `simulation_result{case_number}.png`
   - Final vessel trajectories
   - Waypoint achievements
   - Collision avoidance paths

### Comparison Mode Output (--compare)

When using `--compare` flag, additional files are generated:

1. **Kdir Comparison**: `kdir_comparison_{provider}_case_{number}.png`
   - Side-by-side comparison of turn decisions
   - Baseline vs LLM steering commands
   - Statistical analysis of navigation behavior

2. **Trajectory Comparison**: `trajectory_comparison_{provider}_case_{number}.png`
   - Overlay of vessel paths (baseline vs LLM)
   - Start/end positions and obstacle locations
   - Visual comparison of navigation efficiency

3. **Summary Report**: `comparison_summary_{provider}_case_{number}.txt`
   - Quantitative comparison statistics
   - Turn frequency and risk management analysis
   - Performance metrics and behavioral insights

## Configuration

### API Keys and Security

**Important Security Notes:**
- Never commit your `.env` file to version control
- Keep your API keys secure and do not share them publicly
- The `.env` file is already included in `.gitignore` for security
- API keys are loaded automatically when the simulation starts
- You can switch between providers using the `LLM_PROVIDER` environment variable

### LLM Configuration

You can customize LLM behavior by modifying the environment variables:

```bash
# Adjust response length (max 50 characters recommended)
OPENAI_MAX_TOKENS=50
CLAUDE_MAX_TOKENS=50

# Adjust creativity (0.0 = deterministic, 1.0 = creative)
OPENAI_TEMPERATURE=0.1
CLAUDE_TEMPERATURE=0.1

# Switch between models
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4
CLAUDE_MODEL=claude-3-sonnet-20240229  # or claude-3-haiku-20240307
```

### Customizing LLM Prompt Template

You can customize the LLM prompt template to implement your own COLREGs interpretation or navigation logic. The prompt template is located in:

```
src/decision_making/multi_llm_decision.py
```

To modify the prompt:

1. **Edit the system prompt** in the `MultiLLMCOLREGSInterpreter` class (around line 131):

```python
self.system_prompt = """You are a ship navigation officer. Make COLREGs-compliant decisions.

IMPORTANT: Give response of not more than 50 characters.

Reply with only:
- "turn starboard" (right turn)
- "turn port" (left turn)  
- "stand on" (maintain course)

Keep response under 50 characters."""
```

2. **Customize for your needs**:
   - Add specific COLREGs rules you want to emphasize
   - Modify the response format if needed
   - Adjust the character limit (but keep responses concise)
   - Add domain-specific knowledge or constraints

3. **Example custom prompt**:

```python
self.system_prompt = """You are an expert maritime navigator with 20 years experience.
Follow IMO COLREGs strictly. Consider vessel types, weather, and traffic density.

Response format (max 50 chars):
- "turn starboard" - right turn per Rule 14/15
- "turn port" - left turn per Rule 16/17  
- "stand on" - maintain course per Rule 13/17

Prioritize safety over efficiency."""
```

4. **Response parsing**: If you change the response format, also update the `extract_kdir_from_response()` function in the same file to properly parse your custom responses.

**Note**: Keep responses under 50 characters for optimal performance and ensure they can be parsed by the `extract_kdir_from_response()` function.

### Vessel Parameters

Modify vessel characteristics in the simulation:
- Length Overall (LOA)
- Beam Overall (BOL)
- Maximum speed
- Turning rates

### Control Parameters

Adjust control system settings:
- PID controller gains
- Sampling time
- Actuation limits

### Risk Thresholds

Configure safety parameters:
- Minimum safe distance
- Risk assessment weights
- COLREGs compliance levels

## API Reference

### Core Modules

```python
from src.core.simulation import run_simulation
from src.dynamics.vessel_dynamics import vessel_dynamics
from src.navigation.planning import waypoint_selection
from src.risk_assessment.cpa_calculations import cpa_calculations
```

### Custom Simulations

Create custom simulation scenarios:

```python
from src.core.simulation import run_simulation
import numpy as np

# Define custom waypoints
waypoints = np.array([[100, 200], [300, 400], [500, 300]])

# Run simulation with custom parameters
run_simulation(
    case_number=22,
    waypoints=waypoints,
    sim_time=600.0,
    dt=0.05
)
```

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions
- Include type hints where applicable
- Write unit tests for new features

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run with coverage:
```bash
python -m pytest --cov=src tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use CORALL in your research, please cite:
```bibtex
@software{corall_2025,
  title = {CORALL: COLREGs-Guided Risk-Aware LLM for Maritime Autonomous Navigation},
  author = {Agyei, Klinsmann and Sarhadi, Pouria and Naeem, Wasif },
  year = {2025},
  url = {https://github.com/Klins101/CORALL}
}
```

## Acknowledgments

This work was developed in collaboration with:
- Dr. Pouria Sarhadi (University of Hertfordshire)
- Prof. Wasif Naeem (Queen's University Belfast)
- Klinsmann Agyei (University of Hertfordshire)

- COLREGs implementation based on IMO regulations
- Vessel dynamics model inspired by Fossen's marine control systems
- Risk assessment algorithms adapted from maritime safety research
- LLM integration using OpenAI GPT and Anthropic Claude models

## Contact

For questions or support, please open an issue on GitHub or contact:
- Dr. Pouria Sarhadi - p.sarhadi@herts.ac.uk
- Prof. Wasif Naeem - w.naeem@ee.qub.ac.uk
- Klinsmann Agyei - k.agyei@herts.ac.uk