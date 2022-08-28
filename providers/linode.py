import json

import requests

from providers.base import Provider, Instance
from providers.exceptions import ProviderError


class Linode(Provider):
    def __init__(self, api_key):
        super().__init__()
        self.api_key: str = api_key

    def get_regions(self, show_countries=False) -> list:
        response = requests.get("https://api.linode.com/v4/regions")

        if response.ok:
            if show_countries:
                regions = [data["id"] + " (" + data["country"] + ")" for data in response.json()["data"]]
            else:
                regions = [data["id"] for data in response.json()["data"]]
            return regions

        raise ProviderError(f"Unhandled error when downloading regions:\n{response.json()}")

    def create_server(self, region: str, type_slug: str, authorized_keys: list) -> Instance:
        regions = self.get_regions()

        if not regions.__contains__(region):
            raise ValueError(f"Linode has no region \"{region}\"")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "authorized_keys": authorized_keys,
            "region": region,
            "type": type_slug
        }
        response = requests.post("https://api.linode.com/v4/linode/instances", json.dumps(data), headers=headers)

        if response.ok:
            res = response.json()
            return Instance(res["id"], res["ipv4"][0])
        else:
            raise ProviderError(f"An error occurred when creating server:\n{response.json()}")

    def destroy_server(self, instance: Instance):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{instance.instance_id}",
                                   headers=headers)
        if not response.ok:
            raise ProviderError(f"An error occurred when destroying server:\n{response.json()}")
