## Energy Profile Measurement Tool

## Requirements
- Linux OS (Tested on Ubuntu 22.04)
- Python3.10
<!-- - [psutil](https://pypi.org/project/psutil/)
- [tensorflow-model-optimization](https://www.tensorflow.org/model_optimization/guide/install)
- [python-bigquery](https://github.com/googleapis/python-bigquery)
- [cloud-tpu-client](https://pypi.org/project/cloud-tpu-client/) -->

## Installation
- Make sure you install [CUDA, cuDNN, and TensorFlow](https://www.tensorflow.org/install/pip#linux).
- Run `git clone https://github.com/tensorflow/benchmarks.git` inside the root directory to install the [perfzero benchmark](https://github.com/tensorflow/benchmarks).
- Install [powerstat](https://snapcraft.io/install/powerstat/ubuntu) using `sudo apt install powerstat`
- Run `pip install -r requirements.txt` to install the remainder of dependencies
- Run with `python3 energyprofile.py <#experiments>` which runs #experiments * 3 (balanced, power-saving, performance) times with a default of 5 and a minimum of 1.

## Manual Preparations
- Close all user processes.
- Disable all notifications.
- Disable auto screen brightness adjustment.
- Turn down screen brightness to the lowest level
- Make sure the laptop is connected to a power supply.
- Unplug any external devices (USB/Screen/Drives/etc..).
- Take external factors into account (room temperature adjustments around sunset/sunrise).
- Make sure the laptop is placed in the same location on the same surface for the entire duration of the measurement.
