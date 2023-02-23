#!/usr/bin/env python
import pytest


def test_ansible_ping(host):
    """
    Test that ansible ping completes locally
    This test must run with the testinfra Ansible backend
    """
    assert host.ansible("ping")["ping"] == "pong"
