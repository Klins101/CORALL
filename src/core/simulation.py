import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import argparse
import os
from pathlib import Path
from src.navigation.planning import waypoint_selection, planning
from src.dynamics.vessel_dynamics import vessel_dynamics
from src.core.integration import integration
from src.navigation.obstacle_sim import obstacle_sim
from src.risk_assessment.cpa_calculations import cpa_calculations
from src.risk_assessment.cpa_calculations_0speed import cpa_calculations_0speed
from src.dynamics.controller import controller
from src.dynamics.actuator_modeling import actuator_modeling
from src.risk_assessment.risk_calculations import risk_calculations
from src.navigation.reactive_avoidance import reactive_avoidance
from src.visualization.animate import animate_step
from src.utils.imazu_cases import get_obstacles, nautical_to_meters, obstacle_cases, get_obstacle_data
import matplotlib.ticker as ticker
# Optional LLM imports
try:
    from src.decision_making.multi_llm_decision import COLREGSInterpreter, VesselState
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    COLREGSInterpreter = None
    VesselState = None
from typing import List, Union, Optional

def extract_kdir_from_response(response: str) -> int:
    """
    Extract K_dir from LLM response
    Returns:
        +1 for "turn starboard"
        -1 for "turn port"
        0 for "stand on" or default
    """
    response_lower = response.lower()
    
    if "turn starboard" in response_lower or "alter course to starboard" in response_lower or "starboard" in response_lower:
        return 1
    elif "turn port" in response_lower or "alter course to port" in response_lower or "port" in response_lower:
        return -1
    else:  # "stand on" or any other action
        return 0

def run_colm(risk: Union[float, List[float], np.ndarray],
            distance: Union[float, List[float], np.ndarray],
            bearing: Union[float, List[float], np.ndarray],
            dcpa: Union[float, List[float], np.ndarray],
            tcpa: Union[float, List[float], np.ndarray],
            time_idx: int = 0,
            provider: str = None) -> str:
    """
    Run COLM decision making for any number of vessels.
    
    Args:
        risk: Risk value(s) for vessel(s)
        distance: Distance(s) to vessel(s) in nautical miles
        bearing: Relative bearing(s) to vessel(s) in degrees
        dcpa: Distance at Closest Point of Approach in nautical miles
        tcpa: Time to Closest Point of Approach in minutes
        time_idx: Current time index (default: 0)
    
    Returns:
        str: COLREGs decision with explanation
    """
    if not LLM_AVAILABLE:
        return "LLM not available - using default behavior"
    
    # Convert inputs to numpy arrays if they aren't already
    risk = np.atleast_1d(risk)
    distance = np.atleast_1d(distance)
    bearing = np.atleast_1d(bearing)
    dcpa = np.atleast_1d(dcpa)
    tcpa = np.atleast_1d(tcpa)
    
    # Create interpreter instance with specified provider
    interpreter = COLREGSInterpreter(provider=provider)
    
    # Create vessel states
    vessels = [
        VesselState(float(r), float(d), float(b), float(dc), float(tc))
        for r, d, b, dc, tc in zip(risk, distance, bearing, dcpa, tcpa)
    ]
    
    # Get decision
    return interpreter.make_decision(vessels, time_idx)

def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_file = Path(__file__).parent.parent.parent / '.env'
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value

def parse_args():
    parser = argparse.ArgumentParser(description='Marine Vehicle Simulation')
    parser.add_argument('--case_number', type=int, default=1, help='Simulation case number')
    parser.add_argument('--sim_time', type=float, default=450.0, help='Simulation time in seconds')
    parser.add_argument('--dt', type=float, default=0.1, help='Time step size')
    parser.add_argument('--no_animation', action='store_true', help='Disable animation')
    parser.add_argument('--output_dir', type=str, default='img/', help='Output directory for results')
    parser.add_argument('--llm', type=int, default=0, help='Use LLM for decision making (0=off, 1=on)')
    parser.add_argument('--llm_provider', type=str, default=None, 
                       help='LLM provider to use (openai, claude). If not specified, uses LLM_PROVIDER from .env')
    parser.add_argument('--compare', action='store_true', 
                       help='Run comparison between LLM and baseline simulation')
    return parser.parse_args()

