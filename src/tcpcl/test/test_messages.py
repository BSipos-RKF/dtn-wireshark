
import unittest
from scapy import packet
from .. import messages

class TestMessageLayering(unittest.TestCase):
    ''' Verify MessageHead class and message types '''
    
    def testSerialize(self):
        pkt = messages.MessageHead()/messages.Keepalive()
        self.assertSequenceEqual(str(pkt), '40'.decode('hex'))
        
        pkt = messages.MessageHead()/messages.StartTls()
        self.assertSequenceEqual(str(pkt), '80'.decode('hex'))
        
        pkt = messages.MessageHead()/messages.RejectMsg(rej_id=7, rej_flags=0, reason='UNSUPPORTED')
        self.assertSequenceEqual(str(pkt), '707002'.decode('hex'))
        
        pkt = messages.MessageHead()/messages.BundleLength(bundle_id=1234, length=543210)
        self.assertSequenceEqual(str(pkt), '608952a1936a'.decode('hex'))
        
        pkt = messages.MessageHead()/messages.RefuseBundle(bundle_id=1234)
        self.assertSequenceEqual(str(pkt), '308952'.decode('hex'))
        
        pkt = messages.MessageHead()/messages.DataSegment(bundle_id=1234, data='hello')
        self.assertSequenceEqual(str(pkt), '10895205'.decode('hex') + 'hello')
        
        pkt = messages.MessageHead()/messages.AckSegment(bundle_id=1234, length=43210)
        self.assertSequenceEqual(str(pkt), '20895282d14a'.decode('hex'))
        
        pkt = messages.MessageHead()/messages.Shutdown()
        self.assertSequenceEqual(str(pkt), '50'.decode('hex'))
        pkt = messages.MessageHead(flags=messages.Shutdown.FLAG_REASON)/messages.Shutdown(reason=3)
        self.assertSequenceEqual(str(pkt), '5203'.decode('hex'))
        pkt = messages.MessageHead(flags=messages.Shutdown.FLAG_DELAY)/messages.Shutdown(conn_delay=500)
        self.assertSequenceEqual(str(pkt), '5101f4'.decode('hex'))
    
    def testDeserialize(self):
        pkt = messages.MessageHead('10895205'.decode('hex') + 'hellothere')
        pkt.show()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
