#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.cli.configurator import AbstractModeConfigurator
from cloudshell.cli.service.cli import CLI
from cloudshell.cli.service.cli_service_impl import CliServiceImpl
from cloudshell.cli.service.command_mode_helper import CommandModeHelper
from cloudshell.cli.service.session_pool_manager import SessionPoolManager
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.session.telnet_session import TelnetSession

from cloudshell.extremenetworks.extremenetworks_constants import DEFAULT_SESSION_POOL_TIMEOUT
# from cloudshell.extremenetworks.cli.extreme_command_modes import (  # todo
#     ConfigCommandMode,
#     # DefaultCommandMode,
#     EnableCommandMode,
# )

from cloudshell.extremenetworks.cli.extreme_command_modes import DefaultCommandMode as CommandMode

from cloudshell.extremenetworks.sessions.console_ssh_session import ConsoleSSHSession
# from cloudshell.extremenetworks.sessions.console_telnet_session import (  # todo
#     ConsoleTelnetSession,
# )


class ExtremeCli(object):
    def __init__(self, resource_config, pool_timeout=DEFAULT_SESSION_POOL_TIMEOUT):
        session_pool_size = int(resource_config.sessions_concurrency_limit)
        session_pool = SessionPoolManager(
            max_pool_size=session_pool_size, pool_timeout=pool_timeout
        )
        self.cli = CLI(session_pool=session_pool)

    def get_cli_handler(self, resource_config, logger):
        return ExtremeCliHandler(self.cli, resource_config, logger)


class ExtremeCliHandler(AbstractModeConfigurator):
    REGISTERED_SESSIONS = (
        SSHSession,
        # TelnetSession,
        # ConsoleSSHSession,
        # ConsoleTelnetSession,
    )

    def __init__(self, cli, resource_config, logger):
        super(ExtremeCliHandler, self).__init__(resource_config, logger, cli)
        # self.modes = CommandModeHelper.create_command_mode(resource_config)
        self.modes = CommandModeHelper.create_command_mode(resource_config)

    # @property
    # def default_mode(self):
    #     return self.modes[DefaultCommandMode]
    #
    # @property
    # def enable_mode(self):
    #     return self.modes[EnableCommandMode]
    #
    # @property
    # def config_mode(self):
    #     return self.modes[ConfigCommandMode]

    @property
    def enable_mode(self):
        return self.modes[CommandMode]

    @property
    def config_mode(self):
        return self.modes[CommandMode]

    def _on_session_start(self, session, logger):
        cli_service = CliServiceImpl(
            session=session, requested_command_mode=self.enable_mode, logger=logger
        )
        cli_service.send_command("disable cli paging")
    #
    # def _on_session_start(self, session, logger):
    #     """Send default commands to configure/clear session outputs.
    #
    #     :return:
    #     """
    #     cli_service = CliServiceImpl(
    #         session=session, requested_command_mode=self.enable_mode, logger=logger
    #     )
    #     cli_service.send_command("terminal length 0", EnableCommandMode.PROMPT)
    #     cli_service.send_command("terminal width 300", EnableCommandMode.PROMPT)
    #     cli_service.send_command(
    #         "terminal no exec prompt timestamp", EnableCommandMode.PROMPT
    #     )
    #     with cli_service.enter_mode(self.config_mode) as config_session:
    #         config_session.send_command("no logging console", ConfigCommandMode.PROMPT)
