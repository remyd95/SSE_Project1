def benchmark_cmd():
    return 'python3 benchmarks/perfzero/lib/benchmark.py ' \
           '--git_repos="https://github.com/tensorflow/models.git;benchmark" --python_path=models ' \
           '--gcloud_key_file_url="" ' \
           '--benchmark_methods=official.benchmark.keras_cifar_benchmark' \
           '.Resnet56KerasBenchmarkSynth.benchmark_1_gpu_no_dist_strat'


def fibonacci_of(n):
    if n in {0, 1}:
        return n
    return fibonacci_of(n - 1) + fibonacci_of(n - 2)
