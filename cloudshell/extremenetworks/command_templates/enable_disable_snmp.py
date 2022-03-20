#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ACTION_MAP = OrderedDict(
    {
        # r"Press .SPACE. to continue or .+ to quit": lambda session, logger: session.send_line("", logger),
        r"Entry exists. Are you sure you want to modify it": lambda session, logger: session.send_line("y", logger),
    }
)

ENABLE_SNMP_V3 = CommandTemplate("enable snmp access snmpv3")
ENABLE_SNMP_V1V2 = CommandTemplate("enable snmp access snmp-v1v2c")
DISABLE_SNMP_V1V2 = CommandTemplate("disable snmp access snmp-v1v2c")
DISABLE_SNMP_V3 = CommandTemplate("disable snmp access snmpv3")

SHOW_SNMP_USER = CommandTemplate("show snmpv3 user", action_map=ACTION_MAP)
SHOW_SNMP_VIEW = CommandTemplate("show snmpv3 mib-view", action_map=ACTION_MAP)

CREATE_SNMP_COMMUNITY = CommandTemplate("configure snmp add community readonly {snmp_community}")
DELETE_SNMP_COMMUNITY = CommandTemplate("configure snmp delete community readonly {snmp_community}")

# configure snmpv3 add mib-view [[hex hex_view_name] | view_name] subtree object_identifier {subtree_mask} {type [included | excluded]} {volatile}
ENABLE_SNMP_VIEW = CommandTemplate("configure snmpv3 add mib-view {snmp_view} subtree 1.3.6.1.2.1.1 type included")  # todo included?

SHOW_SNMP_GROUPS = CommandTemplate("show snmpv3 access", action_map=ACTION_MAP)

# configure snmpv3 add access gruppa1 sec-level priv read-view {} write-view {}
CREATE_SNMP_V3_GROUP = CommandTemplate(
    "configure snmpv3 add access {snmp_group} sec-level priv read-view {snmp_view} write-view {snmp_view}"
)
# configure snmpv3 add access snmpgroup sec-level priv read-view randomvvv write-view randomvvv

DELETE_SNMP_V3_GROUP = CommandTemplate(
    "configure snmpv3 delete access {snmp_group}"
)

# create new user
# To create a user, use the following command:
# configure snmpv3 add user [[hex hex_user_name] | user_name]
# {authentication [md5 | sha] [hex hex_auth_password | auth_password]}
# {privacy {des | 3des | aes {128 | 192 | 256}} [[hex hex_priv_password]
# | priv_password]} }{volatile}
CREATE_SNMP_V3_USER = CommandTemplate(
    "configure snmpv3 add user {snmp_user} authentication {auth_protocol} "
    "{snmp_password} privacy {priv_protocol} {snmp_priv_key}"
)

REMOVE_SNMP_V3_USER = CommandTemplate(
    "configure snmpv3 delete user {snmp_user}"
)
# configure snmpv3 add user snmpuser authentication md5 snmppassword privacy aes privkey111

# To associate users with groups, use the following command:
# configure snmpv3 add group [[hex hex_group_name] | group_name] user [[hex hex_user_name] | user_name] {sec-model [snmpv1| snmpv2c | usm]} {volatile}
#
# snmp_user = snmp_user,
# snmp_password = snmp_password,
# auth_protocol = auth_protocol,
# snmp_priv_key = snmp_priv_key,
# priv_protocol = priv_protocol,
# snmp_group = snmp_group,
ASSOC_USER_SNMP_V3_GROUP = CommandTemplate(
    "configure snmpv3 add group {snmp_group} user {snmp_user}"
)


# ERROR_MAP = OrderedDict(
#     {
#         (
#             r"[Ii]nvalid\s*([Ii]nput|[Cc]ommand)|[Cc]ommand rejected"
#         ): "Failed to initialize snmp. Please check Logs for details."
#     }
# )
#
# SHOW_SNMP_COMMUNITY = CommandTemplate(
#     "do show running-config | include snmp-server community", error_map=ERROR_MAP
# )
# SHOW_SNMP_CONFIG = CommandTemplate(
#     "do show running-config | include snmp-server", error_map=ERROR_MAP
# )
# ENABLE_SNMP = CommandTemplate(
#     "snmp-server community {snmp_community} {read_only}", error_map=ERROR_MAP
# )
# ENABLE_SNMP_VIEW = CommandTemplate(
#     "snmp-server view {snmp_view} iso included", error_map=ERROR_MAP
# )
# ENABLE_SNMP_GROUP = CommandTemplate(
#     "snmp-server group {snmp_group} v3 priv read {snmp_view} write {snmp_view}",
#     error_map=ERROR_MAP,
# )
# ENABLE_SNMP_V3_WITH_GROUP = CommandTemplate(
#     "snmp-server user {snmp_user} {snmp_group} v3 auth {auth_protocol} "
#     "{snmp_password} priv {priv_protocol} {snmp_priv_key}",
#     error_map=ERROR_MAP,
# )
# ENABLE_SNMP_USER = CommandTemplate(
#     "snmp-server user {snmp_user} auth {auth_protocol} "
#     "{snmp_password} priv[ {priv_protocol}] {snmp_priv_key}",
#     error_map=ERROR_MAP,
# )
# DISABLE_SNMP_COMMUNITY = CommandTemplate(
#     "no snmp-server community {snmp_community}", error_map=ERROR_MAP
# )
# DISABLE_SNMP_VIEW_ERROR_MAP = {r"\%Bad\s*OID": "Failed to delete snmp view"}
# DISABLE_SNMP_VIEW_ERROR_MAP.update(ERROR_MAP)
# DISABLE_SNMP_VIEW = CommandTemplate(
#     "no snmp-server view {snmp_view}[ iso{mib_oid}]",
#     error_map=DISABLE_SNMP_VIEW_ERROR_MAP,
# )
# DISABLE_SNMP_GROUP = CommandTemplate(
#     "no snmp-server group {snmp_group} v3 priv", error_map=ERROR_MAP
# )
# DISABLE_SNMP_USER_WITH_GROUP = CommandTemplate(
#     "no snmp-server user {snmp_user}[ {snmp_group} v3]", error_map=ERROR_MAP
# )
# DISABLE_SNMP_USER = CommandTemplate(
#     "no snmp-server user {snmp_user}", error_map=ERROR_MAP
# )