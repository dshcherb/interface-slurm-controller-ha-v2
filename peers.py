# Copyright 2017 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import charms.reactive as reactive
import socket

from charmhelpers.contrib.templating.contexts import dict_keys_without_hyphens


class ControllerHA(reactive.Endpoint):

    @reactive.when('endpoint.{endpoint_name}.joined')
    def provide_peer_data(self, hostname=socket.gethostname()):
        # technically, there is only one peer relation but we have a list
        for rel in self.relations:
            rel.to_publish['hostname'] = hostname

    @property
    def peer_data(self):
        peer_data = {}
        if self.relations:
            # only one peer relation is ever present for a given endpoint
            rel = self.relations[0]
            # only one HA peer is expected
            assert len(rel.joined_units) < 2
            peer_data = dict_keys_without_hyphens(
                rel.joined_units[0].received)
        return peer_data
