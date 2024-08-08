# srsr
Really Simple Service Registry - Python Client

## Description
This is the Python client for [srsr](https://github.com/ifIMust/srsr).

## Usage

### Typical
```
from srsrpy import srsrpy

# Store the client object for the lifetime of the service
c = srsrpy.ServiceRegistryClient('http://server.address.com:8080', 'service_name', 'http://client.address.net:3333')
# Returns True if registered
success = c.register()

# Carry on with the service duties. Heartbeats will be sent at the default interval.

# At teardown time, deregister
c.deregister()
```

### Shutdown using interrupt handler
```
import signal
try:
    svc_reg = ServiceRegistryClient('http://server_hostname', 'service_name', 'http://client_hostname')
    svc_reg.register()

    # Assume registration was successful. Deregister on Ctrl-C
    prev_handler = signal.getsignal(signal.SIGINT)
    def handle_sigint(sig, frame):
        svc_reg.deregister()

        if prev_handler:
            prev_handler(sig, frame)
    signal.signal(signal.SIGINT, handle_sigint)
except:
    print("Couldn't connect to registry server.")
```


## Further plans
- Publish the client to the PyPI production server
- Handle failed heartbeat, by stopping the thread.
