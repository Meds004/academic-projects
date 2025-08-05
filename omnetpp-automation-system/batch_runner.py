import subprocess
import time
import psutil
from enum import Enum
from pathlib import Path
import uuid
import os
import shutil
from datetime import datetime
import multiprocessing
import random


# This class is simply used to represent the implemented parellel processing policies as constants
class MultiprocessingPolicy(Enum):
    BAG_OF_TASKS = "Bag of tasks"
    SMALLEST_SEED_FIRST = "Smallest seed first"
    LARGEST_SEED_FIRST = "Largest seed first"

# the multiprocessing policy to use
policy = MultiprocessingPolicy.BAG_OF_TASKS

# the seeds to run (number of cars / density)
seeds = ["7", "100", "400", "700"]

# how many simulations to run for each seed
# the length of this list must match the length of seeds!
repeats = [6, 5, 4, 3]

# terminal command to run veins_launchd script (to automate SUMO)
sumo_script_command = '/home/anthony/veins_framework/src/veins-veins-5.2/bin/veins_launchd -vv'

# the directory that contains omnetpp.ini
directory = Path("/home/anthony/veins_framework/src/omnetpp-6.0pre11/testworkspace/simu5G/simulations/NR/HOMng")

# The shell command to switch to the HOMng folder
cd_command = f"cd {directory}"

# The opp_run_command, obtained from running the simulation in Omnet++ with
# Cmdenv (shows in the console once you begin the simulation)
# Must remove the ?? option from this command, and remove omnetpp.ini from the
# end, which will be appended later with the correct ini file.
partial_opp_run_command = "opp_run -m -u Cmdenv -n ../../../emulation:../..:../../../src:../../../../inet/src:../../../../inet/examples:../../../../inet/tutorials:../../../../inet/showcases:../../../../veins/examples/veins:../../../../veins/src/veins -l ../../../src/simu5g -l ../../../../inet/src/INET -l ../../../../veins/src/veins"

# the full path to the ini file so the script can modify it
ini_file_path = "/home/anthony/veins_framework/src/omnetpp-6.0pre11/testworkspace/simu5G/simulations/NR/HOMng/omnetpp.ini"

# the temporary folder created to hold modified ini files
temp_ini_directory: Path
# the temporary folder name
temp_ini_folder = f"temp_{uuid.uuid4().int}"


# the folder to store the output of the current run
current_run_output_folder: Path

# this variable will hold the cleaned ini file as a list of lines of text
clean_ini_file_lines: list


def create_folder(parent: Path, folder: str):
    path = parent / folder

    try:
        path.mkdir(exist_ok=True)
        print(f"Successfully created folder: {folder}")
    except FileNotFoundError:
        print(f"Parent directory doesn't exist: {parent}")
    except Exception as e:
        print(f"Error: {e}")

    return path

'''
This method saves the output of a simulation to a file.
Two files are created for each simulation: stdout and stderr
'''
def save_output(out, err, seed: str, run):
    print("Creating output files...")

    out_file_path = current_run_output_folder / seed / "stdout" / f"stdout_{seed}_{run}.txt"
    err_file_path = current_run_output_folder / seed / "stderr" /f"stderr_{seed}_{run}.txt"
    fixed_file_path = current_run_output_folder / seed / "stdout_fixed" / f"stdout_fixed_{seed}_{run}.txt"

    with open(out_file_path, 'w') as file:
        file.write(out.decode('utf-8').strip())

    with open(err_file_path, 'w') as file:
        file.write(err.decode('utf-8').strip())

    with open(out_file_path, 'r') as file:
        lines = file.readlines()

    non_blank_lines = [line for line in lines if line.strip() != ""]

    with open(fixed_file_path, 'w') as file:
        file.writelines(non_blank_lines)


def create_ini_file(seed: str, run):
    new_file_name = f"omnetpp_{seed}_{run}.ini"
    new_ini_file = temp_ini_directory / new_file_name

    with open(new_ini_file, "w") as file:
        newline = f'*.veinsManager.launchConfig = xmldoc("colognev{seed}.launchd.xml")\n'
        for line in clean_ini_file_lines:
            if line.startswith('*.veinsManager.launchConfig'):
                file.write(newline)
            else:
                file.write(line + '\n')


