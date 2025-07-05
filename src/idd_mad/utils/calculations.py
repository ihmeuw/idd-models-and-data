"""Calculation utilities for epidemiological models."""

from typing import Dict, Any
import pandas as pd
from ..models.sir import run_sir_model, run_seir_model


class ModelCalculator:
    """Utility class for calculating model results with consistent interfaces."""
    
    @staticmethod
    def calculate_sir_data(
        i_0_percent: float, 
        beta: float, 
        gamma: float, 
        dt: float = 0.01,
        mu: float = 0.0,
        use_exponential_form: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate SIR model data from parameters.
        
        Args:
            i_0_percent: Initial percentage infected (0-100)
            beta: Transmission rate
            gamma: Recovery rate
            dt: Time step
            mu: Birth/death rate
            use_exponential_form: Whether to use exponential transitions
            
        Returns:
            Dictionary with model results and metadata
        """
        i_0 = i_0_percent / 100
        parameters = {
            'beta': beta,
            'gamma': gamma,
            'mu': mu
        }
        
        model_df = run_sir_model(
            initial_infected=i_0,
            parameters=parameters,
            dt=dt,
            use_exponential_form=use_exponential_form
        )
        
        return {
            'model_type': 'SIR',
            'model_df': model_df,
            'parameters': parameters,
            'initial_infected_percent': i_0_percent,
            'title1': "Susceptible, Infectious, and Recovered Populations",
            'title2': "New Infections"
        }
    
    @staticmethod
    def calculate_seir_data(
        i_0_percent: float,
        beta: float,
        sigma: float, 
        gamma: float,
        dt: float = 0.01,
        mu: float = 0.0,
        use_exponential_form: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate SEIR model data from parameters.
        
        Args:
            i_0_percent: Initial percentage infected (0-100)
            beta: Transmission rate
            sigma: Incubation rate
            gamma: Recovery rate
            dt: Time step
            mu: Birth/death rate
            use_exponential_form: Whether to use exponential transitions
            
        Returns:
            Dictionary with model results and metadata
        """
        i_0 = i_0_percent / 100
        parameters = {
            'beta': beta,
            'sigma': sigma,
            'gamma': gamma,
            'mu': mu
        }
        
        model_df = run_seir_model(
            initial_infected=i_0,
            parameters=parameters,
            dt=dt,
            use_exponential_form=use_exponential_form
        )
        
        return {
            'model_type': 'SEIR',
            'model_df': model_df,
            'parameters': parameters,
            'initial_infected_percent': i_0_percent,
            'title1': "SEIR Model Simulation", 
            'title2': "New Infections"
        }
    
    @staticmethod
    def calculate_model_data(
        model_type: str,
        i_0_percent: float,
        beta: float,
        gamma: float,
        sigma: float = 1.0,
        average_age: float = 70.0,
        dt: float = 0.01,
        use_exponential_form: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate model data for any supported model type.
        
        Args:
            model_type: 'SIR', 'SEIR', or 'SEIRS'
            i_0_percent: Initial percentage infected (0-100)
            beta: Transmission rate
            gamma: Recovery rate
            sigma: Incubation rate (for SEIR/SEIRS)
            average_age: Average age for birth/death rate (for SEIRS)
            dt: Time step
            use_exponential_form: Whether to use exponential transitions
            
        Returns:
            Dictionary with model results and metadata
        """
        # Calculate mu from average age
        mu = 1.0 / average_age if average_age > 0 else 0.0
        
        if model_type.upper() == 'SIR':
            return ModelCalculator.calculate_sir_data(
                i_0_percent, beta, gamma, dt, 
                mu=(mu if model_type.upper() == 'SIRS' else 0.0),
                use_exponential_form=use_exponential_form
            )
        elif model_type.upper() in ['SEIR', 'SEIRS']:
            result = ModelCalculator.calculate_seir_data(
                i_0_percent, beta, sigma, gamma, dt,
                mu=(mu if model_type.upper() == 'SEIRS' else 0.0),
                use_exponential_form=use_exponential_form
            )
            result['model_type'] = model_type.upper()
            result['title1'] = f"{model_type.upper()} Model Simulation"
            return result
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    @staticmethod
    def get_basic_reproduction_number(beta: float, gamma: float) -> float:
        """Calculate basic reproduction number R0."""
        return beta / gamma
    
    @staticmethod
    def get_epidemic_threshold(beta: float, gamma: float) -> bool:
        """Check if epidemic threshold is exceeded (R0 > 1)."""
        return ModelCalculator.get_basic_reproduction_number(beta, gamma) > 1.0
