import os
import matplotlib.pyplot as plt
import pandas as pd

def main_menu():
    while True:
        print("\n")
        print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
        print("\n")
        print("Welcome to the visualizer tool, please choose which behaviour you want to visualize:\n")
        print("1. Minor CPU")
        print("2. O3CPU")
        print("3. Exit\n")
        choice = input("Enter choice (1/2/3):")
        print("\n")

        if choice == '1':
            cpu_model_menu("MinorCPU")
        elif choice == '2':
            cpu_model_menu("O3CPU")
        elif choice == '3':
            print("Program terminated.")
            break
        else:
            print("Invalid choice, please pick a valid option\n")

def cpu_model_menu(cpu_model):
    while True:
        print("\n")
        print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
        print("\n")
        print("Please select the architecture:\n")
        print("1. ARM")
        print("2. RISC-V")
        print("3. Back\n")
        choice = input("Enter choice (1/2/3): ")
        print("\n")

        if choice == '1':
            benchmark_menu(cpu_model, "ARM")
        elif choice == '2':
            benchmark_menu(cpu_model, "RISCV")
        elif choice == '3':
            break
        else:
            print("Invalid choice, please pick a valid option\n")

def benchmark_menu(cpu_model, architecture):
    while True:
        print("\n")
        print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
        print("\n")
        print("Please select the benchmark:\n")
        print("1. SPEC")
        print("2. PARSEC")
        print("3. Back\n")
        choice = input("Enter choice (1/2/3): ")
        print("\n")

        if choice == '1':
            parameter_menu(cpu_model, architecture, "SPEC")
        elif choice == '2':
            parameter_menu(cpu_model, architecture, "PARSEC")
        elif choice == '3':
            break
        else:
            print("Invalid choice, please pick a valid option\n")

def parameter_menu(cpu_model, architecture, benchmark):
    while True:
        print("\n")
        print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
        print("\n")
        print("Please select which parameter you want to see:\n")
        print("1. Cache size")
        print("2. Replacement policies")
        print("3. Back\n")
        choice = input("Enter choice (1/2/3): ")
        print("\n")

        if choice == '1':
            statistic_menu(cpu_model, architecture, benchmark, "Cache")
        elif choice == '2':
            statistic_menu(cpu_model, architecture, benchmark, "PdR")
        elif choice == '3':
            break
        else:
            print("Invalid choice, please pick a valid option\n")

def statistic_menu(cpu_model, architecture, benchmark, parameter):
    while True:
        print("\n")
        print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
        print("\n")
        print("Please select which parameter you want to see:\n")
        print("1. Data cache total misses")
        print("2. Data cache total hits")
        print("3. Cycles per instruction")
        print("4. Back\n")
        choice = input("Enter choice (1/2/3/4): ")
        print("\n")

        if choice == '1':
            show_path(cpu_model, architecture, benchmark, parameter, "system.cpu.dcache.overallMisses::total")
            visualize(cpu_model, architecture, benchmark, parameter, "system.cpu.dcache.overallMisses::total")
        elif choice == '2':
            show_path(cpu_model, architecture, benchmark, parameter, "system.cpu.dcache.overallHits::total")
            visualize(cpu_model, architecture, benchmark, parameter, "system.cpu.dcache.overallHits::total")
        elif choice == '3':
            show_path(cpu_model, architecture, benchmark, parameter, "system.cpu.cpi")
            visualize(cpu_model, architecture, benchmark, parameter, "system.cpu.cpi")
        elif choice == '4':
            break
        else:
            print("Invalid choice, please pick a valid option\n")

def show_path(cpu_model, architecture, benchmark, parameter, statistic):
    print(f"You have selected the path: ./stats/{cpu_model}/{architecture}/{benchmark}/{parameter}/{statistic}")

def extract_statistics(file_path, statistic):
    statistics = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 2 and parts[0] == statistic:
                value = float(parts[1])
                statistics.append((statistic, value))
    return statistics

