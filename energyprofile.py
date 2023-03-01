import sys

from measure.profiler import Profiler


def calculate_significance(results):
    # Optional: calculate significance of the results
    pass


def plot_results(results):
    # TODO: plot the results in violin/boxplot
    print(results)


def main():
    print('Running Energy Profile Tool')

    if len(sys.argv) > 1:
        num_experiments = int(sys.argv[1])
    else:
        num_experiments = 5

    profiler = Profiler()
    profiler.create_experiments(num_experiments)
    profiler.shuffle_experiments()
    profiler.warmup()
    profiler.run_experiments()
    results = profiler.get_results()
    plot_results(results)
    calculate_significance(results)


if __name__ == "__main__":
    main()
