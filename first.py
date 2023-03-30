from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSSwitch
from mininet.link import TCLink
import sys

class SingleTopo(Topo):
    def build(self, n=3):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', cpu=n*0.5)
        h2 = self.addHost('h2', cpu=n*0.5)
        h3 = self.addHost('h3', cpu=n*0.5)
        self.addLink(h1, s1, bw=10, delay='5ms', loss=10, max_queue_size=1000)
        self.addLink(h2, s1, bw=10, delay='5ms', loss=10, max_queue_size=1000)
        self.addLink(h3, s1, bw=10, delay='5ms', loss=10, max_queue_size=1000)

class LinearTopo(Topo):
    def build(self, n=3):
        prev_switch = None
        for i in range(n):
            switch = self.addSwitch('s{}'.format(i+1))
            host = self.addHost('h{}'.format(i+1), cpu=n*0.5)
            self.addLink(host, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
            if prev_switch:
                self.addLink(prev_switch, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
            prev_switch = switch

def perfTest(topo_type, num_hosts):
    if topo_type == 'single':
        topo = SingleTopo(num_hosts)
    elif topo_type == 'linear':
        topo = LinearTopo(num_hosts)
    else:
        print("Invalid topology type: {}".format(topo_type))
        sys.exit(1)
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python {} <topology_type> <num_hosts>".format(sys.argv[0]))
        print("Topology types: single, linear")
        sys.exit(1)
    
    topo_type = sys.argv[1]
    num_hosts = int(sys.argv[2])
    
    perfTest(topo_type, num_hosts)
    
   

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    net.start()
    net.pingAll()
    net.stop()

