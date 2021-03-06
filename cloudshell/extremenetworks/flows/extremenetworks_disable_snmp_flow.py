#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from cloudshell.snmp.snmp_parameters import SNMPV3Parameters

from cloudshell.extremenetworks.command_actions.enable_disable_snmp_actions import (
    EnableDisableSnmpActions,
)
from cloudshell.extremenetworks.flows.extremenetworks_enable_snmp_flow import ExtremenetworksEnableSnmpFlow


class ExtremenetworksDisableSnmpFlow(object):
    def __init__(self, cli_handler, logger):
        """Enable snmp flow.
        :param cli_handler:
        :type cli_handler:
        :param logger:
        :return:
        """
        self._cli_handler = cli_handler
        self._logger = logger

    def disable_flow(self, snmp_parameters):
        with self._cli_handler.get_cli_service(
            self._cli_handler.enable_mode
        ) as session:
            with session.enter_mode(self._cli_handler.config_mode) as config_session:
                snmp_actions = EnableDisableSnmpActions(config_session, self._logger)
                if "3" in snmp_parameters.version:
                    # todo disable snmpv3
                    current_snmp_user = snmp_actions.get_current_snmp_users()
                    if snmp_parameters.snmp_user in current_snmp_user:
                        snmp_actions.remove_snmp_v3_user(snmp_parameters.snmp_user)
                        # todo scan for groups?
                        # current_snmp_config = snmp_actions.get_current_snmp_config()
                        # groups = re.findall(
                        #     ExtremenetworksEnableSnmpFlow.DEFAULT_SNMP_GROUP, current_snmp_user
                        # )
                        # if len(groups) < 2:
                        #     snmp_actions.remove_snmp_group(
                        #         ExtremenetworksEnableSnmpFlow.DEFAULT_SNMP_GROUP
                        #     )
                        #     if (
                        #         "snmp-server view {}".format(
                        #             CiscoEnableSnmpFlow.DEFAULT_SNMP_VIEW
                        #         )
                        #         in current_snmp_config
                        #     ):
                        #         snmp_actions.remove_snmp_view(
                        #             ExtremenetworksEnableSnmpFlow.DEFAULT_SNMP_VIEW
                        #         )
                        snmp_actions.delete_snmpv3_group(ExtremenetworksEnableSnmpFlow.DEFAULT_SNMP_GROUP)
                else:
                    self._logger.debug("Start Disable SNMP")
                    snmp_actions.disable_snmp_v1v2()
                    snmp_actions.delete_snmp_community(snmp_parameters.snmp_community)
                #
            # with session.enter_mode(self._cli_handler.config_mode) as config_session:
            #     # Reentering config mode to perform commit for IOS-XR
            #     updated_snmp_actions = EnableDisableSnmpActions(
            #         config_session, self._logger
            #     )
            #     if isinstance(snmp_parameters, SNMPV3Parameters):
            #         updated_snmp_user = updated_snmp_actions.get_current_snmp_users()
            #         if snmp_parameters.snmp_user in updated_snmp_user:
            #             raise Exception(
            #                 self.__class__.__name__,
            #                 "Failed to remove SNMP v3 Configuration."
            #                 + " Please check Logs for details",
            #             )
            #     else:
            #         updated_snmp_communities = (
            #             updated_snmp_actions.get_current_snmp_config()
            #         )
            #         if re.search(
            #             "snmp-server community {}".format(
            #                 re.escape(snmp_parameters.snmp_community)
            #             ),
            #             updated_snmp_communities,
            #         ):
            #             raise Exception(
            #                 self.__class__.__name__,
            #                 "Failed to remove SNMP community."
            #                 + " Please check Logs for details",
            #             )