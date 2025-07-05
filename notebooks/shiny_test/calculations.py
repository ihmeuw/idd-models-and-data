import numpy as np
import pandas as pd

def cull_df(cull_column, df, threshold=0.001):
    """Cull DataFrame rows based on a threshold in a specific column"""
    if cull_column not in df.columns:
        raise ValueError(f"Column '{cull_column}' not found in DataFrame.")
    
    dt = df['time'].iloc[1] - df['time'].iloc[0] if 'time' in df.columns else 1
    extend = np.round(5 / dt).astype(int)  # Extend by 5 time units
    # Find the last index where the column value is above the threshold
    last_valid_index = df[df[cull_column] >= threshold].index.max()
    
    if last_valid_index is not None:
        # Keep rows up to the last valid index plus a few extra rows
        rows_to_keep = last_valid_index + extend
        return df.loc[:rows_to_keep]
    
    return df  # Return original DataFrame if no valid index found

def run_disrete_sir_model(I0, pars, dt = 0.01, dt_adjust = False):
    """Run the discrete SIR model simulation"""
    # Cull output at I(t) = 0.001
    I_threshold = min(0.001, I0 / 1000)
    beta = pars['beta']
    gamma = pars['gamma']
    if 'mu' in pars:
        mu = pars['mu']
    else:
        mu = 0
    # Initialize arrays
    n_steps = 1000
    time = np.arange(n_steps) * dt
    
    # Initial conditions
    S = np.zeros(n_steps)
    I = np.zeros(n_steps)
    R = np.zeros(n_steps)
    newI = np.zeros(n_steps)
    newR = np.zeros(n_steps)
    
    # Set initial values
    S[0] = 1.0 - I0  # Susceptible starts at 1 - initial infected
    I[0] = I0        # Initial infected
    R[0] = 0.0       # No recovered initially
    
    # SIR model simulation
    for t in range(1, n_steps):
        # Calculate new infections and recoveries
        if dt_adjust:
            new_infections = S[t-1] * (1 - np.exp(-beta * I[t-1] * dt))
            new_recoveries = I[t-1] * (1 - np.exp(-gamma * dt))
            susceptible_deaths = S[t-1] * (1 - np.exp(-mu * dt))
            infectious_deaths = I[t-1] * (1 - np.exp(-mu * dt))
            recovered_deaths = R[t-1] * (1 - np.exp(-mu * dt))
        else:
            new_infections = beta * S[t-1] * I[t-1] * dt
            new_recoveries = gamma * I[t-1] * dt
            susceptible_deaths = mu * S[t-1] * dt
            infectious_deaths = mu * I[t-1] * dt
            recovered_deaths = mu * R[t-1] * dt
        
        births = susceptible_deaths + infectious_deaths + recovered_deaths

        # Update compartments
        S[t] = S[t-1] - new_infections + births - susceptible_deaths
        I[t] = I[t-1] + new_infections - new_recoveries - infectious_deaths
        R[t] = R[t-1] + new_recoveries - recovered_deaths
        newI[t] = new_infections
        newR[t] = new_recoveries
    
    SIR_df = pd.DataFrame({
        'time': time,
        'S': S,
        'I': I,
        'R': R,
        'newI': newI,
        'newR': newR
    })
    
    return cull_df('I', SIR_df)

