from shiny import render, reactive
from calculations import calculate_plot1_data, calculate_plot2_data, calculate_plot3_data
from plotting_functions import create_plot1, create_plot2, create_plot3

def safe_input(input, input_id, default=0):
    """Safely get input value with default"""
    try:
        return input[input_id]()
    except:
        return default

def create_plot_functions(input, output):
    """Create all plot functions"""
    
    @output
    @render.plot
    @reactive.event(input.update_plot1)
    def plot1():
        """Simple 2x1 plot for Page 1"""
        data = calculate_plot1_data(
            input.p1_i_0(), 
            input.p1_beta(), 
            input.p1_gamma(), 
            input.p1_dt()
        )
        return create_plot1(data)

    @output
    @render.plot
    @reactive.event(input.update_plot2)
    def plot2():
        """Simple 2x1 plot for Page 2"""
        model_type = input.dropdown2_1()
        
        data = calculate_plot2_data(
            model_type,
            safe_input(input, "p2_i_0", 1),
            safe_input(input, "p2_beta", 1),
            safe_input(input, "p2_gamma", 1),
            safe_input(input, "p2_sigma", 1),
            safe_input(input, "p2_aa", 1),
        )
        return create_plot2(data)
        
    @output
    @render.plot
    @reactive.event(input.update_plot3)
    def plot3():
        """Multi-panel figure"""
        data = calculate_plot3_data(
            input.dropdown3_1(),
            input.dropdown3_2(),
            input.slider3_1(),
            input.slider3_2(),
            input.slider3_3(),
            input.slider3_4(),
            input.slider3_5()
        )
        return create_plot3(data)