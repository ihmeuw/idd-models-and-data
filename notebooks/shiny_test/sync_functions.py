from shiny import ui, reactive

def create_sync_functions(input, param_values):
    """Create all sync functions for the app"""
    
    # Page 1 sync functions
    @reactive.effect
    def sync_i0_slider_to_numeric():
        ui.update_numeric("p1_i_0_num", value=input.p1_i_0())

    @reactive.effect  
    def sync_i0_numeric_to_slider():
        ui.update_slider("p1_i_0", value=input.p1_i_0_num())
        
    @reactive.effect
    def sync_beta_slider_to_numeric():
        ui.update_numeric("p1_beta_num", value=input.p1_beta())

    @reactive.effect  
    def sync_beta_numeric_to_slider():
        ui.update_slider("p1_beta", value=input.p1_beta_num())

    @reactive.effect
    def sync_gamma_slider_to_numeric():
        ui.update_numeric("p1_gamma_num", value=input.p1_gamma())

    @reactive.effect  
    def sync_gamma_numeric_to_slider():
        ui.update_slider("p1_gamma", value=input.p1_gamma_num())

    # Page 2 sync functions
    def create_p2_sync(param_name):
        """Create sync functions for a Page 2 parameter"""
        @reactive.effect
        def sync_slider_to_numeric():
            try:
                ui.update_numeric(f"p2_{param_name}_num", value=input[f"p2_{param_name}"]())
            except:
                pass

        @reactive.effect  
        def sync_numeric_to_slider():
            try:
                ui.update_slider(f"p2_{param_name}", value=input[f"p2_{param_name}_num"]())
            except:
                pass
    
    # Create sync functions for all Page 2 parameters
    for param in ["i0", "beta", "gamma", "sigma", "aa"]:
        create_p2_sync(param)

    # Update reactive values
    @reactive.effect
    def update_param_values_from_p1():
        current_values = param_values.get()
        current_values.update({
            'i_0': input.p1_i_0(),
            'beta': input.p1_beta(),
            'gamma': input.p1_gamma()
        })
        param_values.set(current_values)

    @reactive.effect
    def store_p2_values():
        def safe_get(input_id, default):
            try:
                return input[input_id]()
            except:
                return default
                
        current_values = param_values.get()
        current_values.update({
            'i_0': safe_get('p2_i_0', current_values['i_0']),
            'beta': safe_get('p2_beta', current_values['beta']),
            'gamma': safe_get('p2_gamma', current_values['gamma']),
            'sigma': safe_get('p2_sigma', current_values['sigma']),
            'aa': safe_get('p2_aa', current_values['aa'])
        })
        param_values.set(current_values)