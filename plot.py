from json import load
import matplotlib.pyplot as plt
from sort_lib import insertion_sort_alg
from sort_lib import bubble_sort_alg
from sort_lib import merge_sort_alg
from timeit import repeat


def run_algorithm(algorithm, n):
    '''
    Receives:   algorithm: a string indicating the name of a sorting
                function to call.

                n: an integer indicating the number of files to sort.

    The function uses timeit.repeat to calculate the number of seconds
    it takes to run an algorithm 1000 times.

    It repeats this 3 times and saves the times as a list.
    Source: This function was supplied as part of the assignment.

    Returns: A list of floats inciating times in seconds.
    '''
    # To give the timeit module access to functions you define, you can
    # pass a setup parameter which contains an import statement:
    setup_code = f"from __main__ import {algorithm}"

    # call to the function as text. Repeats the execution.
    times = repeat(f"{algorithm}({n})", setup=setup_code, repeat=3,
                   number=1000)
    # Pay attention to the fact that the output is the execution time of number
    # times iteration of the code snippet, not the single iteration.
    # For a single iteration exec. time, divide the output time by number.
    return times


def get_data():
    '''
    Opens and loads json data from web scraping.
    
    '''
    with open("file_data.json", "r") as input_file:
        file_data = load(input_file)        
    return file_data


def setup_data_to_sort_time_plot():
    '''
    Sets up the tuple algs_data.
    Each list in the tuple algs_data contains the following:
        element 0 = The name of the sorting algorithm function. (string)        

        element 1 = The x coordinates of the data to plot. (list of integers)

        element 2 = The y coordinates of the data to plot. (list of floats)

        element 3 = The name of the algorithm to print in the legend. (string)

        element 4 = The marker to use in the plot as described in
                    https://matplotlib.org/3.3.2/api/markers_api.html#module-matplotlib.markers (string)
    Returns algs_data
    '''
    algs_data = (
                ["insertion_sort_alg", [], [], "Insertion Sort", "*"],
                ["bubble_sort_alg", [], [], "Bubble Sort", "o"],
                ["merge_sort_alg", [], [], "Merge Sort", "d"]
                )
    return algs_data


def main():
    '''
    Calls get_data to set up the list of unsorted file_data.
    file_data is a list containing lists of image names (strings) and file sizes (int).

    Calls setup_data_to_sort_time_plot to obtain algs_data for holding the data to plot.

    The structure of algs_data is explained in the documentation for the
    setup_data_to_sort_time_plot function.

    For each sorting algorithm:
        Calls run_algorithm to get timing data for different numbers of files.

        Number of files is saved as X-coordinates.

        The minimum times from the lists returned by run_algorithm are saved as
        y-coordinates.

        Writes some debugging info to log_file.

        The data is sent to the plt.plot function.
    The axis labels and legend for the plot are generated.
    The plot is saved.
    '''
    file_data = get_data()
    algs_data = setup_data_to_sort_time_plot()
    with open("timing_data_log_file.txt", "w") as log_file:
        for i in range(len(algs_data)):         # For each sorting algorithm
            for n in range(100, 2301, 200):     # Number of files to sort    
                # Get lowest time from run_algorithm function
                times = min(run_algorithm(algs_data[i][0], file_data[:n]))
                algs_data[i][1].append(n)       # Save x-coordinate data in algs_data
                algs_data[i][2].append(times)   # Save y-coordinate data in algs_data
            log_file.write(f"X-coordinates for algorithm {algs_data[i][0]} are {algs_data[i][1]}\n")
            log_file.write(f"Y-coordinates for algorithm {algs_data[i][0]} are {algs_data[i][2]}\n\n\n")
            log_file.flush()

            plt.plot(algs_data[i][1], algs_data[i][2], linewidth=1.0,
                     label=algs_data[i][3], marker=algs_data[i][4])
    plt.xlabel('Number of files')       # X-axis label
    plt.ylabel('Execution time (ms)')   # Y-axis label
    plt.legend()
    plt.savefig('plot_of_sorting_times.png')


main()
