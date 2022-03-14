import os
from pathlib import Path
import requests
import json
from datetime import datetime
import tempfile
import tarfile
import shutil

PROTON_DIR = Path.home() / ".steam" / "steam" / "compatibilitytools.d"
RELEASES_URL = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases"

class ProtonVersionAlreadyInstalledException(Exception):
    pass

class ProtonVersionIsNotInstalledException(Exception):
    pass

class Proton:
    def __init__(self, version: str, installed: bool, published_at: int):
        self.version = version
        self.installed = installed
        self.published_at = published_at

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.version == other.version
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.published_at > other.published_at

    def __lt__(self, other):
        return not self.__gt__(other)

def install_proton_version(version: str) -> None:
    if _is_proton_version_installed(version):
        raise ProtonVersionAlreadyInstalledException()

    release = requests.get(RELEASES_URL + "/tags/" + version).json()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as dldir:
        for asset in release["assets"]:
            if not asset['name'].endswith(".tar.gz"):
                continue
            r = requests.get(asset["browser_download_url"], stream=True)
            with open(Path(dldir) / asset['name'], "wb") as dlfile:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    dlfile.write(chunk)
        targz = tarfile.open(Path(dldir) / (version + ".tar.gz") )
        targz.extractall(PROTON_DIR)
        targz.close()

def uninstall_proton_version(version: str) -> None:
    if not _is_proton_version_installed(version):
        raise ProtonVersionIsNotInstalledException()

    for installed_version in os.listdir(PROTON_DIR):
        with open(PROTON_DIR / installed_version / "version") as f:
            if version == f.read().split(" ")[1].strip():
                shutil.rmtree(PROTON_DIR / installed_version)
                break

def proton_version_stati() -> list:
    results = []

    for installed_version in os.listdir(PROTON_DIR):
        
        results.append(
            Proton(
                version=_get_installed_proton_version_string(installed_version),
                installed=True,
                published_at=_get_installed_proton_publishdate(installed_version)
                )
            )

    for available_version in _get_ge_proton_releases():
        if available_version not in results:
            results.append(available_version)

    return sorted(results)

def _is_proton_version_installed(version: str) -> bool:
    for installed_version in os.listdir(PROTON_DIR):
        with open(PROTON_DIR / installed_version / "version") as f:
            if version == f.read().split(" ")[1].strip():
                return True
    return False

def _get_installed_proton_version_string(version: str) -> str:
    """Gets the actual Proton version string from the version file

    The dir name might not be equal to the actual Proton version string.
    """
    with open(PROTON_DIR / version / "version") as f:
        return f.read().split(" ")[1].strip()

def _get_installed_proton_publishdate(version: str) -> int:
    with open(PROTON_DIR / version / "version") as f:
        return int(f.read().split(" ")[0])

def _convert_datestring_to_timestamp(datestring: str) -> int:
    dt = datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%SZ") # e.g. 2022-03-05T08:28:10Z
    return int(dt.timestamp())

def _get_ge_proton_releases(amount=30) -> list:
    releases = []
    response = requests.get(RELEASES_URL, params={'per_page': amount}).json()
    for release in response:
        if release["draft"]:
            continue

        releases.append(
            Proton(
                version=release["tag_name"],
                published_at=_convert_datestring_to_timestamp(release["published_at"]),
                installed=False
            )
        )

    return releases