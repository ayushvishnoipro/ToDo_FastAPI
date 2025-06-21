import subprocess
import sys

def fix_pydantic_dependency():
    """
    Fix the ForwardRef._evaluate() error by installing the correct version of pydantic
    """
    print("Fixing pydantic dependency...")
    
    try:
        # Uninstall current pydantic version
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "pydantic"])
        print("✅ Removed existing pydantic installation")
        
        # Install the specific version that works with your FastAPI version
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic==1.10.13"])
        print("✅ Installed pydantic 1.10.13")
        
        # Additional dependencies that might be needed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "typing-extensions>=4.2.0"])
        print("✅ Installed typing-extensions")
        
        print("\n✅ Dependency fix complete!")
        print("\nYou can now run your FastAPI application with:")
        print("python run_api.py")
        
    except Exception as e:
        print(f"❌ Error fixing dependencies: {e}")
        
if __name__ == "__main__":
    fix_pydantic_dependency()