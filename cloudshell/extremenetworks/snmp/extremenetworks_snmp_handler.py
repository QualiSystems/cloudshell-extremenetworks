#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.snmp.snmp_configurator import (
    EnableDisableSnmpConfigurator,
    EnableDisableSnmpFlowInterface,
)

from cloudshell.extremenetworks.flows.extremenetworks_disable_snmp_flow import ExtremenetworksDisableSnmpFlow
from cloudshell.extremenetworks.flows.extremenetworks_enable_snmp_flow import ExtremenetworksEnableSnmpFlow


class ExtremenetworksEnableDisableSnmpFlow(EnableDisableSnmpFlowInterface):
    DEFAULT_SNMP_VIEW = "quali_snmp_view"
    DEFAULT_SNMP_GROUP = "quali_snmp_group"

    def __init__(self, cli_handler, logger):
        """Enable snmp flow.
        :param cli_handler:
        :param logger:
        :return:
        """
        self._logger = logger
        self._cli_handler = cli_handler

    def enable_snmp(self, snmp_parameters):
        ExtremenetworksEnableSnmpFlow(self._cli_handler, self._logger).enable_flow(
            snmp_parameters
        )

    def disable_snmp(self, snmp_parameters):
        ExtremenetworksDisableSnmpFlow(self._cli_handler, self._logger).disable_flow(
            snmp_parameters
        )


class ExtremenetworksSnmpHandler(EnableDisableSnmpConfigurator):
    def __init__(self, resource_config, logger, cli_handler):
        self.cli_handler = cli_handler
        enable_disable_snmp_flow = ExtremenetworksEnableDisableSnmpFlow(self.cli_handler, logger)
        super(ExtremenetworksSnmpHandler, self).__init__(
            enable_disable_snmp_flow, resource_config, logger
        )
