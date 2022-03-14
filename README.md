# Protonmanager

A simple commandline interface to install or uninstall the [custom proton versions made by GloriousEggroll](https://github.com/GloriousEggroll/proton-ge-custom).

## Install & Uninstall

I recommend installation using [pipx](https://github.com/pypa/pipx).

```
git clone https://github.com/faeyben/protonmanager.git
pipx install --spec ./protonmanager protonmanager
```

Alternatively, with `pip`:

```
git clone https://github.com/faeyben/protonmanager.git
pip install ./protonmanager
```

Uninstalling the application is equally simple.

`pipx uninstall protonmanager` or `pip uninstall protonmanager`

## Usage

### Show available and installed versions

`protonmanager show`

### Install a new GE Proton version

`protonmanager install GE-Proton7-9`

### Uninstall a GE Proton version

`protonmanager uninstall GE-Proton7-9`

