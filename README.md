# srsr
Really Simple Service Registry - Python Client

## Description
This is the Python client for [srsr](https://github.com/ifIMust/srsr).

## Usage
Import the srsrpy package in your project.
As long as your service can be shutdown cleanly, the client is easy to use:
```
# Store the client object for the lifetime of the service
c = ServiceRegistryClient('http://server.address.com:8080', 'service_name', 'http://client.address.net:3333')
c.register()

# Carry on with the service duties. Heartbeats will be sent at the default interval.

# At teardown time, deregister
c.deregister()
```
