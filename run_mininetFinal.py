from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import sys

class SingleTopology(Topo):
    def build(self, n):
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1', cpu=n*0.5)
        host2 = self.addHost('h2', cpu=n*0.5)
        host3 = self.addHost('h3', cpu=n*0.5)
        self.addLink(host1, switch1, bw=10, delay='5ms', loss=10, max_queue_size=1000)
        self.addLink(host2, switch1, bw=10, delay='5ms', loss=10, max_queue_size=1000)
        self.addLink(host3, switch1, bw=10, delay='5ms', loss=10, max_queue_size=1000)

class LinearTopology(Topo):
    def build(self, n):
        prev_switch = None
        for i in range(n):
            switch = self.addSwitch('s{}'.format(i+1))
            host = self.addHost('h{}'.format(i+1), cpu=n*0.5)
            self.addLink(host, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
            if prev_switch:
                self.addLink(prev_switch, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
            prev_switch = switch
            
class TreeTopology(Topo):
    def build(self, n):
        prev_switch = None
        self.addLink(prev_switch, self.addHost('h1', cpu=.5/n), bw=10, delay='5ms', loss=10, max_queue_size=1000)
        self.addLink(prev_switch, self.addHost('h2', cpu=.5/n), bw=10, delay='5ms', loss=10, max_queue_size=1000)
        for i in range(2, n+1):
            parent = self['s{}'.format(i//2)]
            switch = self.addSwitch('s{}'.format(i))
            self.addLink(switch, self.addHost('h{}'.format(2*i-1), cpu=.5/n), bw=10, delay='5ms', loss=10, max_queue_size=1000)
            self.addLink(switch, self.addHost('h{}'.format(2*i), cpu=.5/n), bw=10, delay='5ms', loss=10, max_queue_size=1000)
            self.addLink(switch, parent, bw=10, delay='5ms', loss=10, max_queue_size=1000)

class MeshTopology(Topo):
    def build(self, n):
        self = Mininet(topo=None, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
        hosts = []
        switches = []
        for i in range(1, n+1):
            host = self.addHost('h{}'.format(i), cpu=.5/n)
            switch = self.addSwitch('s{}'.format(i))
            hosts.append(host)
            switches.append(switch)
            self.addLink(host, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
            for i in range(n):
                for j in range(i+1, n):
                    self.addLink(switches[i], switches[j], bw=10, delay='5ms', loss=10, max_queue_size=1000)
        
def perfTest(topo_type, number):
    if topo_type == 'single':
        topo = SingleTopology(number)
    elif topo_type == 'linear':
        topo = LinearTopology(number)
    elif topo_type == 'tree':
        topo = TreeTopology(number)
    elif topo_type == 'mesh':
        topo = MeshTopology(number)                      
    else:
        print("Invalid topology type: {}".format(topo_type))
        sys.exit(1)
    
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    print("Start up the network created.)
    net.start()
    print("Dump host connections.")
    for host in net.hosts:
        info("{}\n".format(host.cmd("ifconfig")))
    print("Test network connectivity.")
    net.pingAll()
          
    print("Test all pairwise bandwidths amongst hosts.")
    info("*** Testing pairwise bandwidths\n")
    for src in net.hosts:
        for dst in net.hosts:
            if src != dst:
                result = src.cmd("iperf -c {} -t 10 -i 1".format(dst.IP()))
                info("{}\n".format(result))
    print("Stop the network.")
    net.stop()
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Do not have type of topology or numeric value.") 
        print("Usage: python {} <topology_type> <number>".format(sys.argv[0]))
        print("Topology types: single, linear, tree, mesh")
        sys.exit(1)
    
    topo_type = sys.argv[1]
    number = int(sys.argv[2])
    perfTest(topo_type, number)
