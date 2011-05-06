from utilities import bash
from cloudException import CloudRuntimeException, CloudInternalException
import logging
import os
import re

class networkConfig:
    class devInfo:
        def __init__(self, macAddr, ipAddr, netmask, gateway, type, name):
            self.name = name
            self.macAdrr = macAddr
            self.ipAddr = ipAddr
            self.netmask = netmask
            self.gateway = gateway
            self.type = type
            self.name = name
            #dhcp or static
            self.method = None 
     
    @staticmethod
    def getDefaultNetwork():
        cmd = bash("route -n|awk \'/^0.0.0.0/ {print $2,$8}\'") 
        if not cmd.isSuccess():
            logging.debug("Failed to get default route")
            raise CloudRuntimeException("Failed to get default route")

        result = cmd.getStdout().split(" ")
        gateway = result[0]
        dev = result[1]

        pdi = networkConfig.getDevInfo(dev)
        logging.debug("Found default network device:%s"%pdi.name)
        pdi.gateway = gateway
        return pdi

    @staticmethod
    def createBridge(dev, brName):
        if not networkConfig.isBridgeSupported():
            logging.debug("bridge is not supported")
            return False
        if networkConfig.isBridgeEnslavedWithDevices(brName):
            logging.debug("bridge: %s has devices enslaved"%brName)
            return False

        cmds = ""
        if not networkConfig.isBridge(brName):
            cmds = "brctl addbr %s ;"%brName
    
        cmds += "ifconfig %s up;"%brName
        cmds += "brctl addif %s %s"%(brName, dev)
        return bash(cmds).isSuccess()

    @staticmethod
    def isBridgeEnslavedWithDevices(brName):
        if not networkConfig.isBridge(brName):
            return False        

        if not os.listdir("/sys/class/net/%s/brif"%brName):
            return False           

        return True

    @staticmethod
    def isBridgeSupported():
        if os.path.exists("/proc/sys/net/bridge"):
            return True

        return bash("modprobe bridge").isSucess()

    @staticmethod
    def isNetworkDev(devName):
        return os.path.exists("/sys/class/net/%s"%devName)

    @staticmethod
    def isBridgePort(devName):
        return os.path.exists("/sys/class/net/%s/brport"%devName)
    
    @staticmethod
    def isBridge(devName):
        return os.path.exists("/sys/class/net/%s/bridge"%devName)

    @staticmethod
    def getBridge(devName):
        bridgeName = None
        if os.path.exists("/sys/class/net/%s/brport/bridge"%devName):
            realPath = os.path.realpath("/sys/class/net/%s/brport/bridge"%devName)
            bridgeName = realPath.split("/")[-1] 
        return bridgeName

    @staticmethod
    def getEnslavedDev(br, brPort):
        if not networkConfig.isBridgeEnslavedWithDevices(br):
            return None

        for dev in os.listdir("/sys/class/net/%s/brif"%br):
            br_port = int(file("/sys/class/net/%s/brif/%s/port_no"%(br,dev)).readline().strip("\n"), 16)
            if br_port == brPort:
                return dev

        return None
        
    @staticmethod
    def getDevInfo(dev):
        if not networkConfig.isNetworkDev(dev):
            logging.debug("dev: " + dev + " is not a network device")
            raise CloudInternalException("dev: " + dev + " is not a network device")

        netmask = None
        ipAddr = None
        macAddr = None

        cmd = bash("ifconfig " + dev)
        if not cmd.isSuccess():
            logging.debug("Failed to get address from ifconfig")
            raise CloudInternalException("Failed to get network info by ifconfig %s"%dev)

        for line in cmd.getLines():
            if line.find("HWaddr") != -1:
                macAddr = line.split("HWaddr ")[1].strip(" ")
            elif line.find("inet ") != -1:
                m = re.search("addr:(.*)\ *Bcast:(.*)\ *Mask:(.*)", line)
                if m is not None:
                    ipAddr = m.group(1).rstrip(" ")
                    netmask = m.group(3).rstrip(" ")

        if networkConfig.isBridgePort(dev):
            type = "brport"
        elif networkConfig.isBridge(dev):
            type = "bridge"
        else:
            type = "dev"

        return networkConfig.devInfo(macAddr, ipAddr, netmask, None, type, dev)


