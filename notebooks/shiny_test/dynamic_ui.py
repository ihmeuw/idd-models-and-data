from shiny import ui
from ui_components import create_parameter_input

def create_dynamic_sliders_2(option, current_values):
    """Create dynamic sliders based on model selection"""
    
    if option == "SIR":
        return ui.div(
            create_parameter_input("p2_i_0", "Percent infectious at t=0", 0, 10, current_values['i_0'], add_percent=True),
            create_parameter_input("p2_beta", "beta", 0.1, 10, current_values['beta']),
            create_parameter_input("p2_gamma", "gamma", 0, 10, current_values['gamma'])
        )
    elif option == "SEIR":
        return ui.div(
            create_parameter_input("p2_i_0", "Percent infectious at t=0", 0, 10, current_values['i_0'], add_percent=True),
            create_parameter_input("p2_beta", "beta", 0.1, 10, current_values['beta']),
            create_parameter_input("p2_sigma", "sigma", 0.1, 10, current_values['sigma']),
            create_parameter_input("p2_gamma", "gamma", 0, 10, current_values['gamma'])
        )
    elif option == "SEIRS":
        return ui.div(
            create_parameter_input("p2_i_0", "Percent infectious at t=0", 0, 10, current_values['i_0'], add_percent=True),
            create_parameter_input("p2_beta", "beta", 0.1, 10, current_values['beta']),
            create_parameter_input("p2_sigma", "sigma", 0.1, 10, current_values['sigma']),
            create_parameter_input("p2_gamma", "gamma", 0, 10, current_values['gamma']),
            create_parameter_input("p2_aa", "Average Age (1/mu)", 0, 10, current_values['aa'])
        )
    
def create_dynamic_sliders_3(option, current_values):
    """Create dynamic sliders based on model selection"""
    
    if option == "SIR: Differential Eqns":
        return ui.div(
            create_parameter_input("p3_i_0", "Percent infectious at t=0", 0, 10, current_values['i_0'], add_percent=True),
            create_parameter_input("p3_beta", "beta", 0.1, 10, current_values['beta']),
            create_parameter_input("p3_gamma", "gamma", 0, 10, current_values['gamma'])
        )
    elif option == "SIR: Difference Eqns":
        return ui.div(
            create_parameter_input("p3_i_0", "Percent infectious at t=0", 0, 10, current_values['i_0'], add_percent=True),
            create_parameter_input("p3_beta", "beta", 0.1, 10, current_values['beta']),
            create_parameter_input("p3_sigma", "sigma", 0.1, 10, current_values['sigma']),
            create_parameter_input("p3_N", "N", 50, 500, current_values['N'])
        )
    elif option == "SIR: Stochastic Diff. Eqns":
        return ui.div(
            create_parameter_input("p3_i_0", "Percent infectious at t=0", 0, 10, current_values['i_0'], add_percent=True),
            create_parameter_input("p3_beta", "beta", 0.1, 10, current_values['beta']),
            create_parameter_input("p3_gamma", "gamma", 0, 10, current_values['gamma']),
            create_parameter_input("p3_N", "N", 50, 500, current_values['N']),
            create_parameter_input("p3_sim_n", "Number of simulations", 5, 50, current_values['sim_n'])
        )