def run_simulation(args=None, return_data=False):
    # Load environment variables from .env file if it exists
    load_env_file()
    
    # Parse command line arguments if not provided
    if args is None:
        args = parse_args()
    
    # Check if comparison mode is requested (only if not called from comparison)
    if args.compare and not return_data:
        from src.core.comparison_simulation import run_comparison_simulation
        return run_comparison_simulation(args)
    
    # Initialize parameters
    t = 0.0  # initial time
    dt = args.dt  # time step
    Ts = dt  # sampling time
    N = round(args.sim_time / dt)
    Animation = not args.no_animation

    # Initial conditions
    x_v, y_v, psi_v = 0.0, 0.0, np.radians(0)  # initial position and heading
    r_v, b_v, u_v = 0.0, 0.0, 0.0  # initial rates and velocity
    ui_psi1 = 0.0  # initial integral of yaw error

    X_0 = np.array([x_v, y_v, psi_v, r_v, b_v, u_v])
    X = X_0.copy()

    Sat_amp_s = 20
    i = 0

    # Waypoints
    Xwpt = [0, nautical_to_meters(40)/1852]
    Ywpt = [0, 0]
    i_wpt = 1

    # Vessel parameters
    LOA_own, BOL_own = 30, 16
    CPA_own = LOA_own * 2
    
    # Get obstacle data
    Xob, Yob, Vob, psiob = get_obstacle_data(args.case_number)
    LOA_ob = [80] * len(Xob)
    BOL_ob = [30] * len(Xob)
    CPA_ob = [LOA_ob[0] * 1] * len(Xob)

    # Initialize arrays
    time = []
    Kdir = np.ones(N)  # Initialize Kdir array
    x, y, psi = np.zeros(N), np.zeros(N), np.zeros(N)
    r, b, u = np.zeros(N), np.zeros(N), np.zeros(N)
    v_c = np.zeros(N)
    u_p, tau_c, tau_ac = np.zeros(N), np.zeros(N), np.zeros(N)
    psi_p, psi_wp, psi_oa = np.zeros(N), np.zeros(N), np.zeros(N)
    V_x, V_y = np.zeros(N), np.zeros(N)
    x_nmi, y_nmi = np.zeros(N), np.zeros(N)  # Add nautical mile arrays
    # i_wpt is already initialized above as 1
    
    Xobs, Yobs, Vxobs, Vyobs = (np.zeros((N, len(Xob))) for _ in range(4))
    DCPA, TCPA, Vrel, alpha, psi_Vrel = (np.zeros((N, len(Xob))) for i in range(5))
    DCPA[:1], TCPA[:1] = 1000, 1000
    DCPA2, TCPA2, Vrel2, alpha2, psi_Vrel2 = (np.zeros((N, len(Xob))) for _ in range(5))
    Distance_ob, Bearing_ob, Risk = (np.zeros((N, len(Xob))) for _ in range(3))

    # Prepare for animation if enabled
    if Animation:
        fig, ax = plt.subplots()
        plt.plot(Xwpt, Ywpt, 'ob', Xwpt, Ywpt, ':b', linewidth=1.0)
        plt.grid(True)
        writer = animation.PillowWriter(fps=5)

    # Main simulation loop
    if Animation:
        with writer.saving(fig, f"{args.output_dir}/scenario_animation{args.case_number}.gif", dpi=200):
            for i in range(len(x)):
                # Record current state
                time.append(t)
                x[i] = X[0]
                y[i] = X[1]
                psi[i] = X[2]
                r[i] = X[3]
                b[i] = X[4]
                u[i] = X[5]
                X_0 = X.copy()

                # Speed command
                u_p[i] = 43.3

                # Convert to nautical miles
                METERS_TO_NMI = (1 / 1852)
                x_nmi = [xi * METERS_TO_NMI for xi in x]
                y_nmi = [yi * METERS_TO_NMI for yi in y]
                Xob_nmi = [xo * METERS_TO_NMI for xo in Xob]
                Yob_nmi = [yo * METERS_TO_NMI for yo in Yob]
                LOA_own_nmi = LOA_own * METERS_TO_NMI
                BOL_own_nmi = BOL_own * METERS_TO_NMI
                LOA_ob_nmi = [loa * METERS_TO_NMI for loa in LOA_ob]
                BOL_ob_nmi = [bol * METERS_TO_NMI for bol in BOL_ob]

                # Path planning and collision avoidance
                i_wpt = waypoint_selection(Xwpt, Ywpt, x_nmi[i], y_nmi[i], i_wpt)
                psi_wp[i] = planning(Xwpt, Ywpt, x_nmi[i], y_nmi[i], i_wpt)
                psi_oa[i], w_B, w_R, Distance_ob[i, :], Bearing_ob[i, :] = reactive_avoidance(
                    Xob_nmi, Yob_nmi, x_nmi[i], y_nmi[i], psi[i], t)
                


                # extract_kdir_from_response function moved to global scope
                

                # Run COLM decision making (function moved to global scope)

                # Overall yaw command with Kdir
                psi_p[i] = psi_wp[i] + Kdir[i] * psi_oa[i]

                # Controller and actuator
                tau_c[i], v_c[i], ui_psi1 = controller(
                    psi_p[i], psi[i], r[i], u_p[i], b, ui_psi1, Ts)
                tau_ac[i] = actuator_modeling(tau_c[i], Sat_amp_s)
                
                # System dynamics
                inputs = [tau_ac[i], v_c[i]]
                X_dot = vessel_dynamics(X_0, inputs)
                X = integration(X_0, X_dot, dt)
                V_x[i] = X_dot[0]
                V_y[i] = X_dot[1]

                # Obstacles simulation
                Xob, Yob, Vxob, Vyob = obstacle_sim(Xob, Yob, Vob, psiob, dt)
                Xobs[i, :] = Xob
                Yobs[i, :] = Yob
                Vxobs[i, :] = Vxob
                Vyobs[i, :] = Vyob

                # Risk analysis
                for j in range(len(Xob)):
                    if i >= 1:
                        Distance_ob[i, j] = np.sqrt(
                            (np.array(Xobs[i, j]) - x[i])**2 + 
                            (np.array(Yobs[i, j]) - y[i])**2)
                        
                        DCPA[i, j], TCPA[i, j], Vrel[i, j], alpha[i, j], psi_Vrel[i, j] = cpa_calculations(
                            x[i], y[i], x[i-1], y[i-1], Xobs[i, j], Yobs[i, j], 
                            Xobs[i-1, j], Yobs[i-1, j], Ts
                        )

                        DCPA2[i, j], TCPA2[i, j], Vrel2[i, j], alpha2[i, j], psi_Vrel2[i, j] = cpa_calculations_0speed(
                            x[i], y[i], Xobs[i, j], Yobs[i, j], V_x[i], V_y[i], 
                            Vxobs[i, j], Vyobs[i, j], Distance_ob[i, j]
                        )

                    Risk[i, j] = risk_calculations(
                        DCPA[i, j], TCPA[i, j], Distance_ob[i, j], Vrel[i, j])

                if args.llm == 1:
                    if not LLM_AVAILABLE:
                        if i == 0:  # Print warning only once
                            print("Warning: LLM requested but langchain_openai not available. Running without LLM.")
                    else:
                        if i % 200 == 0:
                            decision = run_colm(
                                Risk[i, :],
                                Distance_ob[i, :],
                                Bearing_ob[i, :],
                                DCPA[i, :],
                                TCPA[i, :],
                                provider=args.llm_provider
                            )
                            print(f"\nStep {i}: COLM Decision:")
                            print(decision)
                            print(f"Risk: {Risk[i, :]}")
                            
                            new_kdir = extract_kdir_from_response(decision)
                            Kdir[i] = new_kdir
                            #print(f"Extracted Kdir value: {new_kdir}")
                        elif i > 0:
                            pass
                            #Kdir[i] = Kdir[i-1]  # Maintain previous value between updates
                        
               

                # Animation
                l = len(Risk[i, :])
                animate_step(
                    x_nmi[i], y_nmi[i], psi[i],
                    LOA_own_nmi, BOL_own_nmi, CPA_own,
                    Xob_nmi, Yob_nmi, psiob,
                    LOA_ob_nmi, BOL_ob_nmi, CPA_ob,
                    Risk[i, :], Vob, i, l
                )
                
                if i % 101 == 0 and i != 0:
                    writer.grab_frame()

                t += dt

            # Save animation plots
            plt.title(f'Case {args.case_number}', fontsize=25)
            plt.savefig(f'{args.output_dir}/simulation_result{args.case_number}.eps', format='eps')
            plt.savefig(f'{args.output_dir}/simulation_result{args.case_number}.png')
            plt.show(block=True)
    else:
        # Run simulation without animation
        for i in range(len(x)):
            # Record current state
            time.append(t)
            x[i] = X[0]
            y[i] = X[1]
            psi[i] = X[2]
            r[i] = X[3]
            b[i] = X[4]
            u[i] = X[5]

            # Convert to nautical miles
            x_nmi[i] = x[i] / 1852
            y_nmi[i] = y[i] / 1852

            # Speed command
            u_p[i] = 43.3

            # Convert to nautical miles
            METERS_TO_NMI = (1 / 1852)
            x_nmi = [xi * METERS_TO_NMI for xi in x]
            y_nmi = [yi * METERS_TO_NMI for yi in y]
            Xob_nmi = [xo * METERS_TO_NMI for xo in Xob]
            Yob_nmi = [yo * METERS_TO_NMI for yo in Yob]
            LOA_own_nmi = LOA_own * METERS_TO_NMI
            BOL_own_nmi = BOL_own * METERS_TO_NMI
            LOA_ob_nmi = [loa * METERS_TO_NMI for loa in LOA_ob]
            BOL_ob_nmi = [bol * METERS_TO_NMI for bol in BOL_ob]

            # Path planning and collision avoidance
            i_wpt = waypoint_selection(Xwpt, Ywpt, x_nmi[i], y_nmi[i], i_wpt)
            psi_wp[i] = planning(Xwpt, Ywpt, x_nmi[i], y_nmi[i], i_wpt)
            psi_oa[i], w_B, w_R, Distance_ob[i, :], Bearing_ob[i, :] = reactive_avoidance(
                Xob_nmi, Yob_nmi, x_nmi[i], y_nmi[i], psi[i], t)

            # Overall yaw command with Kdir
            psi_p[i] = psi_wp[i] + Kdir[i] * psi_oa[i]

            # Controller and actuator
            tau_c[i], v_c[i], ui_psi1 = controller(
                psi_p[i], psi[i], r[i], u_p[i], b, ui_psi1, Ts)
            tau_ac[i] = actuator_modeling(tau_c[i], Sat_amp_s)

            # Store current state
            X_0 = X.copy()
            
            # System dynamics
            inputs = [tau_ac[i], v_c[i]]
            X_dot = vessel_dynamics(X_0, inputs)
            X = integration(X_0, X_dot, dt)
            V_x[i] = X_dot[0]
            V_y[i] = X_dot[1]

            # Obstacles simulation
            Xob, Yob, Vxob, Vyob = obstacle_sim(Xob, Yob, Vob, psiob, dt)
            Xobs[i, :] = Xob
            Yobs[i, :] = Yob
            Vxobs[i, :] = Vxob
            Vyobs[i, :] = Vyob

            # Risk analysis
            for j in range(len(Xob)):
                if i >= 1:
                    Distance_ob[i, j] = np.sqrt(
                        (np.array(Xobs[i, j]) - x[i])**2 + 
                        (np.array(Yobs[i, j]) - y[i])**2)
                    
                    DCPA[i, j], TCPA[i, j], Vrel[i, j], alpha[i, j], psi_Vrel[i, j] = cpa_calculations(
                        x[i], y[i], x[i-1], y[i-1], Xobs[i, j], Yobs[i, j], 
                        Xobs[i-1, j], Yobs[i-1, j], Ts
                    )

                    DCPA2[i, j], TCPA2[i, j], Vrel2[i, j], alpha2[i, j], psi_Vrel2[i, j] = cpa_calculations_0speed(
                        x[i], y[i], Xobs[i, j], Yobs[i, j], V_x[i], V_y[i], 
                        Vxobs[i, j], Vyobs[i, j], Distance_ob[i, j]
                    )

                    Risk[i, j] = risk_calculations(
                        DCPA[i, j], TCPA[i, j], Distance_ob[i, j], Vrel[i, j])

            if args.llm == 1:
                if not LLM_AVAILABLE:
                    if i == 0:  # Print warning only once
                        print("Warning: LLM requested but langchain_openai not available. Running without LLM.")
                else:
                    if i % 200 == 0:
                        decision = run_colm(
                            Risk[i, :],
                            Distance_ob[i, :],
                            Bearing_ob[i, :],
                            DCPA[i, :],
                            TCPA[i, :],
                            provider=args.llm_provider
                        )
                     
                        print(decision)
                        
                        new_kdir = extract_kdir_from_response(decision)
                        Kdir[i] = new_kdir
                    elif i > 0:
                        pass

            t += dt

    #print(Kdir)
    # Plot DCPA, TCPA, Risk plots
    fig, axs = plt.subplots(2, 2)
    for i in range(len(Xob)):
        axs[0, 0].plot(time, DCPA[:, i] / 1852, linewidth=1.0)
        axs[0, 1].plot(time, Distance_ob[:, i]/1852, linewidth=1.0)
        axs[1, 0].plot(time, TCPA[:, i], linewidth=1.0, label=f'TS{i+1}')
        axs[1, 1].plot(time, Risk[:, i], linewidth=1.0)

    # Configure plots
    axs[0, 0].set_xlim([0, args.sim_time])
    axs[0, 0].set_ylabel(r'$DCPA$ (nmi)', fontsize=20)
    axs[0, 0].tick_params(axis='both', labelsize=15)

    axs[0, 1].set_xlim([0, args.sim_time])
    axs[0, 1].set_ylim([0, 2000/1852])
    axs[0, 1].set_ylabel(r'$R$ (nmi)', fontsize=20)
    axs[0, 1].tick_params(axis='both', labelsize=15)
    

    axs[1, 0].set_xlim([0, args.sim_time])
    axs[1, 0].set_xlabel('Time (s)', fontsize=20)
    axs[1, 0].set_ylabel(r'$TCPA$ (s)', fontsize=20)
    axs[1, 0].tick_params(axis='both', labelsize=15)
    axs[1, 0].legend()

    axs[1, 1].set_xlim([0, args.sim_time])
    axs[1, 1].set_ylim([0, 1])
    axs[1, 1].set_xlabel('Time (s)', fontsize=20)
    axs[1, 1].set_ylabel(r'$Risk$', fontsize=20)
    axs[1, 1].tick_params(axis='both', labelsize=15)

    fig.suptitle(f'Case {args.case_number}', fontsize=20)
    plt.tight_layout()
    plt.savefig(f'{args.output_dir}/plot_dcpa_tcpa_risk_{args.case_number}.eps', format='eps')
    plt.savefig(f'{args.output_dir}/plot_dcpa_tcpa_risk_{args.case_number}.png')
    plt.show()

    # Return data if requested (for comparison mode)
    if return_data:
        # Calculate Kdir for comparison based on actual control values
        # Kdir = 0 when Kdir[i] * psi_oa[i] == 0 (no turn)
        # Kdir = +1 when Kdir[i] * psi_oa[i] > 0 (starboard)
        # Kdir = -1 when Kdir[i] * psi_oa[i] < 0 (port)
        comparison_kdir = np.zeros(len(Kdir))
        for i in range(len(Kdir)):
            control_value = Kdir[i] * psi_oa[i]
            if control_value > 0:
                comparison_kdir[i] = 1  # Starboard
            elif control_value < 0:
                comparison_kdir[i] = -1  # Port
            else:
                comparison_kdir[i] = 0  # No turn
        
        return {
            'time': time,
            'x': x,
            'y': y,
            'psi': psi,
            'kdir': comparison_kdir,  # Use calculated comparison values
            'risk': Risk,
            'dcpa': DCPA,
            'tcpa': TCPA,
            'distance_ob': Distance_ob,
            'obstacles_x': Xobs[-1, :] if len(Xobs) > 0 else [],
            'obstacles_y': Yobs[-1, :] if len(Yobs) > 0 else [],
            'simulation_type': 'main_simulation'
        }

""""
    # Plot Kdir values
    plt.figure()
    plt.plot(time, Kdir, 'b', linewidth=1.5)
    plt.title(f'Case {args.case_number}')
    plt.xlabel('Time (s)')
    plt.ylabel(r'$K_{dir}$')
    plt.grid(True)
    plt.savefig(f'{args.output_dir}/plot_kdir_{args.case_number}.png', dpi=300)
    plt.show()"""

if __name__ == "__main__":
    run_simulation()