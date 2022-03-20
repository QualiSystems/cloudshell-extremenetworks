#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import os
from collections import OrderedDict

from cloudshell.cli.command_template.command_template_executor import (
    CommandTemplateExecutor,
)
from cloudshell.cli.session.session_exceptions import (
    CommandExecutionException,
    ExpectedSessionException,
)
from cloudshell.shell.flows.utils.networking_utils import UrlParser

from cloudshell.extremenetworks.command_templates import configuration
from cloudshell.extremenetworks.extremenetworks_constants import (
    PRIMARY_CONFIGURATION_FILENAME, SECONDARY_CONFIGURATION_FILENAME, TEMPORARY_CONFIGURATION_FILENAME
)
# from cloudshell.networking.cisco.command_templates import firmware


class SystemActions(object):

    # SAVED_CONFIGURATION_NAME = "saved_configuration"

    def __init__(self, cli_service, logger):
        """Reboot actions.

        :param cli_service: default mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    # @staticmethod
    # def prepare_action_map(source_file, destination_file):
    #     action_map = OrderedDict()
    #     if "://" in destination_file:
    #         url = UrlParser.parse_url(destination_file)
    #         dst_file_name = url.get(UrlParser.FILENAME)
    #         source_file_name = UrlParser.parse_url(source_file).get(UrlParser.FILENAME)
    #         action_map[
    #             r"[\[\(].*{}[\)\]]".format(dst_file_name)
    #         ] = lambda session, logger: session.send_line("", logger)
    #
    #         action_map[
    #             r"[\[\(]{}[\)\]]".format(source_file_name)
    #         ] = lambda session, logger: session.send_line("", logger)
    #     else:
    #         destination_file_name = UrlParser.parse_url(destination_file).get(
    #             UrlParser.FILENAME
    #         )
    #         url = UrlParser.parse_url(source_file)
    #
    #         source_file_name = url.get(UrlParser.FILENAME)
    #         action_map[
    #             r"(?!/)[\[\(]{}[\)\]]".format(destination_file_name)
    #         ] = lambda session, logger: session.send_line("", logger)
    #         action_map[
    #             r"(?!/)[\[\(]{}[\)\]]".format(source_file_name)
    #         ] = lambda session, logger: session.send_line("", logger)
    #     host = url.get(UrlParser.HOSTNAME)
    #     password = url.get(UrlParser.PASSWORD)
    #     username = url.get(UrlParser.USERNAME)
    #     if username:
    #         action_map[r"[Uu]ser(name)?"] = lambda session, logger: session.send_line(
    #             username, logger
    #         )
    #     if password:
    #         action_map[r"[Pp]assword"] = lambda session, logger: session.send_line(
    #             password, logger
    #         )
    #     if host:
    #         action_map[
    #             r"(?!/){}(?!/)\D*\s*$".format(host)
    #         ] = lambda session, logger: session.send_line("", logger)
    #
    #     return action_map

    # def upload(self, dst_address, filename):
    #     output = CommandTemplateExecutor(self._cli_service, configuration.UPLOAD).execute_command(address=dst_address,
    #                                                                                               filename=filename)

    # def copy(self, source, destination, vrf=None, action_map=None, error_map=None, timeout=180):
    #     output = CommandTemplateExecutor(
    #         self._cli_service,
    #         configuration.DEBUG_TRIGGER,
    #         action_map=action_map,
    #         error_map=error_map,
    #         timeout=timeout,
    #     ).execute_command()

    def save_configuration_locally(self, filename=None):
        self._logger.info("save_configuration_locally started")
        local_configuration_filename = filename if filename else TEMPORARY_CONFIGURATION_FILENAME
        self._logger.info("save config filename set to '{}'".format(local_configuration_filename))
        save_configuration_executor = CommandTemplateExecutor(self._cli_service, configuration.SAVE_CONFIGURATION)
        self._logger.info(f"preparing to execute {save_configuration_executor}")
        output = save_configuration_executor.execute_command(local_filename=local_configuration_filename)
        self._logger.info(f"received output from device: {output}")
        if self._verify_file_exists(local_configuration_filename + ".cfg"):
            return "{}.cfg".format(local_configuration_filename)
        else:
            raise CommandExecutionException("unable to save configuration locally: file does not exist")

    def tftp_put(self, remote_server_ip, local_filepath, remote_filepath=None, vr=None):
        if not vr:
            vr = None
        self._logger.info("tftp_put started")
        tftp_put_executor = CommandTemplateExecutor(self._cli_service, configuration.TFTP_PUT)
        self._logger.info(f"preparing to execute {tftp_put_executor}")
        output = tftp_put_executor.execute_command(
            remote_server_ip=remote_server_ip,
            local_filepath=local_filepath,
            remote_filepath=remote_filepath if remote_filepath else os.path.basename(local_filepath),
            vr=vr,
        )
        self._logger.info(f"received output from device: {output}")

    def tftp_get(self, remote_server_ip, remote_filepath, local_filepath=None, vr=None):
        if not vr:
            vr = None
        self._logger.info("tftp_put started")
        tftp_get_executor = CommandTemplateExecutor(self._cli_service, configuration.TFTP_GET)
        output = tftp_get_executor.execute_command(
            remote_server_ip=remote_server_ip,
            remote_filepath=remote_filepath,
            local_filepath=local_filepath if local_filepath else os.path.basename(remote_filepath),
            vr=vr
        )
        self._logger.info(f"received output from device: {output}")

    def rm(self, filepath):
        self._logger.info("rm started")
        output = CommandTemplateExecutor(self._cli_service, configuration.RM).execute_command(filepath=filepath)
        self._logger.info(f"received output from device: {output}")
        if self._verify_file_exists(filepath):
            raise CommandExecutionException("file exists after rm")

    def copy(self, src, dst):
        self._logger.info("copy started")
        output = CommandTemplateExecutor(self._cli_service, configuration.COPY).execute_command(src=src, dst=dst)
        self._logger.info(f"received output from device: {output}")
        if not self._verify_file_exists(dst):
            raise CommandExecutionException()

    def reboot(self, timeout=300):
        try:
            self._logger.info("Rebooting")
            reboot_executor = CommandTemplateExecutor(self._cli_service, configuration.REBOOT)
            output = reboot_executor.execute_command()
            self._logger.info(f"Received output from device: {output}")
        except ExpectedSessionException:
            time.sleep(10)
            self._logger.info("ExpectedSessionException thrown (expected), attempting to reconnect")
            self._cli_service.reconnect(timeout)
            self._logger.info("Reconnected")

    def use_configuration(self, filepath):
        self._logger.info("use_configuration started")
        if filepath.endswith(".cfg"):
            filepath = filepath[:-4]
            self._logger.info(f"trimmed .cfg off the filename, got {filepath}")
        output = CommandTemplateExecutor(self._cli_service, configuration.USE_CONFIGURATION).execute_command(filepath=filepath)
        self._logger.info(f"received output from device: {output}")
        if "The selected configuration file is now" not in output:
            raise CommandExecutionException("use configuration command unsuccessful")

    def _verify_file_exists(self, path):
        self._logger.info("_verify_file_exists started")
        output = CommandTemplateExecutor(self._cli_service, configuration.LS).execute_command(path=path)
        check_result = "No such file or directory" not in output
        self._logger.info(f"file {path} exists: {check_result}")
        return check_result

    def _current_selected_config(self):
        self._logger.info("_current_selected_config started")
        output = CommandTemplateExecutor(self._cli_service, configuration.SHOW_SWITCH).execute_command()
        self._logger.info(f"received output from device: {output}")
        selected_config_filename = re.search(r"Config Selected:\s+(.+.cfg)", output).group(1)
        self._logger.info(f"currently selected config defined as {selected_config_filename}")
        return selected_config_filename

    def _current_booted_config(self):
        self._logger.info("_current_booted_config started")
        output = CommandTemplateExecutor(self._cli_service, configuration.SHOW_SWITCH).execute_command()
        self._logger.info(f"received output from device: {output}")
        booted_config_filename = re.search(r"Config Booted:\s+(.+.cfg)", output).group(1)
        self._logger.info(f"currently booted config defined as {booted_config_filename}")
        return booted_config_filename

    # # # # # #

    def override_running(
        self,
        path,
        vrf=None,
        action_map=None,
        error_map=None,
        timeout=300,
        reconnect_timeout=1600,
    ):
        """Override running-config.

        :param path: relative path to the file on the remote host
            tftp://server/sourcefile
        :param action_map: actions will be taken during executing commands,
            i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands,
        i.e. handles Invalid Commands errors
        :raise Exception:
        """
        try:
            output = CommandTemplateExecutor(
                self._cli_service,
                configuration.CONFIGURE_REPLACE,
                action_map=action_map,
                error_map=error_map,
                timeout=timeout,
                check_action_loop_detector=False,
            ).execute_command(path=path, vrf=vrf)
            match_error = re.search(r"[Ee]rror.*", output, flags=re.DOTALL)
            if match_error:
                error_str = match_error.group()
                raise CommandExecutionException(
                    "Override_Running",
                    "Configure replace completed with error: " + error_str,
                )
        except ExpectedSessionException as e:
            self._logger.warning(e.args)
            if isinstance(e, CommandExecutionException):
                raise
            self._cli_service.reconnect(reconnect_timeout)

    def write_erase(self, action_map=None, error_map=None):
        """Erase startup configuration.

        :param action_map:
        :param error_map:
        """
        CommandTemplateExecutor(
            self._cli_service,
            configuration.WRITE_ERASE,
            action_map=action_map,
            error_map=error_map,
        ).execute_command()

    def reload_device(self, timeout, action_map=None, error_map=None):
        """Reload device.

        :param timeout: session reconnect timeout
        :param action_map: actions will be taken during executing commands,
            i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands,
            i.e. handles Invalid Commands errors
        """
        try:
            redundancy_reload = CommandTemplateExecutor(
                self._cli_service,
                configuration.REDUNDANCY_PEER_SHELF,
                action_map=action_map,
                error_map=error_map,
            ).execute_command()
            if re.search(
                r"[Ii]nvalid\s*([Ii]nput|[Cc]ommand)", redundancy_reload, re.IGNORECASE
            ):
                CommandTemplateExecutor(
                    self._cli_service,
                    configuration.RELOAD,
                    action_map=action_map,
                    error_map=error_map,
                ).execute_command()
            time.sleep(60)
        except Exception:
            self._logger.info("Device rebooted, starting reconnect")
        self._cli_service.reconnect(timeout)

    def get_flash_folders_list(self):
        output = CommandTemplateExecutor(
            self._cli_service, configuration.SHOW_FILE_SYSTEMS
        ).execute_command()

        match_dir = re.findall(
            r"(bootflash:|bootdisk:|flash-\d+\S+)", output, re.MULTILINE
        )
        if match_dir:
            return match_dir

    def reload_device_via_console(self, timeout=500, action_map=None, error_map=None):
        """Reload device.

        :param timeout: session reconnect timeout
        """
        CommandTemplateExecutor(
            self._cli_service,
            configuration.CONSOLE_RELOAD,
            action_map=action_map,
            error_map=error_map,
            timeout=timeout,
        ).execute_command()
        self._cli_service.session.on_session_start(
            self._cli_service.session, self._logger
        )

    def get_current_boot_config(self, action_map=None, error_map=None):
        """Retrieve current boot configuration.

        :param action_map: actions will be taken during executing commands,
            i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands,
            i.e. handles Invalid Commands errors
        :return:
        """
        return CommandTemplateExecutor(
            self._cli_service,
            firmware.SHOW_RUNNING,
            action_map=action_map,
            error_map=error_map,
        ).execute_command()

    def get_current_os_version(self, action_map=None, error_map=None):
        """Retrieve os version.

        :param action_map: actions will be taken during executing commands,
            i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands,
            i.e. handles Invalid Commands errors
        :return:
        """
        return CommandTemplateExecutor(
            self._cli_service,
            firmware.SHOW_VERSION,
            action_map=action_map,
            error_map=error_map,
        ).execute_command()

    def get_current_boot_image(self):
        current_firmware = []
        for line in self.get_current_boot_config().splitlines():
            if ".bin" in line:
                current_firmware.append(line.strip(" "))

        return current_firmware

    def shutdown(self):
        """Shutdown the system."""
        pass

# ######


class FirmwareActions(object):
    pass

    # def __init__(self, cli_service, logger):
    #     """Reboot actions.
    #
    #     :param cli_service: default mode cli_service
    #     :type cli_service: CliService
    #     :param logger:
    #     :type logger: Logger
    #     :return:
    #     """
    #     self._cli_service = cli_service
    #     self._logger = logger
    #
    # def add_boot_config_file(self, firmware_file_name):
    #     """Set boot firmware file.
    #
    #     :param firmware_file_name: firmware file nameSet boot firmware file.
    #
    #     :param firmware_file_name: firmware file name
    #     """
    #     CommandTemplateExecutor(
    #         self._cli_service, firmware.BOOT_SYSTEM_FILE
    #     ).execute_command(firmware_file_name=firmware_file_name)
    #     current_reg_config = CommandTemplateExecutor(
    #         self._cli_service, configuration.SHOW_VERSION_WITH_FILTERS
    #     ).execute_command(do="", filter="0x")
    #     if "0x2102" not in current_reg_config:
    #         CommandTemplateExecutor(
    #             self._cli_service, firmware.CONFIG_REG
    #         ).execute_command()
    #
    # def add_boot_config(self, boot_config_line):
    #     """Set boot firmware file.
    #
    #     :param boot_config_line: firmware file name
    #     """
    #     self._cli_service.send_command(boot_config_line)
    #
    # def clean_boot_config(self, config_line_to_remove, action_map=None, error_map=None):
    #     """Remove current boot from device.
    #
    #     :param config_line_to_remove: current boot configuration
    #     :param action_map: actions will be taken during executing commands,
    #         i.e. handles yes/no prompts
    #     :param error_map: errors will be raised during executing commands,
    #         i.e. handles Invalid Commands errors
    #     """
    #     self._logger.debug("Start cleaning boot configuration")
    #
    #     self._logger.info(
    #         "Removing '{}' boot config line".format(config_line_to_remove)
    #     )
    #     CommandTemplateExecutor(
    #         self._cli_service,
    #         configuration.NO,
    #         action_map=action_map,
    #         error_map=error_map,
    #     ).execute_command(command=config_line_to_remove.strip(" "))
    #
    #     self._logger.debug("Completed cleaning boot configuration")
