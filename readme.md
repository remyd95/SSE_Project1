## Energy Profile Measurement Tool

## Requirements
- Linux OS (Tested on Ubuntu 22.04)
- Python3.10
- CUDA
- cuDNN
- [TensorFlow](https://www.tensorflow.org/install/pip#linux)
- [perfzero](https://github.com/tensorflow/benchmarks)
- [powerstat](https://snapcraft.io/install/powerstat/ubuntu)
- [psutil](https://pypi.org/project/psutil/)
- [tensorflow-model-optimization](https://www.tensorflow.org/model_optimization/guide/install)
- [python-bigquery](https://github.com/googleapis/python-bigquery)
- [cloud-tpu-client](https://pypi.org/project/cloud-tpu-client/)

## Installation
- Make sure to have all the requirements installed.
- Place the perfzero folder inside the root folder of this directory.
- Run with 'python3 energyprofile.py <#experiments/mode>'.

## Manual Preparations
- Close all user processes.
- Disable all notifications.
- Disable auto screen brightness adjustment.
- Turn down screen brightness to the lowest level
- Make sure the laptop is connected to a power supply.
- Unplug any external devices (USB/Screen/Drives/etc..).
- Take external factors into account (room temperature adjustments around sunset/sunrise).
- Make sure the laptop is placed in the same location on the same surface for the entire duration of the measurement.
