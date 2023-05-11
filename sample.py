#!/usr/bin/env python
import click
from argparse import ArgumentParser
import dateutil.parser
import eero
from eero.cookie_store import CookieStore
import json
import pandas as pd

session = CookieStore("session.cookie")
eero = eero.Eero(session)

COMMANDS = [
    'details',
    'device',
    'devices',
    'eeros',
    'info',
    'login',
    'networks',
    'reboot',
    'summary',
    'speedtest',
    'speedtests',
    'clients',
    'diagnostics',
    'resources',
    'forwards',
    'reservations',
    'profiles'
]

def print_json(data, sort=True):
    click.echo(json.dumps(data, indent=4, sort_keys=sort))


@click.group()
def cli():
    # This makes click work.
    pass


@cli.command()
def login():
    """ Login to eero API """
    if not eero.needs_login():
        click.echo("Already logged in. Not required.")
    else:
        eero_login = click.prompt("Your eero login (email address or phone number): ")
        user_token = eero.login(eero_login)
        verification_code = click.prompt("Your eero verification code: ")
        eero.login_verify(verification_code, user_token)
        click.echo("Login successful. Rerun this command to get some output.")


def account_info():
    return eero.account()


@cli.command()
def account():
    """ Show your eero user account details """
    print_json(account_info())


@cli.command()
def devices():
    """ Show all the devices connected to your network """
    for network in account_info()["networks"]["data"]:
        devices = eero.devices(network["url"])
        print_json(devices)


@cli.command()
def reservations():
    """ Show all network reservations """
    for network in account_info()["networks"]["data"]:
        network_id = eero.id_from_url(network["url"])
        results = eero.reservations(network_id)
        print_json(results, False)


@cli.command()
def forwards():
    """ Show all network port forwarding rules """
    for network in account_info()["networks"]["data"]:
        network_id = eero.id_from_url(network["url"])
        results = eero.forwards(network_id)
        print_json(results, False)


@cli.command()
def profiles():
    """ Show all account and network profiles """
    for network in account_info()["networks"]["data"]:
        network_id = eero.id_from_url(network["url"])
        results = eero.profiles(network_id)
        print_json(results, False)


@cli.command()
def diagnostics():
    """ Show all network diagnostics """
    for network in account_info()["networks"]["data"]:
        network_id = eero.id_from_url(network["url"])
        results = eero.diagnostics(network_id)
        print_json(results, False)


@cli.command()
@click.option("--last", is_flag=True, default=False)
def speedtests():
    """ Show your recent network speed test results """
    for network in account_info()["networks"]["data"]:
        network_id = eero.id_from_url(network["url"])
        results = eero.get_speed_test(network_id)
        if last:
            print_json(results[0])
        else:
            print_json(results, False)


@cli.command()
def speedtest():
    """ Run a new network speed test """
    for network in account_info()["networks"]["data"]:
        network_id = eero.id_from_url(network["url"])
        print("Running speed test...")


@cli.command()
@click.option("--verbose", is_flag=True, default=False)
def eeros(verbose):
    """ Shows all the eeros on your network """
    summary_erros = []
    for network in account_info()["networks"]["data"]:
        es = eero.eeros(network["url"])
        for e in es:
            if verbose:
                print_json(e)
                return
            ds = {}
            ds["serial"] = e["serial"]
            ds["location"] = e["location"]
            ds["connected_clients_count"] = e["connected_clients_count"]
            ds["status"] = e["status"]
            ds["wired"] = e["wired"]
            ds["using_wan"] = e["using_wan"]
            ds["gateway"] = e["gateway"]
            ds["ip_address"] = e["ip_address"]
            ds["nightlight"] = e["nightlight"]
            ds["mesh_quality_bars"] = e["mesh_quality_bars"]
            ds["last_heartbeat"] = e["last_heartbeat"]
            summary_erros.append(ds)
    df = pd.DataFrame.from_dict(summary_erros, orient="columns")
    print(df)


@cli.command()
@click.argument("network_id")
@click.argument("device_id")
def device(network_id, device_id):
    """ Prints out the information for a specific device """
    print_json(eero.device(network_id, device_id))


def get_bitrate(bitrate):
    if bitrate is None:
        return 0
    return bitrate.split(" ")[0]


@cli.command()
@click.option("--recent", is_flag=True, default=True)
def summary(recent):
    """ Summary of your network """
    summary_score = []
    for network in account_info()["networks"]["data"]:
        devices = eero.devices(network["url"])
        for device in devices:
            ds = {}
            ds["nickname"] = device["nickname"]
            ds["hostname"] = device["hostname"]
            ds["manufacturer"] = device["manufacturer"]
            ds["con_rx_bitrate"] = get_bitrate(device["connectivity"]["rx_bitrate"])
            ds["con_score"] = device["connectivity"]["score"]
            ds["con_score_bar"] = device["connectivity"]["score_bars"]
            ds["usage"] = device["usage"]
            ds["location"] = device["source"]["location"]
            ds["last_active"] = dateutil.parser.isoparse(
                device["last_active"]
            ).strftime("%Y-%m-%d %H:%M:%S")
            ds["id"] = device["url"].split("/")[-1]

            summary_score.append(ds)
    df = pd.DataFrame.from_dict(summary_score, orient="columns")
    click.echo(df)


@cli.command()
def networks():
    """ Shows available networks. (Generally one) """
    for network in account_info()["networks"]["data"]:
        print(network["url"])


@cli.command()
def details():
    """ Show your network configuration in detail. (Generally one) """
    for network in account_info()["networks"]["data"]:
        network_details = eero.networks(network['url'])
        print_json(network_details, False)


@cli.command()
def resources():
    """ Show your network resources. """
    for network in account_info()["networks"]["data"]:
        resources = eero.resources(network['url'])
        print_json(resources, False)


@cli.command()
def info():
    """ Show your network info. (Generally one) """
    for network in account_info()["networks"]["data"]:
        print_json(network, False)


@cli.command()
@click.argument("--device")
def reboot(device):
    """ Reboot an eero """
    click.echo(f"Rebooting device: {device}...")
    eero.reboot(device)


if __name__ == "__main__":
    cli()
