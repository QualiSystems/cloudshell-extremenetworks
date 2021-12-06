from cloudshell.snmp.autoload.snmp_if_table import SnmpIfTable

from cloudshell.extremenetworks.autoload.extremenetworks_snmp_if_port import ExtremenetworksSnmpIfPort
from cloudshell.extremenetworks.autoload.extremenetworks_snmp_if_port_channel import ExtremenetworksIfPortChannel


class CiscoIfTable(SnmpIfTable):
    IF_PORT = ExtremenetworksSnmpIfPort
    IF_PORT_CHANNEL = ExtremenetworksIfPortChannel
