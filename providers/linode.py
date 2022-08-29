import json
import secrets
import string
import time

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

    def create_server(self, region: str, type_slug: str, image: str) -> Instance:
        regions = self.get_regions()
        alphabet = string.ascii_letters + string.digits
        root_pass = ''.join(secrets.choice(alphabet) for _ in range(16))

        if not regions.__contains__(region):
            raise ValueError(f"Linode has no region \"{region}\"")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "image": image,
            "region": region,
            "root_pass": root_pass,
            "type": type_slug
        }
        create_res = requests.post("https://api.linode.com/v4/linode/instances", json.dumps(data), headers=headers)

        if create_res.ok:
            create_data = create_res.json()
            instance = Instance(create_data["id"], create_data["ipv4"], root_pass)

            check_res = requests.get(f"https://api.linode.com/v4/linode/instances/{instance.instance_id}",
                                     headers=headers)
            while check_res.json()["status"] in ("provisioning", "booting"):
                status = check_res.json()["status"]
                print(f"Server {status}, stand-by...")
                time.sleep(5)
                check_res = requests.get(f"https://api.linode.com/v4/linode/instances/{instance.instance_id}",
                                         headers=headers)
            status = check_res.json()["status"]
            print(f"Server {status}")

            return instance
        else:
            raise ProviderError(f"An error occurred when creating server:\n{create_res.json()}")

    def destroy_server(self, instance: Instance):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.delete(f"https://api.linode.com/v4/linode/instances/{instance.instance_id}",
                                   headers=headers)
        if not response.ok:
            raise ProviderError(f"An error occurred when destroying server:\n{response.json()}")
