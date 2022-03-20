#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template_executor import (
    CommandTemplateExecutor,
)
from cloudshell.cli.session.session_exceptions import CommandExecutionException

from cloudshell.extremenetworks.command_templates import enable_disable_snmp
import re


class EnableDisableSnmpActions(object):

    def __init__(self, cli_service, logger):
        self._cli_service = cli_service
        self._logger = logger

    # def enable_snmpv3(self):
    #     CommandTemplateExecutor(cli_service=self._cli_service, command_template=enable_disable_snmp.ENABLE_SNMP_V3)
    #
    # def enable_snmpv1v2(self):
    #     CommandTemplateExecutor(cli_service=self._cli_service, command_template=enable_disable_snmp.ENABLE_SNMP_V1V2)

    def get_current_snmp_users(self, action_map=None, error_map=None):
        output = CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.SHOW_SNMP_USER,
            action_map=action_map,
            error_map=error_map,
        ).execute_command()
        return re.findall(r"User Name\s+\:\s+(.+)", output)

    # def get_current_snmp_config(self, action_map=None, error_map=None):
    #     return CommandTemplateExecutor(
    #         cli_service=self._cli_service,
    #         command_template=enable_disable_snmp.SHOW_SNMP_CONFIG,
    #         action_map=action_map,
    #         error_map=error_map,
    #     ).execute_command()

    def get_current_snmp_views(self, action_map=None, error_map=None):
        output = CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.SHOW_SNMP_VIEW,
            action_map=action_map,
            error_map=error_map,
            check_action_loop_detector=False,  # todo
        ).execute_command()
        return re.findall(r"View Name\s+\:\s+(.+)", output)

    def enable_snmp_view(self, snmp_view, action_map=None, error_map=None):
        return CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.ENABLE_SNMP_VIEW,
            action_map=action_map,
            error_map=error_map,
        ).execute_command(snmp_view=snmp_view)

    def get_current_snmp_groups(self, action_map=None, error_map=None):
        output = CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.SHOW_SNMP_GROUPS,
            action_map=action_map,
            error_map=error_map,
            check_action_loop_detector=False,  # todo
        ).execute_command()
        return re.findall(r"Group Name\s+\:\s+(.+)", output)

    def enable_snmp_group(self, snmp_group, snmp_view, action_map=None, error_map=None):
        return CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.CREATE_SNMP_V3_GROUP,
            action_map=action_map,
            error_map=error_map,
        ).execute_command(snmp_group=snmp_group, snmp_view=snmp_view)

    def delete_snmpv3_group(self, snmp_group):
        return CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.DELETE_SNMP_V3_GROUP,
        ).execute_command(snmp_group=snmp_group)

    def enable_snmp_v3_access(self):
        CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.ENABLE_SNMP_V3
        ).execute_command()

    def disable_snmp_v3_access(self):
        CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.DISABLE_SNMP_V3
        ).execute_command()

    def create_snmp_v3_user(self, user, password, auth_protocol, priv_key, priv_protocol):
        CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.CREATE_SNMP_V3_USER,
        ).execute_command(
            snmp_user=user,
            snmp_password=password,
            auth_protocol=auth_protocol,
            snmp_priv_key=priv_key,
            priv_protocol=priv_protocol,
        )

    def remove_snmp_v3_user(self, user):
        # todo check if user exists before deletion and check if it doesnt after deletion?
        CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.REMOVE_SNMP_V3_USER
        ).execute_command(snmp_user=user)

    def associate_snmp_v3_user_group(self, user, group):
        CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.ASSOC_USER_SNMP_V3_GROUP,
        ).execute_command(snmp_user=user, snmp_group=group)

    def enable_snmp_v1v2(self):
        CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.ENABLE_SNMP_V1V2,
        ).execute_command()

    def disable_snmp_v1v2(self):
        CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.DISABLE_SNMP_V1V2,
        ).execute_command()

    def create_snmp_community(self, snmp_community):
        # todo readonly?
        CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.CREATE_SNMP_COMMUNITY,
        ).execute_command(snmp_community=snmp_community)

    def delete_snmp_community(self, snmp_community):
        # todo readonly?
        CommandTemplateExecutor(
            cli_service=self._cli_service,
            command_template=enable_disable_snmp.DELETE_SNMP_COMMUNITY,
        ).execute_command(snmp_community=snmp_community)

    # def enable_snmp_v3(
    #     self,
    #     snmp_user,
    #     snmp_password,
    #     auth_protocol,
    #     snmp_priv_key,
    #     priv_protocol,
    #     snmp_group,
    #     action_map=None,
    #     error_map=None,
    # ):
    #     # enable snmp v3 access
    #     CommandTemplateExecutor(
    #         cli_service=self._cli_service,
    #         command_template=enable_disable_snmp.ENABLE_SNMP_V3
    #     ).execute_command()
    #
    #     # create user
    #     CommandTemplateExecutor(
    #         cli_service=self._cli_service,
    #         command_template=enable_disable_snmp.CREATE_SNMP_V3_USER,
    #         action_map=action_map,
    #         error_map=error_map,
    #     ).execute_command(
    #         snmp_user=snmp_user,
    #         snmp_password=snmp_password,
    #         auth_protocol=auth_protocol,
    #         snmp_priv_key=snmp_priv_key,
    #         priv_protocol=priv_protocol,
    #     )
    #
    #     # associate user with group
    #     CommandTemplateExecutor(
    #         cli_service=self._cli_service,
    #         command_template=enable_disable_snmp.ASSOC_USER_SNMP_V3_GROUP,
    #         action_map=action_map,
    #         error_map=error_map,
    #     ).execute_command(snmp_user=snmp_user, snmp_group=snmp_group)

        # if snmp_group:
        #     try:
        #         result = CommandTemplateExecutor(
        #             cli_service=self._cli_service,
        #             command_template=enable_disable_snmp.ENABLE_SNMP_V3_WITH_GROUP,
        #             action_map=action_map,
        #             error_map=error_map,
        #         ).execute_command(
        #             snmp_user=snmp_user,
        #             snmp_password=snmp_password,
        #             auth_protocol=auth_protocol,
        #             snmp_priv_key=snmp_priv_key,
        #             priv_protocol=priv_protocol,
        #             snmp_group=snmp_group,
        #         )
        #     except CommandExecutionException:
        #         result = CommandTemplateExecutor(
        #             cli_service=self._cli_service,
        #             command_template=enable_disable_snmp.ENABLE_SNMP_V3_WITH_GROUP,
        #             action_map=action_map,
        #             error_map=error_map,
        #         ).execute_command(
        #             snmp_user=snmp_user,
        #             snmp_password=snmp_password,
        #             auth_protocol=auth_protocol,
        #             snmp_priv_key=snmp_priv_key,
        #             priv_protocol=priv_protocol.replace("-", " "),
        #             snmp_group=snmp_group,
        #         )
        # else:
        #     result = CommandTemplateExecutor(
        #         cli_service=self._cli_service,
        #         command_template=enable_disable_snmp.ENABLE_SNMP_USER,
        #         action_map=action_map,
        #         error_map=error_map,
        #     ).execute_command(
        #         snmp_user=snmp_user,
        #         snmp_password=snmp_password,
        #         auth_protocol=auth_protocol,
        #         snmp_priv_key=snmp_priv_key,
        #         priv_protocol=priv_protocol,
        #     )
        # return result

    # READ_ONLY = "ro"
    # READ_WRITE = "rw"
    #

    #
    # def get_current_snmp_communities(self, action_map=None, error_map=None):
    #     """Retrieve current snmp communities.
    #     :param action_map: actions will be taken during executing commands,
    #         i.e. handles yes/no prompts
    #     :param error_map: errors will be raised during executing commands,
    #         i.e. handles Invalid Commands errors
    #     :return:
    #     """
    #     return CommandTemplateExecutor(
    #         cli_service=self._cli_service,
    #         command_template=enable_disable_snmp.SHOW_SNMP_COMMUNITY,
    #         action_map=action_map,
    #         error_map=error_map,
    #     ).execute_command()
    #

    #
    # def get_current_snmp_user(self, action_map=None, error_map=None):
    #     """Retrieve current snmp communities.
    #     :param action_map: actions will be taken during executing commands,
    #         i.e. handles yes/no prompts
    #     :param error_map: errors will be raised during executing commands,
    #         i.e. handles Invalid Commands errors
    #     :return:
    #     """
    #     return CommandTemplateExecutor(
    #         cli_service=self._cli_service,
    #         command_template=enable_disable_snmp.SHOW_SNMP_USER,
    #         action_map=action_map,
    #         error_map=error_map,
    #     ).execute_command()
    #
    # def enable_snmp(
    #     self,
    #     snmp_community,
    #     is_read_only_community=True,
    #     action_map=None,
    #     error_map=None,
    # ):
    #     """Enable SNMP on the device.
    #     :param snmp_community: community name
    #     :param action_map: actions will be taken during executing commands,
    #         i.e. handles yes/no prompts
    #     :param error_map: errors will be raised during executing commands,
    #         i.e. handles Invalid Commands errors
    #     """
    #     read_only = self.READ_WRITE
    #     if is_read_only_community:
    #         read_only = self.READ_ONLY
    #     return CommandTemplateExecutor(
    #         cli_service=self._cli_service,
    #         command_template=enable_disable_snmp.ENABLE_SNMP,
    #         action_map=action_map,
    #         error_map=error_map,
    #     ).execute_command(snmp_community=snmp_community, read_only=read_only)
    #

    #

    #

    #
    # def disable_snmp(self, snmp_community, action_map=None, error_map=None):
    #     """Disable SNMP community on the device.
    #     :param snmp_community: community name
    #     :param action_map: actions will be taken during executing commands,
    #         i.e. handles yes/no prompts
    #     :param error_map: errors will be raised during executing commands,
    #         i.e. handles Invalid Commands errors
    #     """
    #     return CommandTemplateExecutor(
    #         cli_service=self._cli_service,
    #         command_template=enable_disable_snmp.DISABLE_SNMP_COMMUNITY,
    #         action_map=action_map,
    #         error_map=error_map,
    #     ).execute_command(snmp_community=snmp_community)
    #
    # def remove_snmp_group(self, snmp_group, action_map=None, error_map=None):
    #     """Disable SNMP community on the device.
    #     :param snmp_group: community name
    #     :param action_map: actions will be taken during executing commands,
    #         i.e. handles yes/no prompts
    #     :param error_map: errors will be raised during executing commands,
    #         i.e. handles Invalid Commands errors
    #     """
    #     return CommandTemplateExecutor(
    #         cli_service=self._cli_service,
    #         command_template=enable_disable_snmp.DISABLE_SNMP_GROUP,
    #         action_map=action_map,
    #         error_map=error_map,
    #     ).execute_command(snmp_group=snmp_group)
    #
    # def remove_snmp_view(self, snmp_view, action_map=None, error_map=None):
    #     """Disable SNMP view on the device.
    #     :param snmp_view: community name
    #     :param action_map: actions will be taken during executing commands,
    #         i.e. handles yes/no prompts
    #     :param error_map: errors will be raised during executing commands,
    #         i.e. handles Invalid Commands errors
    #     """
    #     try:
    #         CommandTemplateExecutor(
    #             cli_service=self._cli_service,
    #             command_template=enable_disable_snmp.DISABLE_SNMP_VIEW,
    #             action_map=action_map,
    #             error_map=error_map,
    #         ).execute_command(snmp_view=snmp_view)
    #     except CommandExecutionException:
    #         CommandTemplateExecutor(
    #             cli_service=self._cli_service,
    #             command_template=enable_disable_snmp.DISABLE_SNMP_VIEW,
    #             action_map=action_map,
    #             error_map=error_map,
    #         ).execute_command(snmp_view=snmp_view, mib_oid="")
    #
    # def remove_snmp_user(
    #     self, snmp_user, snmp_group=None, action_map=None, error_map=None
    # ):
    #     """Disable SNMP user on the device.
    #     :param snmp_user: snmp v3 user name
    #     :param action_map: actions will be taken during executing commands,
    #         i.e. handles yes/no prompts
    #     :param error_map: errors will be raised during executing commands,
    #         i.e. handles Invalid Commands errors
    #     """
    #     if snmp_group:
    #         result = CommandTemplateExecutor(
    #             cli_service=self._cli_service,
    #             command_template=enable_disable_snmp.DISABLE_SNMP_USER_WITH_GROUP,
    #             action_map=action_map,
    #             error_map=error_map,
    #         ).execute_command(snmp_user=snmp_user, snmp_group=snmp_group)
    #     else:
    #         result = CommandTemplateExecutor(
    #             cli_service=self._cli_service,
    #             command_template=enable_disable_snmp.DISABLE_SNMP_USER,
    #             action_map=action_map,
    #             error_map=error_map,
    #         ).execute_command(snmp_user=snmp_user)
    #     return result