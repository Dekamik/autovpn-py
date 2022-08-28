from abc import abstractmethod


class Instance:
    def __init__(self, instance_id, ip_address):
        self.instance_id = instance_id
        self.ip_address: str = ip_address


class Provider:
    def __init__(self):
        pass

    @abstractmethod
    def get_regions(self, show_countries=False) -> list:
        pass

    @abstractmethod
    def create_server(self, region: str, type_slug: str, authorized_keys: list) -> Instance:
        pass

    @abstractmethod
    def destroy_server(self, instance: Instance):
        pass