def clean_ini_file():
    with open(ini_file_path, 'r') as file:
            omnetpp_ini_lines = file.readlines()

    cleaned_lines = []
    for line in omnetpp_ini_lines:
        stripped_line = line.strip()

        if stripped_line and not stripped_line.startswith('#'):
            cleaned_lines.append(stripped_line)
    
    return cleaned_lines

'''
This method starts the SUMO automation script on a new thread. 
'''
def start_sumo(sumo_script_command):
    sumo = subprocess.Popen(sumo_script_command, shell=True)
    return sumo


'''
This method begins a simulation with the given seed, and saves the outputs
to files.
'''
def start_simulation(seed: str, run):
    ini_file_name = f"omnetpp_{seed}_{run}.ini"

    # Move ini file to main folder
    shutil.move(str(temp_ini_directory / ini_file_name), str(directory))

    # Update command to use the new ini file
    command = f"{cd_command} && {partial_opp_run_command} {ini_file_name}"

    # Start new simulation
    simulation = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Waits for simulation to complete and gets the output
    stdout, stderr = simulation.communicate()

    # Save output to file
    save_output(stdout, stderr, seed, run)

    # Return ini file
    shutil.move(str(directory / ini_file_name), str(temp_ini_directory))


def cleanup():
    try:
        if os.path.exists(temp_ini_directory):
            shutil.rmtree(temp_ini_directory)
            print(f"{temp_ini_directory} and it's contents deleted.")
        else:
            print(f"Directory {temp_ini_directory} does not exist.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    # Declare global variables
    global temp_ini_directory
    global clean_ini_file_lines
    global current_run_output_folder

    # Create main output folder
    home_path = Path.home()
    desktop_path = home_path / 'Desktop'
    output_folder = "Output"
    output_folder_path = create_folder(desktop_path, output_folder)

    # Create subfolder in output for this run (uses date and time)
    now = datetime.now()
    current_run_output_folder_name = now.strftime("Simulation_%Y-%m-%d_%H-%M-%S")
    current_run_output_folder = create_folder(output_folder_path, current_run_output_folder_name)

    # Create output subfolders for each seed
    for seed in seeds:
        seed_folder = create_folder(current_run_output_folder, seed)
        create_folder(seed_folder, 'stdout')
        create_folder(seed_folder, 'stderr')
        create_folder(seed_folder, 'stdout_fixed')

    # Create temp folder for ini files
    temp_ini_directory = create_folder(directory, temp_ini_folder)

    # Clean omnetpp.ini and store contents in variable
    clean_ini_file_lines = clean_ini_file()

    # Create ini files for each seed
    # for seed in seeds:
    #     for run in range(1, repeat + 1):
    #         create_ini_file(seed, run)

    for i in range(len(seeds)):
        for run in range(1, repeats[i] + 1):
            create_ini_file(seeds[i], run)


    # Start SUMO
    print("Starting SUMO...")
    sumo_process = start_sumo(sumo_script_command)
    time.sleep(2) # allow time for script to load

    # Start simulation
    print("Starting Simulation...")
    

    tasks = []

    # Creates tuples of all possible seed/run pairs - to be used arguments
    for i in range(len(seeds)):
        for j in range(1, repeats[i] + 1):
            tasks.append((seeds[i], j))

    # Sort the task parameters according to the desired multiprocessing policy
    # No need to modify tasks if smallest seed first is the chosen policy
    if policy == MultiprocessingPolicy.LARGEST_SEED_FIRST:
        tasks.sort(key=lambda x: int(x[0]), reverse=True)
        print("Using 'largest seed first' policy")
    elif policy == MultiprocessingPolicy.BAG_OF_TASKS:
        random.shuffle(tasks)
        print("Using 'bag of tasks (random)' policy")

    # For each seed and run, begin the simulations in parallel
    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        pool.starmap(start_simulation, tasks)

    print("Simulation Complete")

    # Kill SUMO script (veins_launchd)
    print("Killing SUMO script...")
    try:
        parent = psutil.Process(sumo_process.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
    except psutil.NoSuchProcess:
        pass

    # Perform clean up operations (remove temporary ini files)
    cleanup()
    


if __name__ == "__main__":
    main()