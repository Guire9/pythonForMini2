from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSSwitch
from mininet.link import TCLink
import sys

class SingleTopo(Topo):
    def build(self, n):
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1', cpu=n*0.5)
        host2 = self.addHost('h2', cpu=n*0.5)
        host3 = self.addHost('h3', cpu=n*0.5)
        self.addLink(host1, switch1, bw=10, delay='5ms', loss=10, max_queue_size=1000)
        self.addLink(host2, switch1, bw=10, delay='5ms', loss=10, max_queue_size=1000)
        self.addLink(host3, switch1, bw=10, delay='5ms', loss=10, max_queue_size=1000)

class LinearTopo(Topo):
    def build(self, n):
        prev_switch = None
        for i in range(n):
            switch = self.addSwitch('s{}'.format(i+1))
            host = self.addHost('h{}'.format(i+1), cpu=n*0.5)
            self.addLink(host, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
            if prev_switch:
                self.addLink(prev_switch, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
            prev_switch = switch
            
class TreeTopo(Topo):
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

class MeshTopo(Topo):
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
        
def perfTest(topo_type, num_hosts):
    if topo_type == 'single':
        topo = SingleTopo(num_hosts)
    elif topo_type == 'linear':
        topo = LinearTopo(num_hosts)
    elif topo_type == 'tree':
        topo = TreeTopo(num_hosts)
    elif topo_type == 'mesh':
        topo = MeshTopo(num_hosts)                      
    else:
        print("Invalid topology type: {}".format(topo_type))
        sys.exit(1)
    
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    net.start()
    net.pingAll()
    net.stop()
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python {} <topology_type> <num_hosts>".format(sys.argv[0]))
        print("Topology types: single, linear")
        sys.exit(1)
    
    topo_type = sys.argv[1]
    num_hosts = int(sys.argv[2])
    perfTest(topo_type, num_hosts)
    
   

  

