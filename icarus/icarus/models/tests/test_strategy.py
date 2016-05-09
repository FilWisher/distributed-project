import sys
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
import fnss

import icarus.models as strategy
from icarus.execution import NetworkModel, NetworkView, NetworkController, TestCollector

def t_stat_topology():   #making one neighbour cache but not the other depending on threshhold
    topology = fnss.Topology()
    topology.add_path([1, 2, 3, 4, 5, 6])
    topology.add_edge(2, 7)
    topology.add_edge(3, 8)
    topology.add_edge(8, 9)
    topology.add_edge(8, 10)
    receivers = (1, 9)
    source = 6
    caches = (2, 8, 7, 10, 3, 4 , 5)

	# 1-2-3-4-5-6
	#   | |
	#   7 8-9
	#     |
	#     10
    contents = caches
    fnss.add_stack(topology, source, 'source', {'contents': contents})
    for v in caches:
        fnss.add_stack(topology, v, 'router', {'cache_size': 1})
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver', {})
    return topology


def star_topology():  #havent used this one yet
    topology = fnss.star_topology(6)
    source = 4
    receivers = (0, 5) 
    caches = (1, 2, 3)
    contents = caches
    fnss.add_stack(topology, source, 'source', {'contents': contents})
    for v in caches:
        fnss.add_stack(topology, v, 'router', {'cache_size': 1})
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver', {})
    return topology

def lisa_topology():
    topology = fnss.topology()
    topology.add_path([0, 2, 4, 6, 8, 7,  5, 3, 1])
    topology.add_edge(2, 3)
    topology.add_edge(0, 1)
    topology.add_edge(8, 1)
    receivers = (0, 1, 5)
    source = (6) 
    caches = (2, 3, 4, 7,8)
    contents = caches
    fnss.add_stack(topology, source, 'source', {'contents': contents})
    for v in caches:
        fnss.add_stack(topology, v, 'router', {'cache_size': 1})
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver', {})
    return topology

def wing_topology():
    topology = fnss.Topology()
    topology.add_path([0, 2, 4, 6, 8, 7,  5, 3, 1])
    topology.add_edge(2, 3)
    topology.add_edge(0, 1)
    receivers = (0, 1, 5)
    source = (6) 
    caches = (2, 3, 4, 7,8)
    contents = caches
    fnss.add_stack(topology, source, 'source', {'contents': contents})
    for v in caches:
        fnss.add_stack(topology, v, 'router', {'cache_size': 1})
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver', {})
    return topology


def on_path_topology():
    """Return topology for testing on-path caching strategies
    """ 
    # Topology sketch
    #
    # 0 ---- 1 ---- 2 ---- 3 ---- 4
    #               |
    #               |
    #               5
    #
    topology = fnss.line_topology(5)
    topology.add_edge(2, 5)
    source = 4
    receivers = (0, 5) 
    caches = (1, 2, 3)
    contents = caches
    fnss.add_stack(topology, source, 'source', {'contents': contents})
    for v in caches:
        fnss.add_stack(topology, v, 'router', {'cache_size': 1})
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver', {})
    return topology

def off_path_topology():
    """Return topology for testing off-path caching strategies
    """
    # Topology sketch
    #
    #     --------- 5 ----------  
    #    /                      \
    #   /                        \
    # 0 ---- 1 ---- 2 ---- 3 ---- 4 
    #               |
    #               |
    #               6
    #
    topology = fnss.ring_topology(6)
    topology.add_edge(2, 6)
    topology.add_edge(1, 7)
    source = 4
    receivers = (0, 6, 7) 
    caches = (1, 2, 3, 5)
    contents = caches
    fnss.add_stack(topology, source, 'source', {'contents': contents})
    for v in caches:
        fnss.add_stack(topology, v, 'router', {'cache_size': 1})
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver', {})
    return topology

