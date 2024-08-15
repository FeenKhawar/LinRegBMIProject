import subprocess

def run_script(script_name):
    try:
        # Note the "python3," if an error occurs in relation to "python3" then switch the name for whatever version of python/program you are running this on
        # If you are using python but not python3, you may need to remove the "3" to have just "python"
        subprocess.run(["python3", script_name], check=True)
        print(f"Successfully ran {script_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        return False
    
# If one wants to exclude one of the programs from the list (or re-arrange the order), exclude it (or re-arrange it) from the scripts list below
if __name__ == "__main__":
    scripts = ["DataRetrieval.py", "PlotsAndGraphs.py", "LinearRegressions.py"]

for script in scripts:
    success = run_script(script)
    if not success:
        print(f"Stopping execution due to failure in {script}.")
        break