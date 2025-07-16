import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from typing import Dict, Any, Tuple, List
import copy

from src.core.simulation import run_simulation as _run_simulation
from src.visualization.comparison_plots import plot_kdir_comparison, create_comparison_summary
import io
import sys
from contextlib import redirect_stdout

def run_comparison_simulation(args) -> Dict[str, Any]:
    """
    Run both baseline and LLM simulations and create comparison plots.
    
    Args:
        args: Command line arguments
        
    Returns:
        Dict containing comparison results and statistics
    """
    
    print("🔄 Running Comparison Simulation...")
    print("=" * 50)
    
    # Store original args
    original_llm = args.llm
    original_animation = args.no_animation
    
    # Keep original animation setting
    
    print("Step 1: Running Baseline Simulation (No LLM)...")
    args.llm = 0  # Disable LLM for baseline
    baseline_results = _run_simulation(args, return_data=True)
    
    print("\n Step 2: Running LLM Simulation...")
    args.llm = 1  # Enable LLM
    llm_results = _run_simulation(args, return_data=True)
    
    print("\n Step 3: Creating Comparison Plots...")
    
    # Create Kdir comparison plot
    kdir_plot_path = plot_kdir_comparison(
        time_baseline=baseline_results['time'],
        kdir_baseline=baseline_results['kdir'],
        time_llm=llm_results['time'],
        kdir_llm=llm_results['kdir'],
        case_number=args.case_number,
        output_dir=args.output_dir,
        llm_provider=args.llm_provider or 'LLM'
    )
    
    # Calculate comparison statistics
    stats = calculate_comparison_stats(baseline_results, llm_results, args)
    
    # Create summary report
    summary_path = create_comparison_summary(
        baseline_stats=stats['baseline'],
        llm_stats=stats['llm'],
        case_number=args.case_number,
        output_dir=args.output_dir,
        llm_provider=args.llm_provider or 'LLM'
    )
    
    
    # Restore original args
    args.llm = original_llm
    args.no_animation = original_animation
    
    return {
        'baseline': baseline_results,
        'llm': llm_results,
        'stats': stats,
        'plots': {
            'kdir': kdir_plot_path,
            'summary': summary_path
        }
    }


def calculate_comparison_stats(baseline_results: Dict, llm_results: Dict, args) -> Dict[str, Dict]:
    """Calculate statistics for comparison between baseline and LLM simulations."""
    
    # Extract data
    kdir_baseline = baseline_results['kdir']
    kdir_llm = llm_results['kdir']
    risk_baseline = baseline_results['risk']
    risk_llm = llm_results['risk']
    
    # Calculate statistics
    baseline_stats = {
        'total_turns': np.sum(np.abs(kdir_baseline) > 0.1),
        'max_risk': np.max(risk_baseline),
        'avg_risk': np.mean(risk_baseline[risk_baseline > 0]),
        'final_distance': np.sqrt(baseline_results['x'][-1]**2 + baseline_results['y'][-1]**2) / 1852,
        'sim_time': args.sim_time
    }
    
    llm_stats = {
        'total_turns': np.sum(np.abs(kdir_llm) > 0.1),
        'max_risk': np.max(risk_llm),
        'avg_risk': np.mean(risk_llm[risk_llm > 0]),
        'final_distance': np.sqrt(llm_results['x'][-1]**2 + llm_results['y'][-1]**2) / 1852,
        'sim_time': args.sim_time
    }
    
    # Calculate agreement
    turn_agreement = np.mean(np.sign(kdir_baseline) == np.sign(kdir_llm))
    baseline_stats['turn_agreement'] = f"{turn_agreement:.1%}"
    
    # Path efficiency difference
    path_diff = ((llm_stats['final_distance'] - baseline_stats['final_distance']) / 
                 baseline_stats['final_distance'] * 100)
    baseline_stats['path_efficiency_diff'] = path_diff
    
    # Analysis
    if llm_stats['total_turns'] > baseline_stats['total_turns']:
        behavior = "more conservative (more turns)"
    elif llm_stats['total_turns'] < baseline_stats['total_turns']:
        behavior = "more aggressive (fewer turns)"
    else:
        behavior = "similar"
    
    baseline_stats['analysis'] = f"""
The LLM shows {behavior} navigation behavior compared to the baseline.
Risk management: {'Better' if llm_stats['max_risk'] < baseline_stats['max_risk'] else 'Similar' if abs(llm_stats['max_risk'] - baseline_stats['max_risk']) < 0.1 else 'More risky'}
Turn decisions agree {turn_agreement:.1%} of the time.
"""
    
    return {
        'baseline': baseline_stats,
        'llm': llm_stats
    }