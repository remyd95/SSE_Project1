import random
import subprocess
import time

from measure.util import fibonacci_of, benchmark_cmd
from measure.experiment import Type, Experiment


class Profiler:

    def __init__(self):
        self.results = {}
        self.experiments = list()
        self.initialize_results()

    def create_experiments(self, num_experiments):
        print('\t Creating ' + str(num_experiments) + ' experiments per energy mode')

        for i in range(num_experiments):
            self.experiments.append(Experiment(Type.POWERSAVER))
            self.experiments.append(Experiment(Type.BALANCED))
            self.experiments.append(Experiment(Type.PERFORMANCE))

    def shuffle_experiments(self):
        print('\t Shuffling ' + str(len(self.experiments)) + ' experiments for fair measurements')
        random.shuffle(self.experiments)

    def raise_priviliges(self):
        print('\t Raising priviliges to superuser')

        raise_privilige_process = subprocess.Popen("sudo echo Success",
                                                   stdin=subprocess.PIPE,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   shell=True)
        raise_privilige_process.communicate()

    def reset_env(self):
        print('\t Setting environment to balanced for warmup')

        powerprofile_process = subprocess.Popen("powerprofilesctl set balanced",
                                                stdin=subprocess.PIPE,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                shell=True)
        powerprofile_process.communicate()

    def run_experiments(self):
        print('Running experiments:')
        for idx, exp in enumerate(self.experiments):
            print('[' + str(idx + 1) + '/' + str(len(self.experiments)) + '] Starting experiment:')
            result, exptype = exp.run()
            self.results[exptype].append(result)
        print("Finished all experiments.")

    def initialize_results(self):
        print('Creating result container..')
        self.results.setdefault(Type.POWERSAVER, [])
        self.results.setdefault(Type.BALANCED, [])
        self.results.setdefault(Type.PERFORMANCE, [])

    def get_results(self):
        print('Gathering results...')
        return self.results

    def warmup(self):
        print('Warming up hardware..')

        print('\tWarming up CPU')
        start = time.time()
        while time.time() - start < 60:
            fibonacci_of(40)
        print('\tWarming up GPU')
        benchmark_process = subprocess.Popen(benchmark_cmd(),
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             shell=True)
        benchmark_process.communicate()
