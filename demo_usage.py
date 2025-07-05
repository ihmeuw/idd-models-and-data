"""Demo script showing how to use the reorganized epidemiological modeling package."""

import numpy as np
import matplotlib.pyplot as plt

# Import the package modules
from src.idd_mad.models.sir import run_sir_model, run_seir_model
from src.idd_mad.visualization.plotting import create_epidemiology_figure
from src.idd_mad.utils.calculations import ModelCalculator
from src.idd_mad.apps import run_app, list_apps


def demo_model_usage():
    """Demonstrate using the models directly."""
    print("=== Direct Model Usage Demo ===")
    
    # SIR model parameters
    parameters = {
        'beta': 0.3,
        'gamma': 0.1
    }
    
    # Run SIR model
    sir_result = run_sir_model(
        initial_infected=0.01,  # 1% initial infection
        parameters=parameters,
        dt=0.01,
        max_time=50.0
    )
    
    print(f"SIR model simulation completed with {len(sir_result)} time points")
    print(f"Peak infection: {sir_result['I'].max():.3f}")
    print(f"Final recovered: {sir_result['R'].iloc[-1]:.3f}")
    
    # SEIR model parameters
    seir_parameters = {
        'beta': 0.3,
        'sigma': 0.2,  # Incubation rate
        'gamma': 0.1
    }
    
    # Run SEIR model
    seir_result = run_seir_model(
        initial_infected=0.01,
        parameters=seir_parameters,
        dt=0.01,
        max_time=50.0
    )
    
    print(f"SEIR model simulation completed with {len(seir_result)} time points")
    print(f"Peak infection: {seir_result['I'].max():.3f}")
    
    return sir_result, seir_result


def demo_visualization():
    """Demonstrate the visualization functions."""
    print("\n=== Visualization Demo ===")
    
    # Calculate some model data
    data = ModelCalculator.calculate_sir_data(
        i_0_percent=1.0,
        beta=0.3,
        gamma=0.1
    )
    
    # Create a figure
    fig = create_epidemiology_figure(
        df=data['model_df'],
        model_type='SIR',
        title='Demo SIR Model'
    )
    
    print("Created SIR visualization")
    # plt.show()  # Uncomment to display the plot
    plt.close(fig)  # Close to prevent display in this demo


def demo_calculator():
    """Demonstrate the ModelCalculator utility."""
    print("\n=== ModelCalculator Demo ===")
    
    # Calculate SIR data
    sir_data = ModelCalculator.calculate_sir_data(
        i_0_percent=2.0,
        beta=0.4,
        gamma=0.15
    )
    
    print(f"SIR calculation: R0 = {ModelCalculator.get_basic_reproduction_number(0.4, 0.15):.2f}")
    print(f"Epidemic threshold exceeded: {ModelCalculator.get_epidemic_threshold(0.4, 0.15)}")
    
    # Calculate SEIR data
    seir_data = ModelCalculator.calculate_seir_data(
        i_0_percent=1.5,
        beta=0.35,
        sigma=0.25,
        gamma=0.12
    )
    
    print(f"SEIR model type: {seir_data['model_type']}")
    print(f"Peak infection in SEIR: {seir_data['model_df']['I'].max():.3f}")


def demo_apps():
    """Demonstrate the available Shiny apps."""
    print("\n=== Available Shiny Apps ===")
    
    apps = list_apps()
    print(f"Available apps: {apps}")
    
    print("\nTo run an app, use:")
    print("from src.idd_mad.apps import run_app")
    print("run_app('sir_demo')")
    print("run_app('model_comparison')")
    
    print("\nOr run directly:")
    print("python -m src.idd_mad.apps.sir_demo.app")


def main():
    """Run all demos."""
    print("Epidemiological Modeling Package Demo")
    print("=" * 40)
    
    try:
        # Run demos
        sir_result, seir_result = demo_model_usage()
        demo_visualization()
        demo_calculator()
        demo_apps()
        
        print("\n=== Demo completed successfully! ===")
        print("\nNext steps:")
        print("1. Run a Shiny app: python -m src.idd_mad.apps.sir_demo.app")
        print("2. Create your own epidemiological analysis")
        print("3. Add new models to the models module")
        print("4. Create custom visualizations")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        print("Make sure all dependencies are installed and the package is properly structured.")


if __name__ == "__main__":
    main()