def run_disrete_seir_model(I0, pars, dt=0.01, dt_adjust = False):
    """Run the discrete SEIR model simulation"""
    # Cull output at I(t) = 0.001
    I_threshold = min(0.001, I0 / 1000)
    beta = pars['beta']
    sigma = pars['sigma']
    gamma = pars['gamma']
    if 'mu' in pars:
        mu = pars['mu']
    else:
        mu = 0
    # Initialize arrays
    n_steps = 1000
    time = np.arange(n_steps) * dt
    
    # Initial conditions
    S = np.zeros(n_steps)
    E = np.zeros(n_steps)
    I = np.zeros(n_steps)
    R = np.zeros(n_steps)
    newE = np.zeros(n_steps)
    newI = np.zeros(n_steps)
    newR = np.zeros(n_steps)
    
    # Set initial values
    S[0] = 1.0 - I0  # Susceptible starts at 1 - initial infected
    E[0] = 0.0       # No exposed initially
    I[0] = I0        # Initial infected
    R[0] = 0.0       # No recovered initially
    
    # SIR model simulation
    for t in range(1, n_steps):
        # Calculate new infections and recoveries
        if dt_adjust:
            new_exposures = S[t-1] * (1 - np.exp(-beta * I[t-1] * dt))
            new_infectious = E[t-1] * (1 - np.exp(-sigma * dt))
            new_recoveries = I[t-1] * (1 - np.exp(-gamma * dt))
            susceptible_deaths = S[t-1] * (1 - np.exp(-mu * dt))
            exposed_deaths = E[t-1] * (1 - np.exp(-mu * dt))
            infectious_deaths = I[t-1] * (1 - np.exp(-mu * dt))
            recovered_deaths = R[t-1] * (1 - np.exp(-mu * dt))
        else:
            new_exposures = beta * S[t-1] * I[t-1] * dt
            new_infectious = sigma * E[t-1] * dt
            new_recoveries = gamma * I[t-1] * dt
            susceptible_deaths = mu * S[t-1] * dt
            exposed_deaths = mu * E[t-1] * dt
            infectious_deaths = mu * I[t-1] * dt
            recovered_deaths = mu * R[t-1] * dt
        
        births = susceptible_deaths + exposed_deaths + infectious_deaths + recovered_deaths

        # Update compartments
        S[t] = S[t-1] - new_exposures + births - susceptible_deaths
        E[t] = E[t-1] + new_exposures - new_infectious - exposed_deaths
        I[t] = I[t-1] + new_infectious - new_recoveries - infectious_deaths
        R[t] = R[t-1] + new_recoveries - recovered_deaths
        newE[t] = new_exposures
        newI[t] = new_infectious
        newR[t] = new_recoveries
    
    SEIR_df = pd.DataFrame({
        'time': time,
        'S': S,
        'E': E,
        'I': I,
        'R': R,
        'newE': newE,
        'newI': newI,
        'newR': newR
    })


    return cull_df('I', SEIR_df)


def calculate_plot1_data(p1_i_0, p1_beta, p1_gamma, p1_dt):
    """Calculate data for plot1 based on slider values"""
    I0 = p1_i_0 / 100
    pars = {
        'beta': p1_beta,
        'gamma': p1_gamma,
    }
    dt = p1_dt
    model_df = run_disrete_sir_model(I0, pars, dt)
        
    return {
        'model_df': model_df,
        'title1': "Susceptible, Infectious, and Recovered Populations",
        'title2': "New Infections"
    }

def calculate_plot2_data(dropdown_value, p2_i_0, p2_beta, p2_gamma, p2_sigma=0, p2_aa=0):
    """Calculate data for plot2 based on dropdown and slider values"""
    I0 = p2_i_0 / 100
    pars = {
        'beta': p2_beta,
        'gamma': p2_gamma,
        'sigma': p2_sigma,
        'mu': 1 / p2_aa if p2_aa > 0 else 0
    }
    if dropdown_value == "SIR":
        pars['mu'] = 0
        model_df = run_disrete_sir_model(I0, pars)
        title1 = "SIR Model Simulation"
    elif dropdown_value == "SEIR":
        pars['mu'] = 0
        model_df = run_disrete_seir_model(I0, pars)
        title1 = "SEIR Model Simulation"
    elif dropdown_value == "SEIRS":
        model_df = run_disrete_seir_model(I0, pars)
        title1 = "SEIRS Model Simulation"
    
    return {
        'model': dropdown_value,
        'model_df': model_df,
        'title1': title1,
        'title2': "Go fuck yourself"
    }

def calculate_plot3_data(dropdown3_1, dropdown3_2, slider3_1, slider3_2, slider3_3, slider3_4, slider3_5):
    """Calculate data for plot3 complex multi-panel figure"""
    choice1_mult = {"Choice 1": 1, "Choice 2": 1.5, "Choice 3": 2, "Choice 4": 2.5}[dropdown3_1]
    choice2_mult = {"Type X": 0.5, "Type Y": 1, "Type Z": 1.5}[dropdown3_2]
    
    x = np.linspace(0, 10, 100)
    
    # Calculate y values for each panel
    y1 = np.sin(x * choice1_mult) * slider3_1 / 50
    y2 = np.cos(x * choice2_mult) * slider3_2 / 50
    y3 = (np.sin(x * slider3_3 / 10) * slider3_4 / 50 + 
          np.cos(x * slider3_5 / 10) * choice1_mult * choice2_mult)
    
    return {
        'x': x,
        'y1': y1,
        'y2': y2,
        'y3': y3,
        'title1': f"Panel 1: {dropdown3_1}",
        'title2': f"Panel 2: {dropdown3_2}",
        'title3': "Panel 3: Combined Analysis"
    }