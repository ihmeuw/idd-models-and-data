"""Script to list and run available Shiny apps."""

from src.idd_mad.apps import list_apps, run_app

def main():
    print("Available Shiny Apps:")
    print("=" * 30)
    
    apps = list_apps()
    for i, app_name in enumerate(apps, 1):
        print(f"{i}. {app_name}")
    
    print("\nTo run an app, choose one of these methods:")
    print("\n1. Using the app manager:")
    for app_name in apps:
        print(f"   run_app('{app_name}')")
    
    print("\n2. Running modules directly:")
    for app_name in apps:
        print(f"   python -m src.idd_mad.apps.{app_name}.app")
    
    print("\n3. Or uncomment one of the lines below:")
    for app_name in apps:
        print(f"   # run_app('{app_name}')")
    
    # Uncomment one of these to run an app:
    # run_app('sir_demo')
    # run_app('model_comparison') 
    # run_app('multi_tab_dashboard')

if __name__ == "__main__":
    main()
