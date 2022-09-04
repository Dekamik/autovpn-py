#!/usr/bin/env python3
"""
AutoVPN

Automatically provisions and de-provisions single-use VPN servers for one-shot VPN sessions.

Usage: autovpn.py <provider> <region>
       autovpn.py <provider> regions
       autovpn.py providers
       autovpn.py (-h | --help)

Commands:
  <provider> <region>  create and connect to VPN endpoint at <provider> on <region>
  <provider> regions   list available regions for <provider>
  providers            list available providers

Arguments:
  <provider>  VPS provider to use
  <region>    VPS provider region on which to create VPN endpoint

Options:
  -h --help  show this
"""
import os
import sys

from docopt import docopt
import yaml

from providers.exceptions import ProviderError
from providers.linode import Linode
from providers.base import Provider
from utils import agent, openvpn


def is_provider_defined(provider, config) -> bool:
    return provider in config["providers"]


def get_provider(args, config) -> Provider:
    provider_arg = args["<provider>"]

    if provider_arg == "linode":
        return Linode(args, config)

    print(f"{provider_arg} is not a supported provider")
    sys.exit(1)


def up(args, config) -> int:
    global return_code
    return_code = 0

    provider_arg = args["<provider>"]
    if not is_provider_defined(provider_arg, config):
        print(f"{provider_arg} is not a supported provider")
        return 1

    region = args["<region>"]
    type_slug = config["providers"][provider_arg]["type_slug"]
    image = config["providers"][provider_arg]["image"]
    instance = None
    provider = None
    ovpn_config = None

    try:
        provider = get_provider(args, config)

        print("Creating server...")
        instance = provider.create_server(region, type_slug, image)

        print("Setup OpenVPN...")
        ovpn_config = agent.install_openvpn_server(instance, config)

        print("Opening session...")
        openvpn.connect(config, ovpn_config)

    except (ProviderError, ValueError) as ex:
        print(ex)
        return_code = 1

    except KeyboardInterrupt:
        print("Interrupted")
        return_code = 1

    finally:
        if provider is not None and instance is not None:
            print("Destroying server...")
            provider.destroy_server(instance)

        if ovpn_config is not None:
            print(f"Deleting {ovpn_config}...")
            os.remove(ovpn_config)

    return return_code


def show_regions(args, config) -> int:
    provider_arg = args["<provider>"]

    if not is_provider_defined(provider_arg, config):
        print(f"{provider_arg} is not a supported provider")
        return 1

    print("Downloading regions...")
    provider = get_provider(args, config)
    regions = provider.get_regions(True)
    print(*regions, sep="\n")

    return 0


def show_providers(config) -> int:
    print(*config["providers"].keys(), sep="\n")
    return 0


def main() -> int:
    with open("./config.yml", "r") as stream:
        config = yaml.safe_load(stream)

    args = docopt(__doc__)

    if args["regions"]:
        return show_regions(args, config)
    elif args["providers"]:
        return show_providers(config)
    else:
        return up(args, config)


if __name__ == '__main__':
    return_code = main()
    sys.exit(return_code)
