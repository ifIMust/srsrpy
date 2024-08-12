# srsr
Really Simple Service Registry - Python Client

## Description
This is the Python client for [srsr](https://github.com/ifIMust/srsr).

## Usage

### Typical
```
from srsrpy import srsrpy

# Store the client object for the lifetime of the service
# If the client's address and port bindings are known, specify:
c = srsrpy.ServiceRegistryClient('http://server.address.com:8080', 'service_name', 'http://client.address.net:3333')

# Alternatively, omit the address and specify the client port only.
# The server will assume http scheme and try to deduce the client IP.
c = srsrpy.ServiceRegistryClient('http://server.address.com:8080', 'service_name', port='3333')

# Returns True if registered. After this point, a thread is active for heartbeats.
success = c.register()

# Carry on with the service duties. Heartbeats will be sent at the default interval.

# At teardown time, deregister
c.deregister()
```

### Example shutdown using interrupt handler
```
import signal
svc_reg = ServiceRegistryClient('http://server_hostname', 'service_name', 'http://client_hostname')
success = svc_reg.register()

if success:
   prev_handler = signal.getsignal(signal.SIGINT)
   def handle_sigint(sig, frame):
        svc_reg.deregister()

        if prev_handler:
            prev_handler(sig, frame)
    signal.signal(signal.SIGINT, handle_sigint)
```


## Further plans
- Handle failed heartbeat, by stopping the thread.
