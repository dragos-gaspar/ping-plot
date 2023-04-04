# ping-plot
Simple tool for visualising ping times to a target host using
<samp>matplotlib</samp>. The underlying implementation reads ping times from
the stdout of a <samp>ping</samp> subprocess.

## Overview

Tested with Python 3.9 under Windows 10.

### How to run

#### Install requirements.txt
```commandline
pip install -r requrements.txt
```
#### Run the main script
```commandline
python ping-plot.py -i HOST_IP
```
or
```commandline
python ping-plot.py --help
```

Other options can be configured by modifying values in <samp>config.py</samp>.

### Known issues
- Occasionally, the main thread will hang after the <samp>pyplot</samp>
window is manually closed, causing the exit logic for the ping
reading thread to be unreachable. EDIT: using <samp>wxWidgets</samp> as
a backend for <samp>matplotlib</samp> seems to fix this.

### High level description

<samp>main()</samp> starts a separate thread via a <samp>Pinger</samp> instance, which
runs the <samp>ping</samp> command, polls its stdout and extracts the ping with
regex, storing it in its <samp>frame</samp> attribute, along with the current
datetime. Meanwhile, the main thread creates a <samp>Plotter</samp> instance
and stores <samp>Pinger.frame</samp> inside it. <samp>Plotter</samp> starts the <samp>matplotlib</samp>
animation (in the main thread), plotting the data available  in <samp>Pinger.frame</samp> every
<samp>Config.PLOT_POLLING_INTERVAL</samp> seconds. Access to <samp>Pinger.frame</samp> is done
with a lock to avoid race conditions between threads. Once the
<samp>pyplot</samp> window is closed by the user, the <samp>Pinger.stop</samp> attribute
will be set from <samp>main()</samp>, prompting <samp>Pinger</samp> to exit its polling
loop and send <samp>CTRL+C</samp> to the spawned <samp>ping</samp> subprocess.
