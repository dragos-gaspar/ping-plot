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
- Occasionally, the main thread will hang after the `pyplot`
window is manually closed, causing the exit logic for the ping
reading thread to be unreachable. (pls help)

### High level description

`main()` starts a separate thread via a `Pinger` instance, which
runs the `ping` command, polls its stdout and extracts the ping with
regex, storing it in its `frame` attribute, along with the current
datetime. Meanwhile, the main thread creates a `Plotter` instance
and stores `frame` inside it. `Plotter` starts the `matplotlib`
animation, plotting the data available  in `frame` every
`Config.PLOT_POLLING_INTERVAL` seconds. Access to `frame` is done
with a lock to avoid race conditions between threads. Once the
`pyplot` window is closed by the user, the `Pinger.stop` attribute
will be set from `main()`, prompting `Pinger` to exit its polling
loop and send `CTRL+C` to the spawned `ping` subprocess.
