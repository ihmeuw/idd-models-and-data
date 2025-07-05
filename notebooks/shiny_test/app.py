from shiny import App, ui, render, reactive
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from ui_components import create_page1_ui, create_page2_ui, create_page3_ui, get_css_styles
from sync_functions import create_sync_functions
from dynamic_ui import create_dynamic_sliders_2, create_dynamic_sliders_3
from plot_handlers import create_plot_functions

# Define the UI
app_ui = ui.page_navbar(
    create_page1_ui(),
    create_page2_ui(),
    create_page3_ui(),
    title="Multi-Tab Dashboard",
    id="navbar",
    header=ui.tags.head(ui.tags.style(get_css_styles()))
)

# Define server logic
def server(input, output, session):
    # Create reactive values to store parameter values
    param_values = reactive.Value({
        'i_0': 1,
        'beta': 1, 
        'gamma': 1,
        'sigma': 1,
        'aa': 1
    })
    
    # Create all sync functions
    create_sync_functions(input, param_values)
    
    # Dynamic sliders for Page 2
    @output
    @render.ui
    def dynamic_sliders2():
        option = input.dropdown2_1()
        current_values = param_values.get()
        return create_dynamic_sliders_2(option, current_values)

    # Create all plot functions
    create_plot_functions(input, output)

# Create the app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()