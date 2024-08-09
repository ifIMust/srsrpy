import requests
from threading import Thread, Event


class ServiceRegistryClient:
    def __init__(self, server_address, client_name,
                 client_address='', port=''):
        self.heartbeat_interval_seconds = 20
        self.server_address = server_address
        self.client_name = client_name
        self.client_address = client_address
        self.client_port = port

        self.is_registered = False
        self.client_id = ""
        self.heartbeat_thread = None
        self.stop = None

    def register(self):
        reg_data = {
            'name': self.client_name,
            'address': self.client_address,
            'port': self.client_port
        }
        try:
            r = requests.post(self.server_address + "/register", json=reg_data)
            if r.status_code == requests.codes.ok:
                resp_json = r.json()
                if 'id' in resp_json:
                    self.client_id = resp_json['id']
                    self.is_registered = True
                    self.stop = Event()
                    self.heartbeat_thread = Thread(target=self.keep_alive)
                    self.heartbeat_thread.start()
                    return True
        except requests.exceptions.ConnectionError:
            pass
        return False

    def deregister(self):
        if self.is_registered:
            self.stop.set()
            self.heartbeat_thread.join()
            self.is_registered = False
            dereg_data = {'id': self.client_id}
            try:
                requests.post(self.server_address + "/deregister",
                              json=dereg_data)
            except requests.exceptions.ConnectionError:
                pass

    def keep_alive(self):
        heartbeat_data = {'id': self.client_id}
        while not self.stop.is_set():
            stop_flag = self.stop.wait(self.heartbeat_interval_seconds)
            if not stop_flag:
                try:
                    requests.post(self.server_address + "/heartbeat",
                                  json=heartbeat_data)
                except requests.exceptions.ConnectionError:
                    pass
