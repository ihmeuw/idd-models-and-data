"""Layout components for Shiny applications."""

from shiny import ui
from typing import List, Optional, Dict, Any
from .components import create_model_controls_sidebar, create_model_selector_sidebar


def create_epidemiology_layout(
    model_type: str,
    param_values: Dict[str, float],
    plot_output_id: str = "plot",
    prefix: str = "p",
    include_dt: bool = False,
    button_label: str = "Run Model",
    button_id: str = "update_plot",
    plot_height: str = "400px"
) -> ui.Tag:
    """
    Create a standard layout for epidemiological model apps.
    
    Args:
        model_type: Type of epidemiological model
        param_values: Current parameter values
        plot_output_id: ID for the plot output
        prefix: Prefix for parameter IDs
        include_dt: Whether to include time step control
        button_label: Text for the action button
        button_id: ID for the action button
        plot_height: Height of the plot container
    """
    return ui.layout_sidebar(
        create_model_controls_sidebar(
            model_type=model_type,
            param_values=param_values,
            prefix=prefix,
            include_dt=include_dt,
            button_label=button_label,
            button_id=button_id
        ),
        ui.div(
            ui.output_plot(plot_output_id, width="100%", height=plot_height),
            class_="plot-container"
        )
    )


def create_model_comparison_layout(
    model_options: List[str],
    selected_model: str,
    param_values: Dict[str, float],
    plot_output_id: str = "plot",
    prefix: str = "p",
    button_label: str = "Run Model",
    button_id: str = "update_plot",
    plot_height: str = "400px"
) -> ui.Tag:
    """
    Create a layout for comparing different epidemiological models.
    
    Args:
        model_options: List of available model types
        selected_model: Currently selected model
        param_values: Current parameter values
        plot_output_id: ID for the plot output
        prefix: Prefix for parameter IDs
        button_label: Text for the action button
        button_id: ID for the action button
        plot_height: Height of the plot container
    """
    return ui.layout_sidebar(
        create_model_selector_sidebar(
            model_options=model_options,
            selected_model=selected_model,
            param_values=param_values,
            prefix=prefix,
            button_label=button_label,
            button_id=button_id
        ),
        ui.div(
            ui.output_plot(plot_output_id, width="100%", height=plot_height),
            class_="plot-container"
        )
    )


def create_multi_tab_layout(
    tab_configs: List[Dict[str, Any]],
    app_title: str = "Epidemiological Models Dashboard"
) -> ui.Tag:
    """
    Create a multi-tab layout for complex applications.
    
    Args:
        tab_configs: List of tab configuration dictionaries
        app_title: Title for the application
        
    Tab config format:
    {
        'title': 'Tab Name',
        'content': ui.Tag (the tab content),
        'id': 'optional_tab_id'
    }
    """
    nav_panels = []
    
    for config in tab_configs:
        tab_id = config.get('id', None)
        nav_panel = ui.nav_panel(
            config['title'],
            config['content'],
            value=tab_id
        )
        nav_panels.append(nav_panel)
    
    return ui.page_navbar(
        *nav_panels,
        title=app_title,
        id="navbar"
    )


def create_analysis_page(
    title: str,
    controls_content: ui.Tag,
    main_content: ui.Tag,
    sidebar_width: int = 300
) -> ui.Tag:
    """
    Create a standard analysis page with sidebar and main content.
    
    Args:
        title: Page title
        controls_content: Content for the sidebar
        main_content: Main content area
        sidebar_width: Width of the sidebar in pixels
    """
    return ui.nav_panel(
        title,
        ui.layout_sidebar(
            ui.sidebar(
                controls_content,
                width=sidebar_width
            ),
            main_content
        )
    )
