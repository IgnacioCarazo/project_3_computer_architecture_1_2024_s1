import os
import matplotlib.pyplot as plt

def main_menu():
    print("\n")
    print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
    print("\n")
    print("Welcome to the visualizer tool, please choose which behaviour you want to visualize:\n")
    print("1. Minor CPU Model")
    print("2. Trace CPU")
    print("3. Exit\n")
    choice = input("Enter choice (1/2/3):")
    print("\n")

    if choice == '1':
        cpu_model_menu("MinorCPUModel")
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
    print("2. Politicas de reemplazo")
    print("3. Exit\n")
    choice = input("Enter choice (1/2/3): ")
    print("\n")

    if choice == '1':
        statistic_menu(cpu_model, architecture, benchmark, "CacheSize")
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
    print("3. Number of cpu cycles simulated")
    print("4. Exit\n")
    choice = input("Enter choice (1/2/3/4): ")
    print("\n")

    # total misses data cache
    if choice == '1':
        show_path(cpu_model, architecture, benchmark, parameter, "system.cpu.dcache.overallMisses::total")
        visualize(f"./stats/{cpu_model}/{architecture}/{benchmark}/{parameter}", "system.cpu.dcache.overallMisses::total")

    # total hits data cache
    elif choice == '2':
        show_path(cpu_model, architecture, benchmark, parameter, "system.cpu.dcache.overallHits::total")
        visualize(f"./stats/{cpu_model}/{architecture}/{benchmark}/{parameter}", "system.cpu.dcache.overallHits::total")

    # num cycles
    elif choice == '3':
        show_path(cpu_model, architecture, benchmark, parameter, "system.cpu.numCycles")
        visualize(f"./stats/{cpu_model}/{architecture}/{benchmark}/{parameter}", "system.cpu.numCycles")

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



def visualize(directory, statistic):
    def on_close(event):
        plt.close()
        print("\n")
        print("------------- ------------- ------------- ------------- ------------- ------------- ------------- ------------- \n")
        print("\n")
        print("Do you wish to keep using the program?\n")
        print("1. Yes")
        print("2. No")
        choice = input("Enter choice (1/2):")
        print("\n")

        if choice == '1':
            main_menu()
        elif choice == '2':
            print("Program terminated.")
        else:
            print("Invalid choice, please pick a valid option\n")
            main_menu()

    # Directory containing the text files

    # Dictionary to store colors for each file
    file_colors = {}

    # Lists to store x and y values for all files
    x_values = []
    y_values = []

    # Create a figure
    fig, ax = plt.subplots()

    # Connect the close event to the on_close function
    fig.canvas.mpl_connect('close_event', on_close)

    # Iterate over each text file in the directory
    for i, filename in enumerate(os.listdir(directory)):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            # Extract statistics from the file
            statistics = extract_statistics(file_path, statistic)
            # Generate a unique color for the file
            file_color = plt.cm.tab10(i)
            file_colors[filename] = file_color
            # Append statistics to lists with the file's color
            for stat, value in statistics:
                x_values.append(filename)
                y_values.append(value)
                plt.scatter(filename[:-4], value, color=file_color, label=filename[:-4])

    # Create a legend
    plt.legend(title='Stats')

    # Customize plot appearance
    plt.xlabel('VARIACIONES')
    plt.ylabel('VALORES')
    plt.title('TITULO')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    main_menu()

    