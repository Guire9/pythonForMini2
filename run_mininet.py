from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import CPULimitedHost, OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class SingleTopo(Topo):
  def init(n):
    net = Mininet(topo=None, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    switch = net.addSwitch('s1')
    host1 = net.addHost('h1', cpu=.5/n)
    host2 = net.addHost('h2', cpu=.5/n)
    host3 = net.addHost('h3', cpu=.5/n)
    net.addLink(host1, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
    net.addLink(host2, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
    net.addLink(host3, switch, bw=10, delay='5ms', loss=10, max_queue_size=1000)
    
class LinearTopo(Topo):
  def inint(n):
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
        
class TreeTopo(Topo):
  def inint(n):
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
  
 class MeshTopo(Topo):
  def inint(n):  
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
   

  
