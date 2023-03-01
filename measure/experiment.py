import subprocess
import time

from enum import Enum, auto

from measure.util import benchmark_cmd


class Type(Enum):
    PERFORMANCE = auto()
    BALANCED = auto()
    POWERSAVER = auto()


class Experiment:

    def __init__(self, experiment_type):
        self.type = experiment_type
        self.energy_consumption = 0
        self.runtime = 0

    def setup_env(self):
        print('\t Setting up environment..')
        if self.type == Type.POWERSAVER:
            power_mode = "power-saver"
        elif self.type == Type.BALANCED:
            power_mode = "balanced"
        elif self.type == Type.PERFORMANCE:
            power_mode = "performance"

        powerprofile_process = subprocess.Popen("powerprofilesctl set " + power_mode,
                                                stdin=subprocess.PIPE,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                shell=True)
        powerprofile_process.communicate()

    def run_benchmark(self):
        print('\t Running benchmark..')
        self.start_energy_measurement()
        benchmark_process = subprocess.Popen(benchmark_cmd(),
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             shell=True)

        benchmark_start = time.time()
        benchmark_process.communicate()
        benchmark_stop = time.time()

        self.stop_energy_measurement()
        self.energy_consumption = 1 # todo: get energy consumption from file
        self.runtime = benchmark_stop - benchmark_start

    def start_energy_measurement(self):
        # todo enable power measurement
        pass

    def stop_energy_measurement(self):
        # todo stop power measurement
        pass

    def pause(self):
        print('\t Pausing 1 min to cool down..')
        time.sleep(60)
        pass

    def run(self):
        self.setup_env()
        self.run_benchmark()
        self.pause()
        return (self.energy_consumption, self.run_time), self.type
