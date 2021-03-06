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

""" unit tests for nmstate_linkagg.py """

try:
    from unittest import mock
except ImportError:  # py2
    import mock

from testlib import ANSIBLE_MOCK_MODULES


with mock.patch.dict("sys.modules", ANSIBLE_MOCK_MODULES):
    # E402 module level import not at top of file
    import nmstate_linkagg as nla  # noqa: E402


def test_import_succeeded():
    assert nla
