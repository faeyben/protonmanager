from pathlib import Path

import click

from .lib import install_proton_version, uninstall_proton_version, proton_version_stati, Proton, ProtonVersionAlreadyInstalledException, ProtonVersionIsNotInstalledException

import sys

@click.group()
def cli():
    """Manage custom versions of Proton, Steam's implementation of Wine."""
    pass

@cli.command()
@click.argument('version')
@click.option('--non-interactive', is_flag=True, default=False)
def install(version: str, non_interactive=False):
    """Install a custom Proton version. Available versions can be seen with the show command."""
    eprint(f"Installing Proton version {version}...")
    try:
        install_proton_version(version)
    except ProtonVersionAlreadyInstalledException:
        eprint("The requested Proton version is already installed")
        sys.exit(0)
    eprint(f"Successfully installed a new Proton version. Reminder: Steam needs to be restarted to show the new version.")

@cli.command()
@click.argument('version')
@click.option('--non-interactive', is_flag=True, default=False)
def uninstall(version: str, non_interactive: False):
    eprint(f"Uninstalling Proton version {version}...")
    try:
        uninstall_proton_version(version)
    except ProtonVersionIsNotInstalledException:
        eprint("The requested Proton version is not installed")
        sys.exit(0)
    eprint(f"Successfully uninstalled Proton version {version}.")

@cli.command()
def show():
    """Shows all installed custom Proton versions and a limited number of the latest releases."""
    for proton_version in proton_version_stati():
        if proton_version.installed:
            print(proton_version.version + "\t" + "INSTALLED")
        else:
            print(proton_version.version + "\t" + "NOT INSTALLED")

@cli.command()
@click.pass_context
def help(ctx):
    click.echo(ctx.parent.get_help())

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
if __name__ == '__main__':
    cli()
