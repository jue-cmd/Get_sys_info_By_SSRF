import requests
import base64
import re

log_level = 4
class hack_hole:
    def __init__(self, hack_call_back):
        self.hack_call_back = hack_call_back

    def send(self, data):
        try:
            data_=self.hack_call_back(data)
            if log_level == 1:
                print("发送数据:", data)
            if log_level <= 2:
                print("接收数据:", data_)
            return data_
        except requests.exceptions.ConnectionError as e:
            print("连接错误:", e)
            exit()
        except Exception as  e:
            print("错误:", data, "->", e)
            return False


class progress:
    def __init__(self, pid, cmdline):
        self.pid = pid
        self.cmdline = cmdline


class net_work_statistics:
    def __init__(self,raw_data):
        self.Receive_bytes=raw_data[0]
        self.Receive_packets=raw_data[1]
        self.Receive_errs=raw_data[2]
        self.Receive_drop=raw_data[3]
        self.Receive_fifo=raw_data[4]
        self.Receive_frame=raw_data[5]
        self.Receive_compressed=raw_data[6]
        self.Transmit_bytes=raw_data[7]
        self.Transmit_packet=raw_data[8]
        self.Transmit_errs=raw_data[9]
        self.Transmit_drop=raw_data[10]
        self.Transmit_fifo=raw_data[11]
        self.Transmit_colls=raw_data[12]
        self.Transmit_carrier=raw_data[13]
        self.Transmit_compressed=raw_data[14]
    def __str__(self):
        info="""
        Receive_bytes:{}
        Receive_packets:{}
        Receive_errs:{}
        Receive_drop:{}
        Receive_fifo:{}
        Receive_frame:{}
        Receive_compressed:{}
        Transmit_bytes:{}
        Transmit_packet:{}
        Transmit_errs:{}
        Transmit_drop:{}
        Transmit_fifo:{}
        Transmit_colls:{}
        Transmit_carrier:{}
        Transmit_compressed:{}
        """.format(
            self.Receive_bytes,
            self.Receive_packets,
            self.Receive_errs,
            self.Receive_drop,
            self.Receive_fifo,
            self.Receive_frame,
            self.Receive_compressed,
            self.Transmit_bytes,
            self.Transmit_packet,
            self.Transmit_errs,
            self.Transmit_drop,
            self.Transmit_fifo,
            self.Transmit_colls,
            self.Transmit_carrier,
            self.Transmit_compressed)
        return info



class interface_info:
    def __init__(self,ip_mode_, mac_address_, netmask_, broadcast_, mtu_, multicast_):
        self.ip_mode = int(ip_mode_)
        self.mac_address = mac_address_
        self.netmask = netmask_
        self.broadcast = broadcast_
        self.mtu = mtu_
        self.multicast = multicast_
    def __str__(self):
        info="""
        ip_mode:{}
        mac_address:{}
        netmask:{}
        broadcast:{}
        mtu:{}
        multicast:{}
        """.format(
            "static" if self.ip_mode == 1 else "dhcp",
            self.mac_address,
            self.netmask,
            self.broadcast,
            self.mtu,
            self.multicast
            )
        return info




class interface:
    def __init__(self, _name,info,statistics):
        self.name = _name
        self.info=info
        self.statistics=statistics
    def __str__(self):
        info="接口名称:{}\n接口信息:{}接口统计信息:{}".format(self.name,str(self.info),str(self.statistics))
        return info
    def display(self):
        print(self)


class process_status:
    def __init__(self,_raw_):
        if _raw_ == False or _raw_ == None:
            return
        _raw_ = _raw_.split("\n")
        for i in _raw_:
            if i =="":
                continue
            i=i.split(":")
            self.__dict__[i[0].strip()]=i[1].strip()
        pass
    def __str__(self):
        info="进程状态信息:{}\n".format(self.__dict__)
        return info

class process:
    def __init__(self, pid, cmdline,env,status):
        self.pid = pid
        self.cmdline = cmdline
        self.env = env
        self.status = status
    def __str__(self,diaplay_list=["pid","cmdline","env","status"]):
        info=""
        for i in diaplay_list:
            if i not in self.__dict__:
                continue
            info+="""{}:{}\n""".format(i,self.__dict__[i])
        return info
    def display(self,diaplay_list=["pid","cmdline","env","status"]):
        info=""
        for i in diaplay_list:
            if i not in self.__dict__:
                continue
            info+="""   {}:{}\n""".format(i,self.__dict__[i])
        print(info)
        return 0


error_list={
    "get_net_work_interfaces": "获取网络接口信息失败",
    "get_net_work_interfaces_ip_mode": "获取网络接口IP模式失败",
    "get_net_work_interfaces_mac": "获取网络接口MAC地址失败",
    "get_net_work_interfaces_netmask": "获取网络接口子网掩码失败",
    "get_net_work_interfaces_broadcast": "获取网络接口广播地址失败",
    "get_net_work_interfaces_mtu": "获取网络接口MTU失败",
    "get_net_work_interfaces_multicast": "获取网络接口多播地址失败",
    "get_pid": "获取进程信息失败",
    "get_pid_name": "获取进程名称失败",
    "get_process_cmdline": "获取进程路径失败",
    "get_pid_environ": "获取进程环境变量失败",
    "get_pid_status": "获取进程状态失败",
}