def process_directory(directory, statistic, parameter, data):
    directory_marker_mapping = {
        "BiModeBP": 'o', 
        "LocalBP": '^',  
        "TournamentBP": 's',  
    }
    directory_marker = directory_marker_mapping.get(os.path.basename(directory), 'o')  

    directory_color_mapping = {
        "BiModeBP": 'blue',
        "LocalBP": 'green',
        "TournamentBP": 'red',
    }
    directory_color = directory_color_mapping.get(os.path.basename(directory), 'blue')  
    
    x_values = []
    y_values = []

    for filename in os.listdir(directory):
        cache_sizes = {"stats1.txt":"32KB", "stats2.txt":"64KB", "stats3.txt":"128KB", "stats4.txt":"256KB", "stats5.txt":"512KB"}
        pdr = {"stats1.txt":"LRU", "stats2.txt":"FIFO", "stats3.txt":"RANDOM", "stats4.txt":"MRU", "stats5.txt":"LFU"}
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            statistics = extract_statistics(file_path, statistic)
            for stat, value in statistics:
                x_parameter_label = cache_sizes[filename] if parameter == "Cache" else pdr[filename]
                label = f"{x_parameter_label}_{os.path.basename(directory)}"
                data.append((label.split('_')[0], value, os.path.basename(directory)))
                plt.scatter(label, value, marker=directory_marker, color=directory_color, label=filename[:-4])
                plt.annotate(f'{value}', (label, value), textcoords="offset points", xytext=(0,10), ha='right')

    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            process_directory(subdir_path, statistic, parameter, data)

def visualize(cpu_model, architecture, benchmark, parameter, statistic):
    plt.ion()  # Enable interactive mode
    plt.figure()  # Create a new figure
    data = []
    directory = f"./stats/{cpu_model}/{architecture}/{benchmark}/{parameter}"
    process_directory(directory, statistic, parameter, data)

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
            "system.cpu.dcache.overallMisses::total" : "Cache size and branch predictor" if parameter == "Cache" else "Replacement policy and branch predictor",
            "system.cpu.dcache.overallHits::total" : "Cache size and branch predictor",
            "system.cpu.cpi" : "Cache size and branch predictor" 
    }
    label_y_mapping = {
            "system.cpu.dcache.overallMisses::total" : "Count of dCache Misses",
            "system.cpu.dcache.overallHits::total" : "Count of dCache Hits",
            "system.cpu.cpi" : "Count of Cycles per Instruction" 
    }
    title_mapping = {
            "system.cpu.dcache.overallMisses::total" : f"Data cache misses from a {benchmark} benchmark with the {architecture} using {cpu_model}",
            "system.cpu.dcache.overallHits::total" : f"Data cache hits from a {benchmark} benchmark with the {architecture} using {cpu_model}",
            "system.cpu.cpi" : f"Cycles per instruction from a {benchmark} benchmark with {architecture} using {cpu_model}" 
    }
    statistic_mapping = {
            "system.cpu.dcache.overallMisses::total" : "Dcache-missess",
            "system.cpu.dcache.overallHits::total" : "Dcache-hits",
            "system.cpu.cpi" : "system.cpu.cpi" 
    }

    plt.xlabel(label_x_mapping[statistic])
    plt.ylabel(label_y_mapping[statistic])
    plt.title(title_mapping[statistic])
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    #  # Create a DataFrame with all the collected data
    # df = pd.DataFrame(data, columns=['Caché Size', label_y_mapping[statistic], 'Branch Predictor'])

    # plot_file_path = os.path.join('graphs', f'{cpu_model}_{architecture}_{benchmark}_{parameter}_{statistic_mapping[statistic]}.png')
    # plt.savefig(plot_file_path, bbox_inches='tight')

    
    # file_path = os.path.join('tables', f'{cpu_model}_{architecture}_{benchmark}_{parameter}_{statistic_mapping[statistic]}.xlsx')
    # df.to_excel(file_path, index=False)

# Start the program
main_menu()
