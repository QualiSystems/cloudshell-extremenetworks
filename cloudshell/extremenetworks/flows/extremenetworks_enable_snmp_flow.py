#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from cloudshell.snmp.snmp_parameters import SNMPV3Parameters

from cloudshell.extremenetworks.command_actions.enable_disable_snmp_actions import (
    EnableDisableSnmpActions,
)


# enable snmp on device:
#   enable snmp access {snmp-v1v2c | snmpv3}
#   disable snmp access {snmp-v1v2c | snmpv3}

# enable snmp access vr [vr_name | all]
# disable snmp access vr [vr_name | all]

# Display the SNMP configuration and statistics on a VR:
# show snmp {vr} vr_name

#
# To view SNMP settings configured on the switch, use the following command:
# show management

#
# To create a user, use the following command:
# configure snmpv3 add user [[hex hex_user_name] | user_name]
# {authentication [md5 | sha] [hex hex_auth_password | auth_password]}
# {privacy {des | 3des | aes {128 | 192 | 256}} [[hex hex_priv_password]
# | priv_password]} }{volatile}

# A number of default users are initially available. These user names are: admin, initial, initialmd5,
# initialsha, initialmd5Priv, initialshaPriv. The default password for admin is password. For the other
# default users, the default password is the user name.

# • To display information about a user, or all users, use the following command:
# show snmpv3 user {[[hex hex_user_name] | user_name]}

# • To delete a user, use the following command:
# configure snmpv3 delete user [all | [[hex hex_user_name] | user_name]
# {engine-id engine_id}]

# show snmpv3 mib-view

class ExtremenetworksEnableSnmpFlow(object):

    DEFAULT_SNMP_VIEW = "quali_snmp_view"
    DEFAULT_SNMP_GROUP = "quali_snmp_group"
    COMPATIBLE_PRIV_PROTOCOL = {
        "des": "des",
        "3des-ede": "3des",
        "aes-128": "aes 128",
        "aes-192": "aes 192",
        "aes-256": "aes 256",
    }

    def __init__(self, cli_handler, logger):
        """Enable snmp flow.
        :param cli_handler:
        :param logger:
        :return:
        """
        self._logger = logger
        self._cli_handler = cli_handler

    def enable_flow(self, snmp_parameters):
        if "3" not in snmp_parameters.version and not snmp_parameters.snmp_community:
            message = "SNMP community cannot be empty"
            self._logger.error(message)
            raise Exception(message)

        with self._cli_handler.get_cli_service(
            self._cli_handler.enable_mode
        ) as config_session:
            # with session.enter_mode(self._cli_handler.config_mode) as config_session:
            snmp_actions = EnableDisableSnmpActions(config_session, self._logger)
            if "3" in snmp_parameters.version:
                snmp_actions.enable_snmp_v3_access()
                current_snmp_users = snmp_actions.get_current_snmp_users()  # so if user exists just skip everything
                if snmp_parameters.snmp_user not in current_snmp_users:
                    snmp_parameters.validate()
                    # view
                    current_snmp_views = snmp_actions.get_current_snmp_views()
                    if self.DEFAULT_SNMP_VIEW not in current_snmp_views:
                        snmp_actions.enable_snmp_view(self.DEFAULT_SNMP_VIEW)
                    # group
                    current_snmp_groups = snmp_actions.get_current_snmp_groups()
                    if self.DEFAULT_SNMP_GROUP not in current_snmp_groups:
                        snmp_actions.enable_snmp_group(
                            snmp_group=self.DEFAULT_SNMP_GROUP,
                            snmp_view=self.DEFAULT_SNMP_VIEW,
                        )
                    # create user
                    # define compatible priv protocol
                    priv_protocol = self.COMPATIBLE_PRIV_PROTOCOL.get(snmp_parameters.snmp_private_key_protocol.lower())
                    if not priv_protocol:
                        raise Exception(f"unable to create user with privacy protocol "
                                        f"{snmp_parameters.snmp_private_key_protocol}")
                    snmp_actions.create_snmp_v3_user(
                        user=snmp_parameters.snmp_user,
                        password=snmp_parameters.snmp_password,
                        auth_protocol=snmp_parameters.snmp_auth_protocol.lower(),
                        priv_key=snmp_parameters.snmp_private_key,
                        # priv_protocol=snmp_parameters.snmp_private_key_protocol.lower(),
                        priv_protocol=priv_protocol,
                    )
                    # assoc user <-> group
                    snmp_actions.associate_snmp_v3_user_group(
                        user=snmp_parameters.snmp_user,
                        group=self.DEFAULT_SNMP_GROUP,
                    )

            else:
                self._logger.debug("Start enable SNMP")
                snmp_actions.enable_snmp_v1v2()
                snmp_actions.create_snmp_community(snmp_community=snmp_parameters.snmp_community)


                # raise Exception("not yet implemented by vitala")
                # current_snmp_communities = snmp_actions.get_current_snmp_config()
    #                 snmp_community = snmp_parameters.snmp_community
    #                 if not re.search(
    #                     "snmp-server community {}".format(
    #                         re.escape(snmp_parameters.snmp_community)
    #                     ),
    #                     current_snmp_communities,
    #                 ):
    #                     snmp_actions.enable_snmp(
    #                         snmp_community, snmp_parameters.is_read_only
    #                     )
    #                 else:
    #                     self._logger.debug(
    #                         "SNMP Community '{}' already configured".format(
    #                             snmp_community
    #                         )
    #                     )
            self._logger.info("Start verification of SNMP config")
            # todo verify snmp configured
            pass
    #         with session.enter_mode(self._cli_handler.config_mode) as config_session:
    #             # Reentering config mode to perform commit for IOS-XR
    #             updated_snmp_actions = EnableDisableSnmpActions(
    #                 config_session, self._logger
    #             )
    #             if isinstance(snmp_parameters, SNMPV3Parameters):
    #                 updated_snmp_user = updated_snmp_actions.get_current_snmp_user()
    #                 if snmp_parameters.snmp_user not in updated_snmp_user:
    #                     raise Exception(
    #                         self.__class__.__name__,
    #                         "Failed to create SNMP v3 Configuration."
    #                         + " Please check Logs for details",
    #                     )
    #             else:
    #                 updated_snmp_communities = (
    #                     updated_snmp_actions.get_current_snmp_config()
    #                 )
    #                 if not re.search(
    #                     "snmp-server community {}".format(
    #                         re.escape(snmp_parameters.snmp_community)
    #                     ),
    #                     updated_snmp_communities,
    #                 ):
    #                     raise Exception(
    #                         self.__class__.__name__,
    #                         "Failed to create SNMP community."
    #                         + " Please check Logs for details",
    #                     )