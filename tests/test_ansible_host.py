#!/usr/bin/env python
import pytest
from packaging import version


@pytest.fixture
def vagrant_home():
    return "/home/vagrant"


def test_is_linux_host(host):
    """This is linux"""
    assert host.system_info.type == "linux"
    assert host.system_info.arch == "x86_64"


def test_vagrant_user(host, vagrant_home):
    """Test that the vagrant user exists"""
    assert host.user("vagrant").exists
    assert host.user("vagrant").group == "vagrant"
    assert host.user("vagrant").home == vagrant_home


def test_is_git_installed(host):
    """Git is installed and at least a minimum version"""
    git_installed_version = host.package("git").version
    git_min_version = "2.3"
    assert host.package("git").is_installed
    assert version.parse(git_installed_version) >= version.parse(git_min_version)


def test_is_python_installed(host):
    """Python 3 is installed and at least a minimum version"""
    python_installed_version = host.package("python3").version
    python_min_version = "3.9"
    assert host.package("python3").is_installed
    assert version.parse(python_installed_version) >= version.parse(python_min_version)


def test_is_pip_installed(host):
    """Pip is installed and no broken dependencies"""
    pip_min_version = "22"
    assert host.pip.is_installed
    assert version.parse(host.pip("pip").version) >= version.parse(pip_min_version)
    assert host.pip.check().succeeded


def test_python_venv(host, vagrant_home):
    """The virtual environment is there"""
    assert host.file(vagrant_home + "/py39").exists


@pytest.mark.parametrize(
    "pkgname,pkgver",
    [
        ("ansible", "6.5"),
        ("ansible-lint", "6.8"),
        ("Jinja2", "3"),
        ("pytest", "7.1"),
        ("pytest-testinfra", "6.8"),
        ("yamllint", "1.28"),
    ],
)
def test_pip_package_min_versions(host, pkgname, pkgver, vagrant_home):
    """Test python packages are installed in the virtual environment"""
    pkg = host.pip.get_packages(pip_path=vagrant_home + "/py39/bin/pip")[pkgname]
    assert version.parse(pkg["version"]) >= version.parse(pkgver)
