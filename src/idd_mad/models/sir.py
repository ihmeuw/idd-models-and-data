"""SIR, SEIR, and SEIRS epidemiological models."""

import numpy as np
import pandas as pd
from typing import Dict, Optional


def cull_dataframe(df: pd.DataFrame, cull_column: str, threshold: float = 0.001, extend_time: float = 5.0) -> pd.DataFrame:
    """
    Cull DataFrame rows based on a threshold in a specific column.
    
    Args:
        df: DataFrame containing simulation results
        cull_column: Column name to check against threshold
        threshold: Value below which to cull the data
        extend_time: Additional time units to keep after threshold is reached
        
    Returns:
        Culled DataFrame
    """
    if cull_column not in df.columns:
        raise ValueError(f"Column '{cull_column}' not found in DataFrame.")
    
    if 'time' not in df.columns:
        return df
        
    dt = df['time'].iloc[1] - df['time'].iloc[0]
    extend = int(np.round(extend_time / dt))
    
    # Find the last index where the column value is above the threshold
    last_valid_index = df[df[cull_column] >= threshold].index.max()
    
    if last_valid_index is not None:
        rows_to_keep = min(last_valid_index + extend, len(df) - 1)
        return df.iloc[:rows_to_keep + 1].copy()
    
    return df


def run_sir_model(
    initial_infected: float,
    parameters: Dict[str, float],
    dt: float = 0.01,
    max_time: float = 100.0,
    use_exponential_form: bool = False
) -> pd.DataFrame:
    """
    Run discrete SIR model simulation.
    
    Args:
        initial_infected: Initial fraction of population infected (0-1)
        parameters: Dict with 'beta', 'gamma', and optionally 'mu' (death rate)
        dt: Time step
        max_time: Maximum simulation time
        use_exponential_form: Whether to use exponential form for transitions
        
    Returns:
        DataFrame with columns: time, S, I, R, newI, newR
    """
    n_steps = int(max_time / dt)
    time = np.arange(n_steps) * dt
    
    # Extract parameters
    beta = parameters['beta']
    gamma = parameters['gamma']
    mu = parameters.get('mu', 0.0)
    
    # Initialize arrays
    S = np.zeros(n_steps)
    I = np.zeros(n_steps)
    R = np.zeros(n_steps)
    newI = np.zeros(n_steps)
    newR = np.zeros(n_steps)
    
    # Initial conditions
    S[0] = 1.0 - initial_infected
    I[0] = initial_infected
    R[0] = 0.0
    
    # Simulation loop
    for t in range(1, n_steps):
        if use_exponential_form:
            new_infections = S[t-1] * (1 - np.exp(-beta * I[t-1] * dt))
            new_recoveries = I[t-1] * (1 - np.exp(-gamma * dt))
            s_deaths = S[t-1] * (1 - np.exp(-mu * dt))
            i_deaths = I[t-1] * (1 - np.exp(-mu * dt))
            r_deaths = R[t-1] * (1 - np.exp(-mu * dt))
        else:
            new_infections = beta * S[t-1] * I[t-1] * dt
            new_recoveries = gamma * I[t-1] * dt
            s_deaths = mu * S[t-1] * dt
            i_deaths = mu * I[t-1] * dt
            r_deaths = mu * R[t-1] * dt
        
        births = s_deaths + i_deaths + r_deaths
        
        S[t] = S[t-1] - new_infections + births - s_deaths
        I[t] = I[t-1] + new_infections - new_recoveries - i_deaths
        R[t] = R[t-1] + new_recoveries - r_deaths
        newI[t] = new_infections
        newR[t] = new_recoveries
    
    df = pd.DataFrame({
        'time': time,
        'S': S,
        'I': I,
        'R': R,
        'newI': newI,
        'newR': newR
    })
    
    return cull_dataframe(df, 'I')


def run_seir_model(
    initial_infected: float,
    parameters: Dict[str, float],
    dt: float = 0.01,
    max_time: float = 100.0,
    use_exponential_form: bool = False
) -> pd.DataFrame:
    """
    Run discrete SEIR model simulation.
    
    Args:
        initial_infected: Initial fraction of population infected (0-1)
        parameters: Dict with 'beta', 'sigma', 'gamma', and optionally 'mu'
        dt: Time step
        max_time: Maximum simulation time
        use_exponential_form: Whether to use exponential form for transitions
        
    Returns:
        DataFrame with columns: time, S, E, I, R, newE, newI, newR
    """
    n_steps = int(max_time / dt)
    time = np.arange(n_steps) * dt
    
    # Extract parameters
    beta = parameters['beta']
    sigma = parameters['sigma']
    gamma = parameters['gamma']
    mu = parameters.get('mu', 0.0)
    
    # Initialize arrays
    S = np.zeros(n_steps)
    E = np.zeros(n_steps)
    I = np.zeros(n_steps)
    R = np.zeros(n_steps)
    newE = np.zeros(n_steps)
    newI = np.zeros(n_steps)
    newR = np.zeros(n_steps)
    
    # Initial conditions
    S[0] = 1.0 - initial_infected
    E[0] = 0.0
    I[0] = initial_infected
    R[0] = 0.0
    
    # Simulation loop
    for t in range(1, n_steps):
        if use_exponential_form:
            new_exposures = S[t-1] * (1 - np.exp(-beta * I[t-1] * dt))
            new_infectious = E[t-1] * (1 - np.exp(-sigma * dt))
            new_recoveries = I[t-1] * (1 - np.exp(-gamma * dt))
            s_deaths = S[t-1] * (1 - np.exp(-mu * dt))
            e_deaths = E[t-1] * (1 - np.exp(-mu * dt))
            i_deaths = I[t-1] * (1 - np.exp(-mu * dt))
            r_deaths = R[t-1] * (1 - np.exp(-mu * dt))
        else:
            new_exposures = beta * S[t-1] * I[t-1] * dt
            new_infectious = sigma * E[t-1] * dt
            new_recoveries = gamma * I[t-1] * dt
            s_deaths = mu * S[t-1] * dt
            e_deaths = mu * E[t-1] * dt
            i_deaths = mu * I[t-1] * dt
            r_deaths = mu * R[t-1] * dt
        
        births = s_deaths + e_deaths + i_deaths + r_deaths
        
        S[t] = S[t-1] - new_exposures + births - s_deaths
        E[t] = E[t-1] + new_exposures - new_infectious - e_deaths
        I[t] = I[t-1] + new_infectious - new_recoveries - i_deaths
        R[t] = R[t-1] + new_recoveries - r_deaths
        newE[t] = new_exposures
        newI[t] = new_infectious
        newR[t] = new_recoveries
    
    df = pd.DataFrame({
        'time': time,
        'S': S,
        'E': E,
        'I': I,
        'R': R,
        'newE': newE,
        'newI': newI,
        'newR': newR
    })
    
    return cull_dataframe(df, 'I')
