import os
import matplotlib.pyplot as plt

def main_menu():
    print("\n")
    print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
    print("\n")
    print("Welcome to the visualizer tool, please choose which behaviour you want to visualize:\n")
    print("1. Minor CPU")
    print("2. Trace CPU")
    print("3. Exit\n")
    choice = input("Enter choice (1/2/3):")
    print("\n")

    if choice == '1':
        cpu_model_menu("MinorCPU")
    elif choice == '2':
        cpu_model_menu("TraceCPU")
    elif choice == '3':
        print("Program terminated.")
    else:
        print("Invalid choice, please pick a valid option\n")
        main_menu()


def cpu_model_menu(cpu_model):
    print("\n")
    print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
    print("\n")
    print("Please select the architecture:\n")
    print("1. ARM")
    print("2. RISC-V")
    print("3. Exit\n")
    choice = input("Enter choice (1/2/3): ")
    print("\n")

    if choice == '1':
        benchmark_menu(cpu_model, "ARM")
    elif choice == '2':
        benchmark_menu(cpu_model, "RISCV")
    elif choice == '3':
        print("Program terminated.")
    else:
        print("Invalid choice, please pick a valid option\n")
        cpu_model_menu(cpu_model)


def benchmark_menu(cpu_model, architecture):
    print("\n")
    print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
    print("\n")
    print("Please select the benchmark:\n")
    print("1. SPEC")
    print("2. PARSEC")
    print("3. Exit\n")
    choice = input("Enter choice (1/2/3): ")
    print("\n")

    if choice == '1':
        parameter_menu(cpu_model, architecture, "SPEC")
    elif choice == '2':
        parameter_menu(cpu_model, architecture, "PARSEC")
    else:
        print("Invalid choice, please pick a valid option\n")
        benchmark_menu(cpu_model, architecture)


def parameter_menu(cpu_model, architecture, benchmark):
    print("\n")
    print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
    print("\n")
    print("Please select which parameter you want to see:\n")
    print("1. Cache size")
    print("2. Replacement policies")
    print("3. Exit\n")
    choice = input("Enter choice (1/2/3): ")
    print("\n")

    if choice == '1':
        statistic_menu(cpu_model, architecture, benchmark, "Cache")
    elif choice == '2':
        statistic_menu(cpu_model, architecture, benchmark, "PdR")
    elif choice == '3':
        print("Program terminated.")
    else:
        print("Invalid choice, please pick a valid option\n")
        parameter_menu(cpu_model, architecture, benchmark)

def statistic_menu(cpu_model, architecture, benchmark, parameter):
    print("\n")
    print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
    print("\n")
    print("Please select which parameter you want to see:\n")
    print("1. Data cache total misses")
    print("2. Data cache total hits")
    print("3. Simulation time")
    print("4. Exit\n")
    choice = input("Enter choice (1/2/3/4): ")
    print("\n")

    # total misses data cache
    if choice == '1':
        show_path(cpu_model, architecture, benchmark, parameter, "system.cpu.dcache.overallMisses::total")
        visualize(cpu_model,architecture,benchmark, parameter, "system.cpu.dcache.overallMisses::total")
        

    # total hits data cache
    elif choice == '2':
        show_path(cpu_model, architecture, benchmark, parameter, "system.cpu.dcache.overallHits::total")
        visualize(cpu_model,architecture,benchmark, parameter, "system.cpu.dcache.overallHits::total")

    # sim seconds
    elif choice == '3':
        show_path(cpu_model, architecture, benchmark, parameter, "simSeconds")
        visualize(cpu_model,architecture,benchmark, parameter, "simSeconds")

    elif choice == '4':
        print("Program terminated.")

    else:
        print("Invalid choice, please pick a valid option\n")
        statistic_menu(cpu_model, architecture, benchmark, parameter)

def show_path(cpu_model, architecture, benchmark, parameter, statistic):
    print(f"You have selected the path: ./stats/{cpu_model}/{architecture}/{benchmark}/{parameter}/{statistic}")


def extract_statistics(file_path, statistic):

    # List to store the extracted values
    statistics = []

    # Read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by spaces
            parts = line.split()
            if len(parts) >= 2:  # Ensure there are at least two parts
                # Check if the first part matches one of the options
                if parts[0] == statistic:
                    # Extract the value and store it in the list
                    value = float(parts[1])
                    statistics.append((statistic, value))

    return statistics


def process_directory(directory, statistic):
    # Define marker styles for each directory
    directory_marker_mapping = {
        "BiModeBP": 'o',  # Circle
        "LocalBP": '^',  # Triangle
        "TournamentBP": 's',  # Square
    }
    
    # Get the marker style for the current directory
    directory_marker = directory_marker_mapping.get(os.path.basename(directory), 'o')  # Default to circle

    # Define colors for each directory
    directory_color_mapping = {
        "BiModeBP": 'blue',
        "LocalBP": 'green',
        "TournamentBP": 'red',
    }
    
    # Get the color for the current directory
    directory_color = directory_color_mapping.get(os.path.basename(directory), 'blue')  # Default to blue
    
    # Lists to store x and y values for all files
    x_values = []
    y_values = []
    
    # Iterate over each text file in the directory
    for i, filename in enumerate(os.listdir(directory)):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            # Extract statistics from the file
            statistics = extract_statistics(file_path, statistic)
            # Append statistics to lists with the directory's marker style
            for stat, value in statistics:
                x_values.append(filename)
                y_values.append(value)
                plt.scatter(filename[:-4], value, marker=directory_marker, color=directory_color, label=filename[:-4])

    # Recursively process subdirectories
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            # Call process_directory for each subdirectory
            process_directory(subdir_path, statistic)

def visualize(cpu_model,architecture,benchmark, parameter, statistic):

    directory = f"./stats/{cpu_model}/{architecture}/{benchmark}/{parameter}"
    process_directory(directory, statistic)

    directory_color_mapping = {
        "BiModeBP": 'blue',
        "LocalBP": 'green',
        "TournamentBP": 'red',
    }
    custom_legend = []
    for directory, color in directory_color_mapping.items():
        custom_legend.append(plt.Line2D([0], [0], marker='o', color='w', label=directory, markerfacecolor=color, markersize=10))

    plt.legend(handles=custom_legend)

    
    label_x_mapping = {
            "system.cpu.dcache.overallMisses::total" : "Cache size and branch predictor" if parameter == "Cache" else "Replacement policy and branch predictor" ,
            "system.cpu.dcache.overallHits::total" : "Cache size and branch predictor",
            "simSeconds" : "Cache size and branch predictor" 
    }
    label_y_mapping = {
            "system.cpu.dcache.overallMisses::total" : "Count of Misses",
            "system.cpu.dcache.overallHits::total" : "Count of Hits",
            "simSeconds" : "Time (s)" 
    }
    title_mapping = {
            "system.cpu.dcache.overallMisses::total" : f"Data cache misses from a {benchmark} benchmark with the {architecture} using {cpu_model}",
            "system.cpu.dcache.overallHits::total" : f"Data cache hits from a {benchmark} benchmark with the {architecture} using {cpu_model}",
            "simSeconds" : f"Time the simulation takes to run from a {benchmark} benchmark with the {architecture} using {cpu_model}" 
    }
    # Customize plot appearance
    plt.xlabel(label_x_mapping[statistic])
    plt.ylabel(label_y_mapping[statistic])
    plt.title(title_mapping[statistic])
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    main_menu()

    