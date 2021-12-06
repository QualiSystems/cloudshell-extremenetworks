#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
from collections import OrderedDict

from cloudshell.shell.flows.autoload.basic_flow import AbstractAutoloadFlow

from cloudshell.extremenetworks.autoload.extremenetworks_generic_snmp_autoload import ExtremenetworksGenericSNMPAutoload
# from cloudshell.extremenetworks.autoload.extremenetworks_port_attrs_service import ExtremenetworksSnmpPortAttrTables
# from cloudshell.extremenetworks.autoload.extremenetworks_snmp_if_port import ExtremenetworksSnmpIfPort
# from cloudshell.extremenetworks.autoload.extremenetworks_snmp_if_port_channel import ExtremenetworksIfPortChannel

# entity_constants.ENTITY_VENDOR_TYPE_TO_CLASS_MAP = OrderedDict(
#     [
#         (re.compile(r"^\S+cevcontainer", re.IGNORECASE), "container"),
#         (re.compile(r"^\S+cevchassis", re.IGNORECASE), "chassis"),
#         (re.compile(r"^\S+cevmodule", re.IGNORECASE), "module"),
#         (re.compile(r"^\S+cevport", re.IGNORECASE), "port"),
#         (re.compile(r"^\S+cevpowersupply", re.IGNORECASE), "powerSupply"),
#     ]
# )


class ExtremenetworksSnmpAutoloadFlow(AbstractAutoloadFlow):

    EXTREMENETWORKS_MIBS_FOLDER = os.path.join(os.path.dirname(__file__), os.pardir, "mibs")
    DEVICE_NAMES_MAP_FILE = os.path.join(EXTREMENETWORKS_MIBS_FOLDER, "device_names_map.csv")

    def __init__(self, logger, snmp_handler):
        super(ExtremenetworksSnmpAutoloadFlow, self).__init__(logger)
        self._snmp_handler = snmp_handler

    def _autoload_flow(self, supported_os, resource_model):
        # todo implement autoload flow here
        with self._snmp_handler.get_service() as snmp_service:
            snmp_autoload = ExtremenetworksGenericSNMPAutoload(snmp_service, self._logger)
            return snmp_autoload.discover(supported_os, resource_model)

    # def _autoload_flow(self, supported_os, resource_model):
    #     with self._snmp_handler.get_service() as snmp_service:
    #         snmp_service.add_mib_folder_path(self.CISCO_MIBS_FOLDER)
    #         snmp_service.load_mib_tables(
    #             ["CISCO-PRODUCTS-MIB", "CISCO-ENTITY-VENDORTYPE-OID-MIB"]
    #         )
    #         cisco_snmp_autoload = ExtremenetworksGenericSNMPAutoload(snmp_service, self._logger)
    #         cisco_snmp_autoload.entity_table_service.set_port_exclude_pattern(
    #             r"stack|engine|management|"
    #             r"mgmt|voice|foreign|cpu|"
    #             r"control\s*ethernet\s*port|"
    #             r"usb\s*port"
    #         )
    #         cisco_snmp_autoload.entity_table_service.set_module_exclude_pattern(
    #             r"powershelf|cevsfp|cevxfr|"
    #             r"cevxfp|cevContainer10GigBasePort|"
    #             r"cevModulePseAsicPlim|cevModuleCommonCardsPSEASIC"
    #         )
    #         (
    #             cisco_snmp_autoload.if_table_service.port_attributes_service
    #         ) = CiscoSnmpPortAttrTables(snmp_service, self._logger)
    #         cisco_snmp_autoload.if_table_service.if_port_type = CiscoSnmpIfPort
    #         cisco_snmp_autoload.if_table_service.if_port_channel_type = (
    #             CiscoIfPortChannel
    #         )
    #
    #         cisco_snmp_autoload.system_info_service.set_model_name_map_file_path(
    #             self.DEVICE_NAMES_MAP_FILE
    #         )
    #         return cisco_snmp_autoload.discover(
    #             supported_os, resource_model, validate_module_id_by_port_name=True
    #         )
