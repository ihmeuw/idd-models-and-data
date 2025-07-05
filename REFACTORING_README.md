# Epidemiological Modeling Package - Refactored Structure

This document describes the new, refactored structure of the epidemiological modeling package that moves the Shiny applications from `notebooks/shiny_test/` into a proper Python package structure.

## New Structure

```
src/
  idd_mad/
    __init__.py              # Main package initialization
    models/
      __init__.py            # Models module exports
      sir.py                 # SIR/SEIR/SEIRS model implementations
    visualization/
      __init__.py            # Visualization module exports
      colors.py              # Color schemes and palettes
      plotting.py            # Generalized plotting functions
    ui/
      __init__.py            # UI module exports
      components.py          # Reusable UI components
      layouts.py             # Common layout patterns
    apps/
      __init__.py            # Apps management
      sir_demo/
        app.py               # SIR demo app entry point
        ui.py                # UI for SIR demo
        server.py            # Server logic for SIR demo
      model_comparison/
        app.py               # Model comparison app entry point
        ui.py                # UI for model comparison
        server.py            # Server logic for model comparison
    utils/
      __init__.py            # Utilities module exports
      calculations.py        # Calculation utilities
      sync.py                # Shiny synchronization utilities
```

## Key Benefits

### 1. **Modularity**
- Each component has a clear responsibility
- Models can be used independently of UI
- Visualization functions are reusable
- UI components are standardized

### 2. **Reusability**
- Model functions work across multiple apps
- UI components can be used in different applications
- Visualization functions support multiple model types
- Calculation utilities provide consistent interfaces

### 3. **Maintainability**
- Clear separation of concerns
- Type hints throughout for better IDE support
- Comprehensive documentation
- Error handling and validation

### 4. **Extensibility**
- Easy to add new epidemiological models
- Simple to create new Shiny applications
- Straightforward to add visualization types
- Modular design supports future growth

## Usage Examples

### Using Models Directly

```python
from idd_mad.models.sir import run_sir_model

# Run SIR model
result = run_sir_model(
    initial_infected=0.01,
    parameters={'beta': 0.3, 'gamma': 0.1},
    dt=0.01
)
```

### Using the Calculation Utilities

```python
from idd_mad.utils.calculations import ModelCalculator

# Calculate SIR data with proper formatting
data = ModelCalculator.calculate_sir_data(
    i_0_percent=1.0,
    beta=0.3,
    gamma=0.1
)

# Check epidemic threshold
r0 = ModelCalculator.get_basic_reproduction_number(0.3, 0.1)
epidemic = ModelCalculator.get_epidemic_threshold(0.3, 0.1)
```

### Creating Visualizations

```python
from idd_mad.visualization.plotting import create_epidemiology_figure

# Create a figure for SIR results
fig = create_epidemiology_figure(
    df=result_dataframe,
    model_type='SIR',
    title='My SIR Analysis'
)
```

### Running Shiny Apps

```python
from idd_mad.apps import run_app, list_apps

# See available apps
print(list_apps())

# Run specific app
run_app('sir_demo')
run_app('model_comparison')
```

### Building Custom UI

```python
from idd_mad.ui.components import parameter_input_with_sync, model_parameter_set
from idd_mad.ui.layouts import create_epidemiology_layout

# Create parameter inputs
param_input = parameter_input_with_sync(
    "beta", "Transmission Rate", 0.1, 2.0, 0.3
)

# Create full model parameter set
param_set = model_parameter_set("SEIR", default_values)

# Create complete layout
layout = create_epidemiology_layout(
    model_type="SIR",
    param_values=defaults
)
```

## Migration from Original Structure

The original files in `notebooks/shiny_test/` have been refactored as follows:

- `calculations.py` → `src/idd_mad/models/sir.py` + `src/idd_mad/utils/calculations.py`
- `constants.py` → `src/idd_mad/visualization/colors.py`
- `plotting_functions.py` → `src/idd_mad/visualization/plotting.py`
- `ui_components.py` → `src/idd_mad/ui/components.py` + `src/idd_mad/ui/layouts.py`
- `sync_functions.py` → `src/idd_mad/utils/sync.py`
- `app.py` → `src/idd_mad/apps/sir_demo/` (multiple files)
- Additional model comparison app created in `src/idd_mad/apps/model_comparison/`

## Running the Applications

### SIR Demo App
```bash
python -m src.idd_mad.apps.sir_demo.app
```

### Model Comparison App
```bash
python -m src.idd_mad.apps.model_comparison.app
```

### Using the Package Manager
```python
from src.idd_mad.apps import run_app
run_app('sir_demo')
```

## Adding New Apps

To add a new epidemiological modeling app:

1. Create a new directory under `src/idd_mad/apps/your_app_name/`
2. Create `app.py`, `ui.py`, and `server.py` files
3. Use the existing UI components and model functions
4. Add import to `src/idd_mad/apps/__init__.py`

Example structure:
```
src/idd_mad/apps/your_app_name/
├── app.py              # Main app factory
├── ui.py               # UI definition
└── server.py           # Server logic
```

## Dependencies

The refactored package uses the same dependencies as the original:
- `shiny` - Web application framework
- `matplotlib` - Plotting and visualization
- `numpy` - Numerical computations
- `pandas` - Data manipulation

## Testing

Run the demo script to verify everything works:
```bash
python demo_usage.py
```

This will test all major components and show usage examples.
