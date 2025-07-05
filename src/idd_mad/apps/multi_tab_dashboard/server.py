"""Server logic for multi-tab dashboard application."""

from shiny import reactive, render, ui
import numpy as np
from ...utils.calculations import ModelCalculator
from ...visualization.plotting import create_epidemiology_figure, create_multi_panel_figure
from ...ui.components import model_parameter_set


def create_server(input, output, session):
    """Create server function for multi-tab dashboard app."""
    
    # Create reactive values to store parameter values globally
    param_values = reactive.Value({
        'i_0': 1,
        'beta': 1, 
        'gamma': 1,
        'sigma': 1,
        'aa': 70
    })
    
    # Page 1 sync functions
    @reactive.effect
    def sync_p1_i0():
        try:
            if hasattr(input, 'p1_i_0') and input.p1_i_0() is not None:
                ui.update_numeric("p1_i_0_num", value=input.p1_i_0())
        except:
            pass

    @reactive.effect  
    def sync_p1_i0_num():
        try:
            if hasattr(input, 'p1_i_0_num') and input.p1_i_0_num() is not None:
                ui.update_slider("p1_i_0", value=input.p1_i_0_num())
        except:
            pass
        
    @reactive.effect
    def sync_p1_beta():
        try:
            if hasattr(input, 'p1_beta') and input.p1_beta() is not None:
                ui.update_numeric("p1_beta_num", value=input.p1_beta())
        except:
            pass

    @reactive.effect  
    def sync_p1_beta_num():
        try:
            if hasattr(input, 'p1_beta_num') and input.p1_beta_num() is not None:
                ui.update_slider("p1_beta", value=input.p1_beta_num())
        except:
            pass

    @reactive.effect
    def sync_p1_gamma():
        try:
            if hasattr(input, 'p1_gamma') and input.p1_gamma() is not None:
                ui.update_numeric("p1_gamma_num", value=input.p1_gamma())
        except:
            pass

    @reactive.effect  
    def sync_p1_gamma_num():
        try:
            if hasattr(input, 'p1_gamma_num') and input.p1_gamma_num() is not None:
                ui.update_slider("p1_gamma", value=input.p1_gamma_num())
        except:
            pass
    
    # Page 2 sync functions
    @reactive.effect
    def sync_p2_i0():
        try:
            if hasattr(input, 'p2_i_0') and input.p2_i_0() is not None:
                ui.update_numeric("p2_i_0_num", value=input.p2_i_0())
        except:
            pass

    @reactive.effect  
    def sync_p2_i0_num():
        try:
            if hasattr(input, 'p2_i_0_num') and input.p2_i_0_num() is not None:
                ui.update_slider("p2_i_0", value=input.p2_i_0_num())
        except:
            pass
        
    @reactive.effect
    def sync_p2_beta():
        try:
            if hasattr(input, 'p2_beta') and input.p2_beta() is not None:
                ui.update_numeric("p2_beta_num", value=input.p2_beta())
        except:
            pass

    @reactive.effect  
    def sync_p2_beta_num():
        try:
            if hasattr(input, 'p2_beta_num') and input.p2_beta_num() is not None:
                ui.update_slider("p2_beta", value=input.p2_beta_num())
        except:
            pass

    @reactive.effect
    def sync_p2_gamma():
        try:
            if hasattr(input, 'p2_gamma') and input.p2_gamma() is not None:
                ui.update_numeric("p2_gamma_num", value=input.p2_gamma())
        except:
            pass

    @reactive.effect  
    def sync_p2_gamma_num():
        try:
            if hasattr(input, 'p2_gamma_num') and input.p2_gamma_num() is not None:
                ui.update_slider("p2_gamma", value=input.p2_gamma_num())
        except:
            pass
            
    @reactive.effect
    def sync_p2_sigma():
        try:
            if hasattr(input, 'p2_sigma') and input.p2_sigma() is not None:
                ui.update_numeric("p2_sigma_num", value=input.p2_sigma())
        except:
            pass

    @reactive.effect  
    def sync_p2_sigma_num():
        try:
            if hasattr(input, 'p2_sigma_num') and input.p2_sigma_num() is not None:
                ui.update_slider("p2_sigma", value=input.p2_sigma_num())
        except:
            pass
            
    @reactive.effect
    def sync_p2_aa():
        try:
            if hasattr(input, 'p2_aa') and input.p2_aa() is not None:
                ui.update_numeric("p2_aa_num", value=input.p2_aa())
        except:
            pass

    @reactive.effect  
    def sync_p2_aa_num():
        try:
            if hasattr(input, 'p2_aa_num') and input.p2_aa_num() is not None:
                ui.update_slider("p2_aa", value=input.p2_aa_num())
        except:
            pass
    
    # Update global parameters when Page 2 inputs change
    @reactive.effect
    def update_global_params_from_p2():
        try:
            current = param_values.get()
            updated = False
            
            if hasattr(input, 'p2_i_0') and input.p2_i_0() is not None and current['i_0'] != input.p2_i_0():
                current['i_0'] = input.p2_i_0()
                updated = True
            if hasattr(input, 'p2_beta') and input.p2_beta() is not None and current['beta'] != input.p2_beta():
                current['beta'] = input.p2_beta()
                updated = True
            if hasattr(input, 'p2_gamma') and input.p2_gamma() is not None and current['gamma'] != input.p2_gamma():
                current['gamma'] = input.p2_gamma()
                updated = True
            if hasattr(input, 'p2_sigma') and input.p2_sigma() is not None and current['sigma'] != input.p2_sigma():
                current['sigma'] = input.p2_sigma()
                updated = True
            if hasattr(input, 'p2_aa') and input.p2_aa() is not None and current['aa'] != input.p2_aa():
                current['aa'] = input.p2_aa()
                updated = True
                
            if updated:
                param_values.set(current)
        except:
            pass
    
    # Reactive effect to sync Page 2 sliders when model changes
    @reactive.effect
    def sync_page2_on_model_change():
        # Trigger when dropdown changes
        model_type = input.dropdown2_1()
        if model_type is not None:
            current = param_values.get()
            # Give UI time to render new sliders, then update them
            import time
            time.sleep(0.1)  # Small delay to let UI render
            try:
                ui.update_slider("p2_i_0", value=current['i_0'])
                ui.update_slider("p2_beta", value=current['beta'])
                ui.update_slider("p2_gamma", value=current['gamma'])
                if model_type.upper() in ['SEIR', 'SEIRS']:
                    ui.update_slider("p2_sigma", value=current['sigma'])
                if model_type.upper() == 'SEIRS':
                    ui.update_slider("p2_aa", value=current['aa'])
            except:
                pass
    
    # Page 1 Plot - Basic SIR
    @output
    @render.plot
    @reactive.event(input.update_plot1)
    def plot1():
        # Get parameter values and update global params
        i_0 = input.p1_i_0() if input.p1_i_0() is not None else 1
        beta = input.p1_beta() if input.p1_beta() is not None else 1
        gamma = input.p1_gamma() if input.p1_gamma() is not None else 1
        dt = input.p1_dt() if input.p1_dt() is not None else 0.01
        
        # Update global parameter values
        current_params = param_values.get()
        current_params.update({
            'i_0': i_0,
            'beta': beta,
            'gamma': gamma
        })
        param_values.set(current_params)
        
        # Calculate model data
        data = ModelCalculator.calculate_sir_data(
            i_0_percent=i_0,
            beta=beta,
            gamma=gamma,
            dt=dt
        )
        
        # Create and return the figure
        return create_epidemiology_figure(
            df=data['model_df'],
            model_type=data['model_type'],
            title=data['title1']
        )
    
    # Dynamic UI for Page 2 model-specific parameters
    @output
    @render.ui
    def dynamic_sliders2():
        try:
            model_type = input.dropdown2_1()
            if model_type is None:
                model_type = "SIR"
            
            # Get current global parameter values
            current_values = param_values.get()
            
            # Create the parameter set for the selected model
            return model_parameter_set(model_type, current_values, "p2")
            
        except (AttributeError, TypeError):
            return model_parameter_set("SIR", param_values.get(), "p2")
    
    # Page 2 Plot - Model Comparison
    @output
    @render.plot
    @reactive.event(input.update_plot2)
    def plot2():
        # Get model type
        model_type = input.dropdown2_1() if input.dropdown2_1() is not None else "SIR"
        
        # Get parameter values from Page 2 inputs, with fallbacks
        current_params = param_values.get()
        
        try:
            i_0 = input.p2_i_0() if hasattr(input, 'p2_i_0') and input.p2_i_0() is not None else current_params['i_0']
            beta = input.p2_beta() if hasattr(input, 'p2_beta') and input.p2_beta() is not None else current_params['beta']
            gamma = input.p2_gamma() if hasattr(input, 'p2_gamma') and input.p2_gamma() is not None else current_params['gamma']
            sigma = input.p2_sigma() if hasattr(input, 'p2_sigma') and input.p2_sigma() is not None else current_params['sigma']
            aa = input.p2_aa() if hasattr(input, 'p2_aa') and input.p2_aa() is not None else current_params['aa']
        except:
            # Fall back to stored parameter values
            i_0 = current_params['i_0']
            beta = current_params['beta']
            gamma = current_params['gamma']
            sigma = current_params['sigma']
            aa = current_params['aa']
        
        # Update global parameters with current Page 2 values
        current_params.update({
            'i_0': i_0,
            'beta': beta,
            'gamma': gamma,
            'sigma': sigma,
            'aa': aa
        })
        param_values.set(current_params)
        
        # Calculate model data
        data = ModelCalculator.calculate_model_data(
            model_type=model_type,
            i_0_percent=i_0,
            beta=beta,
            gamma=gamma,
            sigma=sigma,
            average_age=aa
        )
        
        # Create and return the figure
        return create_epidemiology_figure(
            df=data['model_df'],
            model_type=data['model_type'],
            title=data['title1']
        )
    
    # Page 3 Plot - Multi-panel Complex Analysis
    @output
    @render.plot
    @reactive.event(input.update_plot3)
    def plot3():
        # Get dropdown values
        choice1 = input.dropdown3_1() if input.dropdown3_1() is not None else "Choice 1"
        choice2 = input.dropdown3_2() if input.dropdown3_2() is not None else "Type X"
        
        # Get slider values
        slider1 = input.slider3_1() if input.slider3_1() is not None else 10
        slider2 = input.slider3_2() if input.slider3_2() is not None else 90
        slider3 = input.slider3_3() if input.slider3_3() is not None else 45
        slider4 = input.slider3_4() if input.slider3_4() is not None else 75
        slider5 = input.slider3_5() if input.slider3_5() is not None else 35
        
        # Calculate multipliers based on choices
        choice1_mult = {"Choice 1": 1, "Choice 2": 1.5, "Choice 3": 2, "Choice 4": 2.5}[choice1]
        choice2_mult = {"Type X": 0.5, "Type Y": 1, "Type Z": 1.5}[choice2]
        
        # Generate x data
        x = np.linspace(0, 10, 100)
        
        # Calculate y values for each panel
        y1 = np.sin(x * choice1_mult) * slider1 / 50
        y2 = np.cos(x * choice2_mult) * slider2 / 50
        y3 = (np.sin(x * slider3 / 10) * slider4 / 50 + 
              np.cos(x * slider5 / 10) * choice1_mult * choice2_mult)
        
        # Create multi-panel data
        panel_data = {
            'panel1': {
                'x': x,
                'y': y1,
                'title': f"Panel 1: {choice1}",
                'color': '#377eb8',  # Blue
                'type': 'line',
                'xlim': [0, 10],
                'ylim': [-2.5, 2.5]
            },
            'panel2': {
                'x': x,
                'y': y2, 
                'title': f"Panel 2: {choice2}",
                'color': '#e41a1c',  # Red
                'type': 'line',
                'xlim': [0, 10],
                'ylim': [-2.5, 2.5]
            },
            'panel3': {
                'x': x,
                'y': y3,
                'title': "Panel 3: Combined Analysis",
                'color': '#4daf4a',  # Green
                'type': 'fill',
                'xlim': [0, 10],
                'ylim': [-8, 8]
            }
        }
        
        return create_multi_panel_figure(panel_data, figsize=(12, 8))
