#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell.flows.configuration.basic_flow import AbstractConfigurationFlow

# from cloudshell.extremenetworks.extremenetworks_constants import DEFAULT_FILE_SYSTEM
from cloudshell.extremenetworks.command_actions.system_actions import SystemActions
from cloudshell.shell.flows.utils.networking_utils import UrlParser
from cloudshell.extremenetworks.extremenetworks_constants import (
    PRIMARY_CONFIGURATION_FILENAME, SECONDARY_CONFIGURATION_FILENAME, CONFIGURATION_FILES
)


class ExtremeConfigurationFlow(AbstractConfigurationFlow):
    STARTUP_CONFIG_NAME = "startup_config"
    STARTUP_LOCATION = "nvram:startup_config"

    def __init__(self, cli_handler, resource_config, logger):
        super(ExtremeConfigurationFlow, self).__init__(logger, resource_config)
        self._cli_handler = cli_handler

    @property
    def _file_system(self):
        return ""

    # def _save_flow(self, folder_path, configuration_type, vrf_management_name=None):
    #     # todo configuration type ?
    #     parsed_url = UrlParser.parse_url(folder_path)
    #     with self._cli_handler.get_cli_service(
    #         self._cli_handler.enable_mode
    #     ) as session:
    #         system_actions = SystemActions(session, self._logger)
    #         local_configuration_name = system_actions.save_configuration_locally()
    #         system_actions.tftp_put(
    #             remote_server_ip=parsed_url[UrlParser.HOSTNAME],
    #             local_filepath=local_configuration_name,
    #             remote_filepath=parsed_url[UrlParser.FILENAME],
    #             vr=vrf_management_name,
    #         )
    #         system_actions.rm(local_configuration_name)

    def _save_flow(self, folder_path, configuration_type, vrf_management_name=None):
        # todo protocol support
        self._logger.info("_save_flow started")
        parsed_url = UrlParser.parse_url(folder_path)
        with self._cli_handler.get_cli_service(
            self._cli_handler.enable_mode
        ) as session:
            system_actions = SystemActions(session, self._logger)
            if configuration_type == "running":
                local_configuration_name = system_actions.save_configuration_locally()
                system_actions.tftp_put(
                    remote_server_ip=parsed_url[UrlParser.HOSTNAME],
                    local_filepath=local_configuration_name,
                    remote_filepath=parsed_url[UrlParser.FILENAME],
                    vr=vrf_management_name,
                )
                system_actions.rm(local_configuration_name)
            elif configuration_type == "startup":
                booted_configuration_name = system_actions._current_booted_config()
                system_actions.tftp_put(
                    remote_server_ip=parsed_url[UrlParser.HOSTNAME],
                    local_filepath=booted_configuration_name,
                    remote_filepath=parsed_url[UrlParser.FILENAME],
                    vr=vrf_management_name,
                )
            else:
                raise Exception(f"Unable to perform save action for configuration type {configuration_type}")
            self._logger.info(f"_save_flow finished")

    def _restore_flow(self, path, configuration_type, restore_method, vrf_management_name=None):
        self._logger.info(f"_restore_flow started")
        if configuration_type not in ("startup", "running"):
            raise Exception(f"wrong configuration type {configuration_type}")
        parsed_url = UrlParser.parse_url(path)
        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as session:
            system_actions = SystemActions(session, self._logger)
            selected_configuration_name = system_actions._current_selected_config()
            switch_to_configuration_name = (CONFIGURATION_FILES - {selected_configuration_name}).pop()
            system_actions.rm(switch_to_configuration_name)
            system_actions.tftp_get(
                remote_server_ip=parsed_url[UrlParser.HOSTNAME],
                remote_filepath=parsed_url[UrlParser.FILENAME],
                local_filepath=switch_to_configuration_name,
                vr=vrf_management_name,
            )
            system_actions.use_configuration(switch_to_configuration_name)
            if configuration_type == "running":
                system_actions.reboot()
            self._logger.info(f"_restore_flow finished")

    @staticmethod
    def _validate_configuration_type(configuration_type):
        print("running/startup verification suppressed")  # todo implement valid logic in terms of conf naming for exos
        pass