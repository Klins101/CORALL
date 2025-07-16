# API Reference

## Core Modules

### `src.core.simulation`

#### `run_simulation()`
Main simulation entry point.

**Parameters:**
- Uses command-line arguments (see CLI Reference)

**Returns:**
- None (generates output files)

**Example:**
```python
from src.core.simulation import run_simulation
run_simulation()
```

#### `parse_args()`
Parse command-line arguments.

**Returns:**
- `argparse.Namespace`: Parsed arguments

---

### `src.dynamics.vessel_dynamics`

#### `vessel_dynamics(X, inputs)`
Calculate vessel dynamics.

**Parameters:**
- `X` (array): State vector [x, y, psi, r, beta, u]
- `inputs` (list): Control inputs [tau, v]

**Returns:**
- `array`: State derivatives

**Example:**
```python
from src.dynamics.vessel_dynamics import vessel_dynamics
X_dot = vessel_dynamics(X, [tau, v])
```

---

### `src.navigation.planning`

#### `waypoint_selection(Xwpt, Ywpt, x, y, i_wpt)`
Select next waypoint based on vessel position.

**Parameters:**
- `Xwpt` (array): X-coordinates of waypoints
- `Ywpt` (array): Y-coordinates of waypoints  
- `x` (float): Current x-position
- `y` (float): Current y-position
- `i_wpt` (int): Current waypoint index

**Returns:**
- `int`: Updated waypoint index

#### `planning(Xwpt, Ywpt, x, y, i_wpt)`
Calculate planned heading to waypoint.

**Parameters:**
- `Xwpt` (array): X-coordinates of waypoints
- `Ywpt` (array): Y-coordinates of waypoints
- `x` (float): Current x-position
- `y` (float): Current y-position
- `i_wpt` (int): Current waypoint index

**Returns:**
- `float`: Planned heading angle (radians)

---

### `src.risk_assessment.cpa_calculations`

#### `cpa_calculations(x1, y1, x1_prev, y1_prev, x2, y2, x2_prev, y2_prev, Ts)`
Calculate Closest Point of Approach (CPA) metrics.

**Parameters:**
- `x1, y1` (float): Current position of vessel 1
- `x1_prev, y1_prev` (float): Previous position of vessel 1
- `x2, y2` (float): Current position of vessel 2
- `x2_prev, y2_prev` (float): Previous position of vessel 2
- `Ts` (float): Time step

**Returns:**
- `tuple`: (DCPA, TCPA, Vrel, alpha, psi_Vrel)

---

### `src.risk_assessment.risk_calculations`

#### `risk_calculations(dcpa, tcpa, distance, v_rel)`
Calculate collision risk based on CPA metrics.

**Parameters:**
- `dcpa` (float): Distance at closest point of approach
- `tcpa` (float): Time to closest point of approach
- `distance` (float): Current distance to obstacle
- `v_rel` (float): Relative velocity

**Returns:**
- `float`: Risk value (0-1)

---

### `src.visualization.animate`

#### `animate_step(x, y, psi, LOA_own, BOL_own, CPA_own, Xob, Yob, psiob, LOA_ob, BOL_ob, CPA_ob, Risk, Vob, i, l)`
Create animation frame for current simulation step.

**Parameters:**
- `x, y` (float): Own vessel position
- `psi` (float): Own vessel heading
- `LOA_own, BOL_own` (float): Own vessel dimensions
- `CPA_own` (float): Own vessel CPA threshold
- `Xob, Yob` (arrays): Obstacle positions
- `psiob` (array): Obstacle headings
- `LOA_ob, BOL_ob` (arrays): Obstacle dimensions
- `CPA_ob` (array): Obstacle CPA thresholds
- `Risk` (array): Risk values
- `Vob` (array): Obstacle velocities
- `i` (int): Current step index
- `l` (int): Number of obstacles

**Returns:**
- None (updates plot)

---

## Utility Functions

### `src.utils.imazu_cases`

#### `get_obstacle_data(case_number)`
Get obstacle configuration for test cases.

**Parameters:**
- `case_number` (int): Test case number (1-15)

**Returns:**
- `tuple`: (Xob, Yob, Vob, psiob)

#### `nautical_to_meters(nautical_miles)`
Convert nautical miles to meters.

**Parameters:**
- `nautical_miles` (float): Distance in nautical miles

**Returns:**
- `float`: Distance in meters

---

## Constants

### Navigation
- `METERS_TO_NMI = 1/1852`: Conversion factor to nautical miles
- `Circ = 200/1852`: Waypoint threshold distance

### Vessel Parameters
- `LOA_own = 30`: Own vessel length overall (m)
- `BOL_own = 16`: Own vessel beam overall (m)
- `LOA_ob = 80`: Obstacle vessel length (m)
- `BOL_ob = 30`: Obstacle vessel beam (m)

### Control Parameters
- `Ts = 0.1`: Default sampling time (s)
- `Sat_amp_s = 20`: Saturation amplitude

## Error Handling

Most functions include basic error handling:
- Invalid array dimensions
- Division by zero in calculations
- File I/O errors for configuration

## Thread Safety

The simulation is not thread-safe. Run only one simulation at a time.