pocs_network = {
    "get_net_work_interfaces": "/proc/net/dev",
    "get_net_work_interfaces_ip_mode": "/sys/class/net/{}/addr_assign_type",
    "get_net_work_interfaces_mac": "/sys/class/net/{}/address",
    "get_net_work_interfaces_netmask": "/sys/class/net/{}/netmask",
    "get_net_work_interfaces_bcast": "/sys/class/net/{}/broadcast",
    "get_net_work_interfaces_mtu": "/sys/class/net/{}/mtu",
    "get_net_work_interfaces_multicast": "/sys/class/net/{}/statistics/multicast",
}

pocs_progress = {
    "get_mem_info": "/proc/meminfo",
    "get_pid_max": "/proc/sys/kernel/pid_max",
    "get_pid_list": "/proc/{}/status",
    "get_pid_cmdline": "/proc/{}/cmdline",
    "get_pid_cwd": "/proc/{}/cwd",
    "get_pid_root": "/proc/{}/root",
    "get_pid_environ": "/proc/{}/environ",
    "get_pid_exe": "/proc/{}/exe",
    "get_pid_maps": "/proc/{}/maps",
    "get_pid_stat": "/proc/{}/stat",
    "get_pid_task": "/proc/{}/task",
}

pocs_mount_point = {

}

def get_net_work_interface_info(target,name):
    try:
        ip_mode_=target.send(pocs_network["get_net_work_interfaces_ip_mode"].format(name))
        if ip_mode_==False:
            ip_mode_=error_list["get_net_work_interfaces_ip_mode"]
        ip_mode_=ip_mode_.replace('\n',"")
        mac_address_=target.send(pocs_network["get_net_work_interfaces_mac"].format(name))
        if mac_address_==False:
            mac_address_=error_list["get_net_work_interfaces_mac"]
        mac_address_=mac_address_.replace('\n',"")
        netmask_=target.send(pocs_network["get_net_work_interfaces_netmask"].format(name))
        if netmask_==False:
            netmask_=error_list["get_net_work_interfaces_netmask"]
        netmask_=netmask_.replace('\n',"")
        broadcast_=target.send(pocs_network["get_net_work_interfaces_bcast"].format(name))
        if broadcast_==False:
            broadcast_=error_list["get_net_work_interfaces_bcast"]
        broadcast_=broadcast_.replace('\n',"")
        mtu_=target.send(pocs_network["get_net_work_interfaces_mtu"].format(name))
        if mtu_==False:
            mtu_=error_list["get_net_work_interfaces_mtu"]
        mtu_=mtu_.replace('\n',"")
        multicast_=target.send(pocs_network["get_net_work_interfaces_multicast"].format(name))
        if multicast_==False:
            multicast_=error_list["get_net_work_interfaces_multicast"]
        multicast_=multicast_.replace('\n',"")
        return interface_info(ip_mode_,mac_address_,netmask_,broadcast_,mtu_,multicast_)
    except Exception as e:
        print("错误",e)


def get_net_work_interfaces(target):
    # 获取所有接口名称
    result_interfaces = []
    response_ret = target.send(
        pocs_network["get_net_work_interfaces"])
    if response_ret == False:
        return False
    for _interface in response_ret.split('\n')[2:]:
        if _interface=="":
            continue
        _temp_=_interface.split(':')
        _interface_name = _temp_[0].strip()
        _net_work_statistics_=net_work_statistics(_temp_[1].split())
        _interface_info_=get_net_work_interface_info(target,_interface_name)
        result_interfaces.append(interface(_interface_name,_interface_info_,_net_work_statistics_))
    return result_interfaces


def get_max_pid(target):
    try:
        _pid_max=int(target.send(pocs_progress["get_pid_max"]))
        if _pid_max==0:
            raise ValueError()
    except ValueError as e:
        while True:
            try:
                _pid_max=int(input("获取最大pid失败，请输入最大pid"))
            except ValueError as e:
                print("请输入正确的pid")
                continue
    return _pid_max

def get_process_cmdline(target,pid):
    _cmd_line_=target.send(pocs_progress["get_pid_cmdline"].format(pid))
    if _cmd_line_ == False:
        return error_list["get_process_cmdline"]
    return _cmd_line_

def get_process_env(target,pid):
    _env_=target.send(pocs_progress["get_pid_environ"].format(pid))
    if _env_ == False:
        return error_list["get_pid_environ"]
    return _env_

def get_process_list(target,fs=None,_pid_max=None):
    process_list = []
    if _pid_max == None:
        _pid_max=get_max_pid(target)
    for i in range(_pid_max):
        _process_info=target.send(pocs_progress["get_pid_list"].format(i))
        if _process_info == False:
            continue
        status=process_status(_process_info)
        cmdline=get_process_cmdline(target,i)
        env=get_process_env(target,i)
        _prog_=process(i,cmdline,env,status)
        if fs is not None:
            fs.write(str(_prog_)+"\n")
        process_list.append(_prog_)
    return process_list

import json
def callback(data):
    '''
a by pass func
            data is the path will accessed
            return False meanes no
            return fle context meanes ok
'''
    pass

if __name__ == "__main__":
    _target_=hack_hole(callback)
    _ret_=get_net_work_interfaces(_target_)
    _data=get_process_list(_target_,_pid_max=10)
    for _interface_ in _ret_:
        _interface_.display()
    for _pid_ in _data:
        _pid_.display(["pid","cmdline"])
