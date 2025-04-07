# CORALL: COLREGs-Guided Risk-Aware LLM for Maritime Autonomous Navigation
CORALL is a novel framework that integrates Large Language Models with real-time risk assessment for autonomous maritime navigation. The system combines LLM-based decision-making with traditional motion planning to enable COLREGs-compliant collision avoidance in autonomous surface vessels.

## Features
- LLM-based COLREGs interpretation and decision-making
- Real-time risk assessment integration
- Multi-vessel encounter handling
- Explainable navigation decisions
- Validation across 22 standardized Imazu test scenarios
- Dynamic path planning and collision avoidance
- Comprehensive vessel dynamics simulation

## Requirements
```
python >= 3.8
numpy
matplotlib
langchain_openai
langchain_core
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Klins101/CORALL.git
cd CORALL
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```python
export OPENAI_API_KEY='your-api-key'
```

## Usage
Run the simulation with:
```bash
python main.py --case_number 1 --sim_time 450 --dt 0.1 --llm 1
```

Arguments:
- `--case_number`: Imazu test scenario number (1-22)
- `--sim_time`: Simulation duration in seconds
- `--dt`: Time step size
- `--no_animation`: Disable animation
- `--output_dir`: Output directory for results
- `--llm`: Enable LLM decision making (0=off, 1=on)

## Project Structure
```
├── main.py                    # Main simulation script
├── decision_makingllm.py      # LLM integration and decision making
├── planning.py                # Path planning and waypoint selection
├── vessel_dynamics.py         # Vessel dynamic model
├── risk_calculations.py       # Risk assessment implementation
├── cpa_calculations.py        # CPA calculations
└── imazu_cases.py            # Test scenario definitions
```

## Results
The simulation generates:
- Animated visualization of vessel trajectories
- DCPA, TCPA, and Risk plots
- Decision direction (Kdir) plots
- Simulation result visualizations

## Example Scenarios
Here are some example simulations demonstrating CORALL's performance across different encounter types:

### Case 2: Crossing Encounter
<p align="center">
  <img src="Simulation Results/Gifs/scenario_animation2.gif" alt="Crossing Encounter" width="400"/>
  <br>
  <em>Crossing encounter showing LLM-guided starboard turn decision</em>
</p>

### Case 8: Head-on with Crossing
<p align="center">
  <img src="Simulation Results/Gifs/scenario_animation8.gif" alt="Head-on with Crossing" width="400"/>
  <br>
  <em>Complex scenario handling Head-on vessel while managing crossing vessel</em>
</p>

### Case 21: Multi-vessel Encounter
<p align="center">
  <img src="Simulation Results/Gifs/scenario_animation21.gif" alt="Multi-vessel Scenario" width="400"/>
  <br>
  <em>Three-vessel encounter demonstrating complex decision-making capabilities</em>
</p>

Each animation shows:
- Own Ship (OS) in voilet
- Target Ships (TS) in blue, orange and green respectively depending on the number of target ships
- Vessel trajectories and maneuvers
- Real-time COLREGs-compliant decisions

## Analysis and Results
### Risk and CPA Analysis for case 1, 7, 21
<p align="center">
  <img src="Simulation Results/Analysis/plot_dcpa_tcpa_risk_1.png" alt="DCPA TCPA Risk Analysis for Case 1" width="200"/>
  <img src="Simulation Results/Analysis/plot_dcpa_tcpa_risk_7.png" alt="DCPA TCPA Risk Analysis for Case 7" width="200"/>
  <img src="Simulation Results/Analysis/plot_dcpa_tcpa_risk_21.png" alt="DCPA TCPA Risk Analysis for Case 21" width="200"/>
  <br>
  <em>Evolution of DCPA, TCPA, Range, and Risk parameters</em>
</p>


The plots demonstrate:
- DCPA/TCPA trends showing effective collision avoidance
- Risk assessment throughout the encounter
- Clear correlation between risk levels and LLM decisions
- Validation of COLREGs compliance through maneuver choices



## Contributing
This project was developed at:
- School of Physics, Engineering and Computer Science, University of Hertfordshire, UK
- School of Electronics, Electrical Engineering and Computer Science, Queen's University Belfast, UK

## Acknowledgments
This work was developed in collaboration with:
- Dr. Pouria Sarhadi (University of Hertfordshire)
- Prof. Wasif Naeem (Queen's University Belfast)
- Klinsmann Agyei (University of Hertfordshire)

## License
MIT License

Copyright (c) 2025 Dr Pouria Sarhadi, Prof. Wasif Naeem, Klinsmann Agyei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact
- Dr. Pouria Sarhadi - p.sarhadi@herts.ac.uk
- Prof. Wasif Naeem - w.naeem@ee.qub.ac.uk
- Klinsmann Agyei - k.agyei@herts.ac.uk

## Citation
If you use CORALL in your research, please cite:
```
[Citation details will be added after publication]
```