def nrr_topology():
    """Return topology for testing NRR caching strategies
    """
    # Topology sketch
    #
    # 0 ---- 2----- 4 
    #        |       \
    #        |        6
    #        |       /
    # 1 ---- 3 ---- 5  
    #
    topology = fnss.Topology()
    topology.add_path([0, 2, 4, 6, 5, 3, 1])
    topology.add_edge(2, 3)
    receivers = (0, 1)
    source = (6) 
    caches = (2, 3, 4, 5)
    contents = caches
    fnss.add_stack(topology, source, 'source', {'contents': contents})
    for v in caches:
        fnss.add_stack(topology, v, 'router', {'cache_size': 1})
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver', {})
    return topology

class TestHashrouting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = off_path_topology()
        model = NetworkModel(topology, cache_policy={'name': 'FIFO'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)

    def tearDown(self):
        pass

    def test_hashrouting_symmetric(self):
        hr = strategy.HashroutingSymmetric(self.view, self.controller)
        hr.authoritative_cache = lambda x: x
        # At time 1, receiver 0 requests content 2
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # At time 2 repeat request, expect cache hit
        hr.process_event(2, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2)))
        exp_cont_hops = set(((2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # Now request from node 6, expect hit
        hr.process_event(3, 6, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((6, 2),))
        exp_cont_hops = set(((2, 6),))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))

    def test_hashrouting_asymmetric(self):
        hr = strategy.HashroutingAsymmetric(self.view, self.controller)
        hr.authoritative_cache = lambda x: x
        # At time 1, receiver 0 requests content 2
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 5), (5, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # Now request from node 6, expect miss but cache insertion
        hr.process_event(2, 6, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((6, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 6)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # Now request from node 0 again, expect hit
        hr.process_event(3, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2)))
        exp_cont_hops = set(((2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))

    def test_hashrouting_multicast(self):
        hr = strategy.HashroutingMulticast(self.view, self.controller)
        hr.authoritative_cache = lambda x: x
        # At time 1, receiver 0 requests content 2
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (4, 5), (5, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # At time 2 repeat request, expect cache hit
        hr.process_event(2, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2)))
        exp_cont_hops = set(((2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # Now request from node 6, expect hit
        hr.process_event(3, 6, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((6, 2),))
        exp_cont_hops = set(((2, 6),))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
   
    def test_hashrouting_hybrid_am(self):
        hr = strategy.HashroutingHybridAM(self.view, self.controller, max_stretch=0.3)
        hr.authoritative_cache = lambda x: x
        # At time 1, receiver 0 requests content 2, expect asymmetric
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 5), (5, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # At time 2, receiver 0 requests content 3, expect multicast
        hr.process_event(3, 0, 3, True)
        loc = self.view.content_locations(3)
        self.assertEquals(len(loc), 2)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 5), (5, 0), (4, 3)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # At time 3, receiver 0 requests content 5, expect symm = mcast = asymm
        hr.process_event(3, 0, 5, True)
        loc = self.view.content_locations(5)
        self.assertEquals(len(loc), 2)
        self.assertIn(5, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 5), (5, 4)))
        exp_cont_hops = set(((4, 5), (5, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops)) 

    def test_hashrouting_hybrid_sm(self):
        hr = strategy.HashroutingHybridSM(self.view, self.controller)
        hr.authoritative_cache = lambda x: x
        # At time 1, receiver 0 requests content 2, expect asymmetric
        hr.process_event(1, 0, 3, True)
        loc = self.view.content_locations(3)
        self.assertEquals(len(loc), 2)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 5), (5, 0), (4, 3)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # At time 2, receiver 0 requests content 5, expect symm = mcast = asymm
        hr.process_event(2, 0, 5, True)
        loc = self.view.content_locations(5)
        self.assertEquals(len(loc), 2)
        self.assertIn(5, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 5), (5, 4)))
        exp_cont_hops = set(((4, 5), (5, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        
    def test_hashrouting_hybrid_sm_multi_options(self):
        # NOTE: The following test case will fail because NetworkX returns as
        # shortest path from 4 to 1: 4-5-0-1. There is also another shortest
        # path: 4-3-2-1. The best delivery strategy overall would be multicast
        # but because of NetworkX selecting the least convenient shortest path
        # the computed solution is symmetric with path: 4-5-0-1-2-6.
        pass 
#        # At time 1, receiver 6 requests content 1, expect multicast
#        hr = strategy.HashroutingHybridSM(self.view, self.controller)
#        hr.authoritative_cache = lambda x: x
#        hr.process_event(1, 6, 1, True)
#        loc = self.view.content_locations(1)
#        self.assertEquals(len(loc), 2)
#        self.assertIn(1, loc)
#        self.assertIn(4, loc)
#        summary = self.collector.session_summary()
#        exp_req_hops = set(((6, 2), (2, 1), (1, 2), (2, 3), (3, 4)))
#        exp_cont_hops = set(((4, 3), (3, 2), (2, 1), (2, 6)))
#        req_hops = summary['request_hops']
#        cont_hops = summary['content_hops']
#        self.assertSetEqual(exp_req_hops, set(req_hops))
#        self.assertSetEqual(exp_cont_hops, set(cont_hops)) 

class TestOnPath(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = on_path_topology()
        model = NetworkModel(topology, cache_policy={'name': 'FIFO'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass
    
    def test_lce_same_content(self):
        hr = strategy.LeaveCopyEverywhere(self.view, self.controller)
        # receiver 0 requests 2, expect miss
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 4)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # receiver 0 requests 2, expect hit
        hr.process_event(1, 5, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 4)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((5, 2),))
        exp_cont_hops = set(((2, 5),))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        
    def test_lce_different_content(self):
        hr = strategy.LeaveCopyEverywhere(self.view, self.controller)
        # receiver 0 requests 2, expect miss
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 4)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # request content 3 from 5
        hr.process_event(1, 5, 3, True)
        loc = self.view.content_locations(3)
        self.assertEquals(len(loc), 3)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(1, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((5, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 5)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # request content 3 from , hit in 2
        hr.process_event(1, 0, 3, True)
        loc = self.view.content_locations(3)
        self.assertEquals(len(loc), 4)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2)))
        exp_cont_hops = set(((2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))

    def test_edge(self):
        hr = strategy.Edge(self.view, self.controller)
        # receiver 0 requests 2, expect miss
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(0, 1), (1, 2), (2, 3), (3, 4)]
        exp_cont_hops = [(4, 3), (3, 2), (2, 1), (1, 0)]
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(set(exp_req_hops), set(req_hops))
        self.assertSetEqual(set(exp_cont_hops), set(cont_hops))
        self.assertEqual(4, summary['serving_node'])
        # receiver 0 requests 2, expect hit
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(0, 1)]
        exp_cont_hops = [(1, 0)]
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(set(exp_req_hops), set(req_hops))
        self.assertSetEqual(set(exp_cont_hops), set(cont_hops))
        self.assertEqual(1, summary['serving_node'])
        hr.process_event(1, 5, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 3)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(5, 2), (2, 3), (3, 4)]
        exp_cont_hops = [(4, 3), (3, 2), (2, 5)]
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(set(exp_req_hops), set(req_hops))
        self.assertSetEqual(set(exp_cont_hops), set(cont_hops))
        self.assertEqual(4, summary['serving_node'])
        hr.process_event(1, 5, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 3)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(5, 2)]
        exp_cont_hops = [(2, 5)]
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(set(exp_req_hops), set(req_hops))
        self.assertSetEqual(set(exp_cont_hops), set(cont_hops))
        self.assertEqual(2, summary['serving_node'])

    def test_lcd(self):
        hr = strategy.LeaveCopyDown(self.view, self.controller)
        # receiver 0 requests 2, expect miss
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # receiver 0 requests 2, expect hit in 3
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 3)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3)))
        exp_cont_hops = set(((3, 2), (2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # receiver 0 requests 2, expect hit in 2
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 4)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2),))
        exp_cont_hops = set(((2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # receiver 0 requests 2, expect hit in 1
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 4)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1),))
        exp_cont_hops = set(((1, 0),))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # receiver 0 requests 3, expect miss and eviction of 2 from 3
        hr.process_event(1, 0, 3, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 3)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        loc = self.view.content_locations(3)
        self.assertEquals(len(loc), 2)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        
    def test_cl4m(self):
        hr = strategy.CacheLessForMore(self.view, self.controller)
        # receiver 0 requests 2, expect miss
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # receiver 0 requests 2, expect hit
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 3)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2)))
        exp_cont_hops = set(((2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        # receiver 0 requests 3, expect miss
        hr.process_event(1, 0, 3, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(1, loc)
        self.assertIn(4, loc)
        loc = self.view.content_locations(3)
        self.assertEquals(len(loc), 2)
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        
    def test_random_choice(self):
        hr = strategy.RandomChoice(self.view, self.controller)
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 2)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        self.assertEqual(4, summary['serving_node'])
        
    def test_random_bernoulli(self):
        hr = strategy.RandomBernoulli(self.view, self.controller)
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        self.assertEqual(4, summary['serving_node'])
        
    def test_random_bernoulli_p_0(self):
        hr = strategy.RandomBernoulli(self.view, self.controller, p=0)
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        self.assertEqual(4, summary['serving_node'])
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        self.assertEqual(4, summary['serving_node'])
        
    def test_random_bernoulli_p_1(self):
        hr = strategy.RandomBernoulli(self.view, self.controller, p=1)
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        self.assertEqual(4, summary['serving_node'])
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        self.assertEqual(1, summary['serving_node'])
        

class TestNrr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = nrr_topology()
        model = NetworkModel(topology, cache_policy={'name': 'FIFO'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass
    
    def test_lce(self):
        hr = strategy.NearestReplicaRouting(self.view, self.controller, metacaching='LCE')
        # receiver 0 requests 2, expect miss
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(3, len(loc))
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        self.assertIn(6, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(5, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(0, 2), (2, 4), (4, 6)]
        exp_cont_hops = [(6, 4), (4, 2), (2, 0)]
        self.assertSetEqual(set(exp_req_hops), set(summary['request_hops']))
        self.assertSetEqual(set(exp_cont_hops), set(summary['content_hops']))
        self.assertEqual(6, summary['serving_node'])
        # receiver 0 requests 2, expect hit
        hr.process_event(1, 1, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(4, len(loc))
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        self.assertIn(6, loc)
        self.assertIn(3, loc)
        self.assertNotIn(5, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(1, 3), (3, 2)]
        exp_cont_hops = [(2, 3), (3, 1)]
        self.assertSetEqual(set(exp_req_hops), set(summary['request_hops']))
        self.assertSetEqual(set(exp_cont_hops), set(summary['content_hops']))
        self.assertEqual(2, summary['serving_node'])
        hr.process_event(1, 1, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(4, len(loc))
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        self.assertIn(6, loc)
        self.assertIn(3, loc)
        self.assertNotIn(5, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(1, 3)]
        exp_cont_hops = [(3, 1)]
        self.assertSetEqual(set(exp_req_hops), set(summary['request_hops']))
        self.assertSetEqual(set(exp_cont_hops), set(summary['content_hops']))
        self.assertEqual(3, summary['serving_node'])
        

    def test_lcd(self):
        hr = strategy.NearestReplicaRouting(self.view, self.controller, metacaching='LCD')
        # receiver 0 requests 2, expect miss
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(2, len(loc))
        self.assertNotIn(2, loc)
        self.assertIn(4, loc)
        self.assertIn(6, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(5, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(0, 2), (2, 4), (4, 6)]
        exp_cont_hops = [(6, 4), (4, 2), (2, 0)]
        self.assertSetEqual(set(exp_req_hops), set(summary['request_hops']))
        self.assertSetEqual(set(exp_cont_hops), set(summary['content_hops']))
        self.assertEqual(6, summary['serving_node'])
        hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(3, len(loc))
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        self.assertIn(6, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(5, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(0, 2), (2, 4)]
        exp_cont_hops = [(4, 2), (2, 0)]
        self.assertSetEqual(set(exp_req_hops), set(summary['request_hops']))
        self.assertSetEqual(set(exp_cont_hops), set(summary['content_hops']))
        self.assertEqual(4, summary['serving_node'])
        # receiver 0 requests 2, expect hit
        hr.process_event(1, 1, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(4, len(loc))
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        self.assertIn(6, loc)
        self.assertIn(3, loc)
        self.assertNotIn(5, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(1, 3), (3, 2)]
        exp_cont_hops = [(2, 3), (3, 1)]
        self.assertSetEqual(set(exp_req_hops), set(summary['request_hops']))
        self.assertSetEqual(set(exp_cont_hops), set(summary['content_hops']))
        self.assertEqual(2, summary['serving_node'])
        hr.process_event(1, 1, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(4, len(loc))
        self.assertIn(2, loc)
        self.assertIn(4, loc)
        self.assertIn(6, loc)
        self.assertIn(3, loc)
        self.assertNotIn(5, loc)
        summary = self.collector.session_summary()
        exp_req_hops = [(1, 3)]
        exp_cont_hops = [(3, 1)]
        self.assertSetEqual(set(exp_req_hops), set(summary['request_hops']))
        self.assertSetEqual(set(exp_cont_hops), set(summary['content_hops']))
        self.assertEqual(3, summary['serving_node'])


class test_pop_neighbour_stat(unittest.TestCase):
    """ Tests for the static threshold, suggest to neighbour popularity table"""
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = nrr_topology()
        model = NetworkModel(topology, 
                             cache_policy={'name': 'POP_NEIGHBOUR_STAT'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Pop_neighbour_stat(self.view, self.controller)
        
        # receiver 0 requests 2 from location 6, expect miss at all nodes
	hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)
        summary = self.collector.session_summary()
        #check the requests took correct path
        exp_req_hops = set([(4,6), (2, 4), (0, 2)])
        #check content took correct path
       	exp_cont_hops = set([(4, 2), (2, 0), (6, 4)])
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(6, summary['serving_node'])

	#run more requests than the threshold value for item 2
        for i in range(0,self.view.get_threshold()):
            hr.process_event(1, 0, 2, True)

        #item 2 should now be everywhere but the requester (0) and node 1
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 5)
        self.assertNotIn(1, loc) #since not adjacent to any on-path nodes 
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
	self.assertIn(5, loc)
	self.assertIn(6, loc)

class test_pop_self_stat(unittest.TestCase):
    """ Tests for the static threshold, self caching popularity table"""

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = nrr_topology()
        model = NetworkModel(topology, 
                             cache_policy={'name': 'POP_SELF_STAT'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Pop_self_stat(self.view, self.controller)
        
	hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)
        summary = self.collector.session_summary()
        #check the requests took correct path
        exp_req_hops = set([(4,6), (2, 4), (0, 2)])
        #check content took correct path
       	exp_cont_hops = set([(4, 2), (2, 0), (6, 4)])
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(6, summary['serving_node'])

	#run more requests than the threshold value for item 2
        for i in range(0,self.view.get_threshold()):
            hr.process_event(1, 0, 2, True)

        #item 2 should now be everywhere on the path
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 3)
        self.assertNotIn(1, loc)
        self.assertIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)


class test_pop_neighbour_t_stat(unittest.TestCase):
    """ Tests for the static threshold, suggest to neighbour, 
    with independent neighbour threshold rejection popularity table"""

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = t_stat_topology()
        model = NetworkModel(topology, 
                             cache_policy={'name': 'POP_NEIGHBOUR_T_STAT'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Pop_neighbour_t_stat(self.view, self.controller)
        
        # receiver 0 requests 2 from location 6, expect miss at all nodes
	hr.process_event(1, 1, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertNotIn(7, loc)
	self.assertNotIn(8, loc)
	self.assertNotIn(9, loc)
	self.assertNotIn(10, loc)
	self.assertIn(6, loc)

        summary = self.collector.session_summary()
        #check the requests took correct path
        exp_req_hops = set([(1,2), (2,3), (3,4), (4,5), (5,6)])
        #check content took correct path
       	exp_cont_hops = set([(6,5), (5,4), (4,3), (3,2), (2,1)])
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(6, summary['serving_node'])
	print "first session summary"

	hr.process_event(1,9,2, True)
        loc = self.view.content_locations(2)
        summary = self.collector.session_summary()
        #check the requests took correct path
        exp_req_hops = set([(9,8), (8,3), (3,4), (4,5), (5,6)])
        #check content took correct pat
       	exp_cont_hops = set([(6,5), (5,4), (4,3), (3,8), (8,9)])
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(6, summary['serving_node'])
	print "second session summary"


        for i in range(0,int(self.view.get_threshold() * 0.75)):
            hr.process_event(1, 1, 2, True)

        for k in range(0, int(self.view.get_threshold() * 0.25)):
            hr.process_event(1, 9, 2, True)

        #item 2 should be
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 5)
        self.assertNotIn(8, loc) 
	self.assertNotIn(10, loc) 
	self.assertNotIn(7, loc) 
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
	self.assertIn(5, loc)
	self.assertIn(6, loc)


class test_dyn_self(unittest.TestCase):
    """ Tests for the static threshold, suggest to neighbour popularity table"""
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = t_stat_topology()
        model = NetworkModel(topology, 
                             cache_policy={'name': 'POP_SELF_DYN'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Pop_self_dyn(self.view, self.controller)

	hr.process_event(1, 1, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertNotIn(7, loc)
	self.assertIn(6, loc)
        summary = self.collector.session_summary()
        #check the requests took correct path
        exp_req_hops = set([(1,2), (2,3), (3,4), (4,5), (5,6)])
        #check content took correct path
       	exp_cont_hops = set([(6,5), (5,4), (4,3), (3,2), (2,1)])
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(6, summary['serving_node'])
	print "first session summary"
        
	# content 2 should be on every node of the route
        loc = self.view.content_locations(2)
	self.assertEqual(len(loc),1)
	t=self.view.get_threshold()
        for i in range(1,105):
	    hr.process_event(1, 1, 2, True)
	loc = self.view.content_locations(2)
	self.assertEqual(len(loc),5)
	self.assertNotIn(1, loc)
	self.assertIn(2, loc)
	self.assertIn(3, loc)
	self.assertIn(4, loc)
	self.assertIn(5, loc)
	self.assertIn(6, loc)
	self.assertNotIn(7, loc)
	self.assertNotIn(8, loc)
	self.assertNotIn(9, loc)
	self.assertNotIn(10, loc)
	
	hr.process_event(121,1,2,True)
	for j in range(2,5):
	    if j>2:    
		self.assertEqual(self.view.get_threshold_v(j),102)	    	    
   	    else:
		self.assertEqual(self.view.get_threshold_v(j),106)	    	    

		
    def assert_threshold(self,t1, t2):
	if t1==t2:
	    return True
	else:
	    return False
	
class test_dyn_neighbour(unittest.TestCase):
    """ Tests for the Dynamic threshold, suggest to neighbour popularity table"""
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = t_stat_topology()
        model = NetworkModel(topology, 
                             cache_policy={'name': 'POP_NEIGHBOUR_DYN'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Pop_neighbour_dyn(self.view, self.controller)

	hr.process_event(1, 1, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertNotIn(7, loc)
	self.assertIn(6, loc)
        summary = self.collector.session_summary()
        #check the requests took correct path
        exp_req_hops = set([(1,2), (2,3), (3,4), (4,5), (5,6)])
        #check content took correct path
       	exp_cont_hops = set([(6,5), (5,4), (4,3), (3,2), (2,1)])
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(6, summary['serving_node'])
	print "first session summary"
        
	# content 2 should be on every node of the route
        loc = self.view.content_locations(2)
	self.assertEqual(len(loc),1)
	
        for i in range(1,105):
	    hr.process_event(1, 1, 2, True)
	loc = self.view.content_locations(2)
	self.assertEqual(len(loc),7)
	self.assertNotIn(1, loc)
	self.assertIn(2, loc)
	self.assertIn(3, loc)
	self.assertIn(4, loc)
	self.assertIn(5, loc)
	self.assertIn(6, loc)
	self.assertIn(7, loc)
	self.assertIn(8, loc)
	self.assertNotIn(9, loc)
	self.assertNotIn(10, loc)
	
	hr.process_event(121,1,2,True)
	for j in range(2,5):
	    if j>2:    
		self.assertEqual(self.view.get_threshold_v(j),102)	    	    
   	    else:
		self.assertEqual(self.view.get_threshold_v(j),106)	    	    

		
    def assert_threshold(self,t1, t2):
	if t1==t2:
	    return True
	else:
	    return False

class test_dyn_neighbour_t(unittest.TestCase):
    """ Tests for the dynamic threshold, suggest to neighbour popularity table"""
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = t_stat_topology()
        model = NetworkModel(topology, 
                             cache_policy={'name': 'POP_NEIGHBOUR_T_DYN'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Pop_neighbour_t_dyn(self.view, self.controller)

	hr.process_event(1, 1, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertNotIn(7, loc)
	self.assertIn(6, loc)
        summary = self.collector.session_summary()
        #check the requests took correct path
        exp_req_hops = set([(1,2), (2,3), (3,4), (4,5), (5,6)])
        #check content took correct path
       	exp_cont_hops = set([(6,5), (5,4), (4,3), (3,2), (2,1)])
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(6, summary['serving_node'])
	print "first session summary"
	# check the caching to neighbour mecahnism        
        loc = self.view.content_locations(2)
	self.assertEqual(len(loc),1)
  
        for i in range(0,int(self.view.get_threshold() * 0.75)):
            hr.process_event(1, 1, 2, True)

        for k in range(0, int(self.view.get_threshold() * 0.25)):
            hr.process_event(1, 9, 2, True)

        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 5)
        self.assertNotIn(8, loc) 
	self.assertNotIn(10, loc) 
	self.assertNotIn(7, loc) 
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
	self.assertIn(5, loc)
	self.assertIn(6, loc)
	
	# check the udpate of threshold
	hr.process_event(121,1,2,True)

	self.assertEqual(self.view.get_threshold_v(2),100)	    	    		
	self.assertEqual(self.view.get_threshold_v(3),102)	    	    		
	self.assertEqual(self.view.get_threshold_v(4),102)	    	    		
	self.assertEqual(self.view.get_threshold_v(5),102)	    	    		
	self.assertEqual(self.view.get_threshold_v(7),100)	    	    		
	self.assertEqual(self.view.get_threshold_v(8),100)	    	    		
		
    def assert_threshold(self,t1, t2):
	if t1==t2:
	    return True
	else:
	    return False
	
"""
class TestOnPath2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = on_path_topology()
        model = NetworkModel(topology, cache_policy={'name': 'POPULARITY_TABLE'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Popularity_Table(self.view, self.controller)
        
        # receiver 0 requests 2, expect miss

	hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0, 1), (1, 2), (2, 3), (3, 4)))
        exp_cont_hops = set(((4, 3), (3, 2), (2, 1), (1, 0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(4, summary['serving_node'])
	#doesnt work, caches everywhere along path except for node next to requestor
	#Run 102 requests which should cause item 2 to cache everywhere since all thresholds will be met!
        for i in range(0,self.view.get_threshold()):
            hr.process_event(1, 0, 2, True)

        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 4)
        self.assertIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)

       


        loc = self.view.content_locations(2)
        print loc
        for i in range(0,1208):
            hr.process_event(i,0,2,True)
            #print self.view.dump_table(1)[2][0]

        loc = self.view.content_locations(2)
        print loc
        #self.assertEquals(len(loc), 21)

	
        print "Worked this far!!!"

class TestOffPath2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = off_path_topology()
        model = NetworkModel(topology, cache_policy={'name': 'POPULARITY_TABLE'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Popularity_Table(self.view, self.controller)
        
        # receiver 0 requests 2, expect miss

	hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
	self.assertNotIn(5, loc)
        summary = self.collector.session_summary()
        exp_req_hops = set(((0,5), (5,4)))
        exp_cont_hops = set(((4,5), (5,0)))
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(4, summary['serving_node'])
	#doesnt work, caches everywhere along path except for node next to requestor
	#Run 102 requests which should cause item 2 to cache everywhere since all thresholds will be met!
        for i in range(0,self.view.get_threshold()):
            hr.process_event(1, 0, 2, True)

        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 3)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
	self.assertIn(5, loc)
"""       
"""
class TestNRR(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = nrr_topology()
        model = NetworkModel(topology, cache_policy={'name': 'POPULARITY_TABLE'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Popularity_Table(self.view, self.controller)
        
        # receiver 0 requests 2, expect miss

	hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)
        summary = self.collector.session_summary()

        exp_req_hops = set([(4,6), (2, 4), (0, 2)])
       	exp_cont_hops = set([(4, 2), (2, 0), (6, 4)])
	#print exp_req_hops
	#print exp_cont_hops
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']

        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(6, summary['serving_node'])
	#doesnt work, caches everywhere along path except for node next to requestor
	#Run 102 requests which should cause item 2 to cache everywhere since all thresholds will be met!
        for i in range(0,self.view.get_threshold()):
            hr.process_event(1, 0, 2, True)

        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 5)
        self.assertNotIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
	self.assertIn(5, loc)
	self.assertIn(6, loc)
"""
"""
class TestLisa(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = lisa_topology()
        model = NetworkModel(topology, cache_policy={'name': 'POPULARITY_TABLE'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Popularity_Table(self.view, self.controller)
        
        # receiver 0 requests 2, expect miss

	hr.process_event(1, 0, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)
        self.assertNotIn(7, loc)
	self.assertNotIn(8, loc)
        summary = self.collector.session_summary()

        exp_req_hops = set([(0,1), (1,8), (8, 6)])
       	exp_cont_hops = set([(6,8), (8,1), (1,0)])
        req_hops = summary['request_hops']
        cont_hops = summary['content_hops']
	#print req_hops
	#print cont_hops

        self.assertSetEqual(exp_req_hops, set(req_hops))
        self.assertSetEqual(exp_cont_hops, set(cont_hops))
        self.assertEqual(6, summary['serving_node'])
	#doesnt work, caches everywhere along path except for node next to requestor
	#Run 102 requests which should cause item 2 to cache everywhere since all thresholds will be met!
        for i in range(0,self.view.get_threshold()):
            hr.process_event(1, 0, 2, True)

        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 4)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)
	self.assertIn(7, loc)
	self.assertIn(8, loc)
"""
"""
class TestLisa2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = lisa_topology()
        model = NetworkModel(topology, cache_policy={'name': 'POPULARITY_TABLE'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Popularity_Table(self.view, self.controller)
        
        # receiver 0 requests 2, expect miss

	hr.process_event(1, 5, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)
        self.assertNotIn(7, loc)
	self.assertNotIn(8, loc)
        summary = self.collector.session_summary()


        self.assertEqual(6, summary['serving_node'])
	#doesnt work, caches everywhere along path except for node next to requestor
	#Run 102 requests which should cause item 2 to cache everywhere since all thresholds will be met!
        for i in range(0,self.view.get_threshold()):
            hr.process_event(1, 0, 2, True)

        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 4)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)
	self.assertIn(7, loc)
	self.assertIn(8, loc)
"""
"""
class TestWing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass    
    
    def setUp(self):
        topology = wing_topology()
        model = NetworkModel(topology, cache_policy={'name': 'POPULARITY_TABLE'})
        self.view = NetworkView(model)
        self.controller = NetworkController(model)
        self.collector = TestCollector(self.view)
        self.controller.attach_collector(self.collector)
        
    def tearDown(self):
        pass

    def test_poptable(self):
        hr = strategy.Popularity_Table(self.view, self.controller)
        
        # receiver 0 requests 2, expect miss

	hr.process_event(1, 5, 2, True)
        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 1)
        self.assertNotIn(1, loc)
        self.assertNotIn(2, loc)
        self.assertNotIn(3, loc)
        self.assertNotIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)
        self.assertNotIn(7, loc)
	self.assertNotIn(8, loc)
        summary = self.collector.session_summary()


        self.assertEqual(6, summary['serving_node'])
	#doesnt work, caches everywhere along path except for node next to requestor
	#Run 102 requests which should cause item 2 to cache everywhere since all thresholds will be met!
        for i in range(0,self.view.get_threshold()):
            hr.process_event(1, 0, 2, True)

        loc = self.view.content_locations(2)
        self.assertEquals(len(loc), 5)
        self.assertNotIn(1, loc)
        self.assertIn(2, loc)
        self.assertIn(3, loc)
        self.assertIn(4, loc)
	self.assertNotIn(5, loc)
	self.assertIn(6, loc)
	self.assertNotIn(7, loc)
	self.assertIn(8, loc)
"""  



       


