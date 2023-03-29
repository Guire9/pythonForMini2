from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI

def create_single_topology(n):
    net = Mininet(topo=None, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    switch = net.addSwitch('s1')
    host1 = net.addHost('h1', cpu=.5/n)
    host2 = net.addHost('h2', cpu=.5/n)
    host3 = net.addHost('h3', cpu=.5/n)
    net.addLink(host1, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
    net.addLink(host2, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
    net.addLink(host3, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
    return net

def create_linear_topology(n):
    net = Mininet(topo=None, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    host1 = net.addHost('h1', cpu=.5/n)
    switch1 = net.addSwitch('s1')
    net.addLink(host1, switch1, bw=10, delay='5ms', loss=10, max_queue_size=1000)
    for i in range(2, n+1):
        host = net.addHost('h{}'.format(i), cpu=.5/n)
        switch = net.addSwitch('s{}'.format(i))
        net.addLink(switch, switch1, bw=10, delay='5ms', loss=10, max_queue_size=1000)
        net.addLink(host, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
        switch1 = switch
    return net

def create_tree_topology(n):
    net = Mininet(topo=None, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    switch1 = net.addSwitch('s1')
    net.addLink(switch1, net.addHost('h1', cpu=.5/n), bw=10, delay='5ms', loss=10, max_queue_size=1000)
    net.addLink(switch1, net.addHost('h2', cpu=.5/n), bw=10, delay='5ms', loss=10, max_queue_size=1000)
    for i in range(2, n+1):
        parent = net['s{}'.format(i//2)]
        switch = net.addSwitch('s{}'.format(i))
        net.addLink(switch, net.addHost('h{}'.format(2*i-1), cpu=.5/n), bw=10, delay='5ms', loss=10, max_queue_size=1000)
        net.addLink(switch, net.addHost('h{}'.format(2*i), cpu=.5/n), bw=10, delay='5ms', loss=10, max_queue_size=1000)
        net.addLink(switch, parent, bw=10, delay='5ms', loss=10, max_queue_size=1000)
    return net

def create_mesh_topology(n):
    net = Mininet(topo=None, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    hosts = []
    switches = []
    for i in range(1, n+1):
        host = net.addHost('h{}'.format(i), cpu=.5/n)
        switch = net.addSwitch('s{}'.format(i))
        hosts.append(host)
        switches.append(switch)
        net.addLink(host, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
    for i in range(n):
        for j in range(i+1, n):
            net.addLink(switches[i], switches[j], bw=10, delay='5ms', loss=10, max_queue_size=1000)
    return net

def perfTest(topo_type, n):
    # create topology
    if topo_type == 'single':
        net = create_single_topology(n)
    elif topo_type == 'linear':
        net = create_linear_topology(n)
    elif topo_type == 'tree':
        net = create_tree_topology(n)
    elif topo_type == 'mesh':
        net = create_mesh_topology(n)
    else:
        raise ValueError("Invalid topology type: {}".format(topo_type))

    # start network
    net.start()

    # dump host connections
    info("*** Dumping host connections\n")
    for host in net.hosts:
        info("{}\n".format(host.cmd("ifconfig")))

    # test network connectivity
    info("*** Testing network connectivity\n")
    net.pingAll()

    # test pairwise bandwidths
    info("*** Testing pairwise bandwidths\n")
    for src in net.hosts:
        for dst in net.hosts:
            if src != dst:
                result = src.cmd("iperf -c {} -t 10 -i 1".format(dst.IP()))
                info("{}\n".format(result))

    # stop network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest('tree', 2)  # test tree topology with depth 2
    perfTest('mesh', 5)
