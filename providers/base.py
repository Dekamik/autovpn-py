from abc import abstractmethod


class Instance:
    def __init__(self, instance_id, ipv4, root_pass):
        self.instance_id = instance_id
        self.ipv4: str = ipv4
        self.root_pass: str = root_pass


class Provider:
    def __init__(self):
        pass

    @abstractmethod
    def get_regions(self, show_countries=False) -> list:
        pass

    @abstractmethod
    def create_server(self, region: str, type_slug: str, image: str) -> Instance:
        pass

    @abstractmethod
    def destroy_server(self, instance: Instance):
        pass
