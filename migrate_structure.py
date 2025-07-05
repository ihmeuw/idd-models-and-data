"""Migration script to help transition from old shiny_test structure to new package structure."""

import shutil
import os
from pathlib import Path


def backup_original_files():
    """Create backup of original shiny_test files."""
    source_dir = Path("notebooks/shiny_test")
    backup_dir = Path("notebooks/shiny_test_backup")
    
    if source_dir.exists() and not backup_dir.exists():
        print(f"Creating backup: {source_dir} → {backup_dir}")
        shutil.copytree(source_dir, backup_dir)
        print("✓ Backup created successfully")
    elif backup_dir.exists():
        print("ℹ Backup already exists, skipping")
    else:
        print("⚠ Original shiny_test directory not found")


def verify_new_structure():
    """Verify that the new package structure is properly created."""
    required_files = [
        "src/idd_mad/__init__.py",
        "src/idd_mad/models/__init__.py",
        "src/idd_mad/models/sir.py",
        "src/idd_mad/visualization/__init__.py",
        "src/idd_mad/visualization/colors.py",
        "src/idd_mad/visualization/plotting.py",
        "src/idd_mad/ui/__init__.py",
        "src/idd_mad/ui/components.py",
        "src/idd_mad/ui/layouts.py",
        "src/idd_mad/utils/__init__.py",
        "src/idd_mad/utils/calculations.py",
        "src/idd_mad/utils/sync.py",
        "src/idd_mad/apps/__init__.py",
        "src/idd_mad/apps/sir_demo/app.py",
        "src/idd_mad/apps/sir_demo/ui.py",
        "src/idd_mad/apps/sir_demo/server.py",
        "src/idd_mad/apps/model_comparison/app.py",
        "src/idd_mad/apps/model_comparison/ui.py",
        "src/idd_mad/apps/model_comparison/server.py",
    ]
    
    print("Verifying new package structure...")
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✓ {file_path}")
    
    if missing_files:
        print("\n⚠ Missing files:")
        for file_path in missing_files:
            print(f"  ✗ {file_path}")
        return False
    else:
        print("\n✓ All required files are present!")
        return True


def test_imports():
    """Test that the new package structure imports correctly."""
    print("\nTesting imports...")
    
    try:
        # Test basic imports
        from src.idd_mad import models, visualization, ui, utils, apps
        print("✓ Main package imports successful")
        
        # Test model functions
        from src.idd_mad.models.sir import run_sir_model, run_seir_model
        print("✓ Model functions import successful")
        
        # Test visualization
        from src.idd_mad.visualization.plotting import create_epidemiology_figure
        print("✓ Visualization functions import successful")
        
        # Test UI components
        from src.idd_mad.ui.components import parameter_input_with_sync
        print("✓ UI components import successful")
        
        # Test utilities
        from src.idd_mad.utils.calculations import ModelCalculator
        print("✓ Utility classes import successful")
        
        # Test apps
        from src.idd_mad.apps import list_apps
        print("✓ Apps module import successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality of the refactored code."""
    print("\nTesting basic functionality...")
    
    try:
        from src.idd_mad.models.sir import run_sir_model
        from src.idd_mad.utils.calculations import ModelCalculator
        
        # Test SIR model
        result = run_sir_model(
            initial_infected=0.01,
            parameters={'beta': 0.3, 'gamma': 0.1},
            dt=0.1,
            max_time=10.0
        )
        
        if len(result) > 0 and 'I' in result.columns:
            print("✓ SIR model runs successfully")
        else:
            print("✗ SIR model output appears incorrect")
            return False
        
        # Test calculator
        data = ModelCalculator.calculate_sir_data(1.0, 0.3, 0.1)
        if 'model_df' in data and len(data['model_df']) > 0:
            print("✓ ModelCalculator works correctly")
        else:
            print("✗ ModelCalculator output appears incorrect")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False


def create_migration_summary():
    """Create a summary of the migration process."""
    summary = """
# Migration Summary

## ✅ Completed Tasks

1. **Package Structure Created**
   - Created modular package structure under `src/idd_mad/`
   - Separated concerns into distinct modules
   - Added proper `__init__.py` files with exports

2. **Models Refactored**
   - Moved model logic to `src/idd_mad/models/sir.py`
   - Improved function signatures and documentation
   - Added proper type hints and error handling

3. **Visualization Improved**
   - Created `src/idd_mad/visualization/` module
   - Standardized color schemes in `colors.py`
   - Generalized plotting functions in `plotting.py`

4. **UI Components Modularized**
   - Reusable components in `src/idd_mad/ui/components.py`
   - Layout templates in `src/idd_mad/ui/layouts.py`
   - Consistent CSS styling

5. **Utilities Created**
   - Model calculation utilities in `src/idd_mad/utils/calculations.py`
   - Shiny synchronization helpers in `src/idd_mad/utils/sync.py`

6. **Apps Restructured**
   - SIR demo app in `src/idd_mad/apps/sir_demo/`
   - Model comparison app in `src/idd_mad/apps/model_comparison/`
   - App management system in `src/idd_mad/apps/__init__.py`

## 🚀 Next Steps

1. **Test the new structure:**
   ```bash
   python demo_usage.py
   ```

2. **Run individual apps:**
   ```bash
   python -m src.idd_mad.apps.sir_demo.app
   python -m src.idd_mad.apps.model_comparison.app
   ```

3. **Use the package in your code:**
   ```python
   from src.idd_mad.apps import run_app
   run_app('sir_demo')
   ```

## 📁 File Mapping

Original → New Location:
- `notebooks/shiny_test/calculations.py` → `src/idd_mad/models/sir.py` + `src/idd_mad/utils/calculations.py`
- `notebooks/shiny_test/constants.py` → `src/idd_mad/visualization/colors.py`
- `notebooks/shiny_test/plotting_functions.py` → `src/idd_mad/visualization/plotting.py`
- `notebooks/shiny_test/ui_components.py` → `src/idd_mad/ui/components.py` + `src/idd_mad/ui/layouts.py`
- `notebooks/shiny_test/sync_functions.py` → `src/idd_mad/utils/sync.py`
- `notebooks/shiny_test/app.py` → `src/idd_mad/apps/sir_demo/` (split into multiple files)

Original files have been backed up to `notebooks/shiny_test_backup/`
"""
    
    with open("MIGRATION_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📄 Migration summary written to MIGRATION_SUMMARY.md")


def main():
    """Run the complete migration process."""
    print("🔄 Starting migration from shiny_test to new package structure")
    print("=" * 60)
    
    # Step 1: Backup original files
    backup_original_files()
    
    # Step 2: Verify new structure
    structure_ok = verify_new_structure()
    
    if not structure_ok:
        print("❌ Migration incomplete - some files are missing")
        return False
    
    # Step 3: Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("❌ Migration incomplete - import errors detected")
        return False
    
    # Step 4: Test functionality
    functionality_ok = test_basic_functionality()
    
    if not functionality_ok:
        print("❌ Migration incomplete - functionality errors detected")
        return False
    
    # Step 5: Create summary
    create_migration_summary()
    
    print("\n🎉 Migration completed successfully!")
    print("\n📚 Next steps:")
    print("1. Run: python demo_usage.py")
    print("2. Test apps: python -m src.idd_mad.apps.sir_demo.app")
    print("3. Read: REFACTORING_README.md")
    print("4. Check: MIGRATION_SUMMARY.md")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
