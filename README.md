# ping-plot
Simple tool for visualising ping times to a target host using
`matplotlib`. The underlying implementation reads ping times from
the stdout of a `ping` subprocess.

## Overview

Tested with Python 3.9 under Windows 10.

### How to run

#### Install requirements.txt
```commandline
pip install -r requrements.txt
```
#### Run the main script
```commandline
python ping-plot.py -i <HOST_IP>
```
or
```commandline
python ping-plot.py --help
```

Other options can be configured by modifying values in `config.py`.

### Known issues
- Occasionally, the main thread will hang after manually closing the
`matplotlib` window, causing the exit logic for the ping thread to
be unreachable. (pls help)
