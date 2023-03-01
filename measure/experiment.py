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

        powerstat_process = subprocess.Popen("sudo powerstat 1 60 -R -D -i 90% &", shell=True, stdout=subprocess.PIPE)
        benchmark_process = subprocess.Popen(benchmark_cmd(),
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             shell=True)
        print('\t\t Starting power measurement')
        powerstat_process.wait()
        time.sleep(5)
        print('\t\t Starting benchmark task')
        benchmark_start = time.time()
        benchmark_process.wait()
        benchmark_stop = time.time()

        #Obtain energy consumption in Watts
        for outputline in powerstat_process.stdout:
            if "CPU:" in outputline.decode('utf-8'):
                self.energy_consumption = float(outputline.decode('utf-8').split()[1])

        self.runtime = benchmark_stop - benchmark_start
        print('\t\t Obtained runtime: ' + str(round(self.runtime, 2)) + 's & Average energy consumption: ' + str(self.energy_consumption) + 'W')

    def pause(self):
        print('\t Cooldown pause')
        time.sleep(60)
        pass

    def run(self):
        self.setup_env()
        self.run_benchmark()
        self.pause()
        return (self.energy_consumption, self.runtime), self.type
