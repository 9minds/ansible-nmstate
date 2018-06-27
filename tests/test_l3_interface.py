#
# Copyright 2018 Red Hat, Inc.
#
# This file is part of ansible-nmstate.
#
# ansible-nmstate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ansible-nmstate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ansible-nmstate.  If not, see <https://www.gnu.org/licenses/>.
#
""" Unit tests for nmstate_l3_interface.py """

try:
    from unittest import mock
except ImportError:  # py2
    import mock

import sys
sys.modules['libnmstate'] = mock.Mock()
sys.modules['ansible'] = mock.Mock()
sys.modules['ansible.module_utils.basic'] = mock.Mock()
sys.modules['ansible.module_utils'] = mock.Mock()
sys.modules['ansible.module_utils.network.common'] = mock.Mock()
sys.modules['ansible.module_utils.network.common.utils'] = mock.Mock()
sys.modules['ansible.module_utils.network'] = mock.Mock()

import nmstate_l3_interface as nli  # noqa: E402

BASE_STATE = [
    {'name': 'eth0'},
    {'name': 'eth1'}
]


def test_get_interface_state():
    assert nli.get_interface_state(BASE_STATE, 'eth2') is None
    assert nli.get_interface_state(BASE_STATE, 'eth0') == BASE_STATE[0]
    assert nli.get_interface_state(BASE_STATE, 'eth1') == BASE_STATE[-1]


def test_set_ipv4_addresses():
    # test ip addresses are from:
    # https://tools.ietf.org/html/rfc5737
    ipv4 = '198.51.100.31/24'
    interface_state = nli.get_interface_state(BASE_STATE, 'eth0')
    new_state = nli.set_ipv4_addresses(interface_state, ipv4, False)
    assert len(new_state["ipv4"]["addresses"]) == 1
    assert new_state["ipv4"]["addresses"][0]["ip"] == ipv4.split("/")[0]

    # add second IP address
    ipv4_old = ipv4
    ipv4 = '192.0.2.8/24'
    new_state = nli.set_ipv4_addresses(new_state, ipv4, False)
    assert len(new_state["ipv4"]["addresses"]) == 2
    assert new_state["ipv4"]["addresses"][0]["ip"] == ipv4_old.split("/")[0]
    assert new_state["ipv4"]["addresses"][1]["ip"] == ipv4.split("/")[0]

    # Set only one address
    new_state = nli.set_ipv4_addresses(new_state, ipv4, True)
    assert len(new_state["ipv4"]["addresses"]) == 1
    assert new_state["ipv4"]["addresses"][0]["ip"] == ipv4.split("/")[0]

    # Set only one (different) address
    ipv4 = '203.0.113.5/24'
    new_state = nli.set_ipv4_addresses(new_state, ipv4, True)
    assert len(new_state["ipv4"]["addresses"]) == 1
    assert new_state["ipv4"]["addresses"][0]["ip"] == ipv4.split("/")[0]