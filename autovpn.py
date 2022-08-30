#!/usr/bin/env python3
"""
AutoVPN

Automatically provisions and de-provisions single-use VPN servers for one-shot VPN sessions.

Usage: autovpn.py up PROVIDER REGION
       autovpn.py regions PROVIDER
       autovpn.py providers
       autovpn.py (-h | --help)
       autovpn.py --version

Commands:
  up PROVIDER REGION  create and connect to VPN endpoint at PROVIDER on REGION
  regions PROVIDER    list available regions for PROVIDER
  providers           list available providers

Arguments:
  PROVIDER  VPS provider to use
  REGION    VPS provider region on which to create VPN endpoint

Options:
  -h --help         show help
  --version         show version
"""
import sys

from docopt import docopt
import yaml

from providers.exceptions import ProviderError
from providers.linode import Linode
from providers.base import Provider
from utils import agent


def is_provider_defined(provider, config) -> bool:
    return provider in config["providers"]


def get_provider(args, config) -> Provider:
    provider_arg = args["PROVIDER"]

    if provider_arg == "linode":
        return Linode(args, config)

    print(f"{provider_arg} is not a supported provider")
    sys.exit(1)


def up(args, config):
    provider_arg = args["PROVIDER"]
    if not is_provider_defined(provider_arg, config):
        print(f"{provider_arg} is not a supported provider")
        sys.exit(1)

    region = args["REGION"]
    type_slug = config["providers"][provider_arg]["type_slug"]
    image = config["providers"][provider_arg]["image"]

    try:
        provider = get_provider(args, config)

        print("Creating server...")
        instance = provider.create_server(region, type_slug, image)

        try:
            print("Setup OpenVPN...")
            agent.install_vpn_server(instance, config)

            print("Opening session...")
            agent.vpn_connect()

        finally:
            print("Destroying server...")
            provider.destroy_server(instance)

    except (ProviderError, ValueError) as ex:
        print(ex)
        sys.exit(1)


def show_regions(args, config):
    provider_arg = args["PROVIDER"]

    if not is_provider_defined(provider_arg, config):
        print(f"{provider_arg} is not a supported provider")
        sys.exit(1)

    print("Downloading regions...")
    provider = get_provider(args, config)
    regions = provider.get_regions(True)
    print(*regions, sep="\n")


def show_providers(config):
    print(*config["providers"].keys(), sep="\n")


def main():
    with open("./config.yml", "r") as stream:
        config = yaml.safe_load(stream)

    args = docopt(__doc__)

    if args["up"]:
        up(args, config)

    elif args["regions"]:
        show_regions(args, config)

    elif args["providers"]:
        show_providers(config)


if __name__ == '__main__':
    main()
    sys.exit(0)
