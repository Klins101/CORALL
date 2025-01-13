# COLM: COLREGs-Guided Risk-Aware LLM for Maritime Autonomous Navigation
COLM is a novel framework that integrates Large Language Models with real-time risk assessment for autonomous maritime navigation. The system combines LLM-based decision-making with traditional motion planning to enable COLREGs-compliant collision avoidance in autonomous surface vessels.

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
git clone https://github.com/Klins101/COLM.git
cd COLM
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

Copyright (c) 2024 Kwabena Agyei, Pouria Sarhadi, Wasif Naeem

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
- Dr. Wasif Naeem - w.naeem@qub.ac.uk
- Klinsmann Agyei - k.agyei@herts.ac.uk

## Citation
If you use COLM in your research, please cite:
```
[Citation details will be added after publication]
```
