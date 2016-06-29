import unittest
import sys
from b_hash import *
from jenkins import jenkins
from bdz import bdz
from h3_hash import h3_hash

class BasicHashTest(unittest.TestCase):
    """ Test basic functions of the hash function implemented in netbench library"""
    def testCreateHash(self):
        """Creates instance of the b_Hash class to ensure that constructor works correctly"""
        Test = b_hash()
        bound = Test.get_size()
        self.assert_(bound[0] == -sys.maxint-1)
        self.assert_(bound[1] == sys.maxint)

    def testSeed(self):
        """Test function for seting and getting seed from b_Hash class"""
        Test = b_hash()
        self.assert_(Test.get_seed() == None)
        Test.set_seed(3)
        self.assert_(Test.get_seed() == 3)

    def testSetSize(self):
        """Tests if the set size fails on the b_Hash."""
        Test = b_hash()
        self.assert_(Test.set_size((2,5)) == False)

    def testCreateJenkins(self):
        """Creates Jenkins hash function and test if it works"""
        Test = jenkins()
        bound = Test.get_size()
        self.assert_(bound[0] == -sys.maxint-1)
        self.assert_(bound[1] == sys.maxint)

    def testJenkinsSeed(self):
        """Test function for seting and getting seed from jenkins hash"""
        Test = jenkins()
        self.assert_(Test.get_seed() == None)
        Test.set_seed(3)
        self.assert_(Test.get_seed() == 3)

    def testJenkinsSetSize(self):
        """Tests if the set size fails on the jenkins."""
        Test = jenkins()
        self.assert_(Test.set_size((2,5)) == False)

    def testJenkinsGenSeed(self):
        """Test if the seed generation works"""
        Test = jenkins()
        Test.generate_seed()
        Seed1 = Test.get_seed()
        self.assert_(Seed1 != None)
        Test.generate_seed()
        Seed2 = Test.get_seed()
        self.assert_(Seed1 != Seed2)

    def testJenkinsHash(self):
        """Computes value of the Jenkins hash"""
        Test = jenkins()
        Test.set_seed(13)
        self.assert_(Test.hash("TESTXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"))
        #Second call of the hash is to ensure that jenkins did not store the state
        self.assert_(Test.hash("TESTXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"))

    def testCreateBDZ(self):
        """Creates instance of the BDZ class to ensure that constructor works correctly"""
        Test = bdz()
        bound = Test.get_size()
        self.assert_(bound[0] == -sys.maxint-1)
        self.assert_(bound[1] == sys.maxint)
        self.assert_(Test.get_ratio() == 1.24)
        self.assert_(Test.get_iteration_limit() == 5)
        self.assert_(Test.get_order() == 3)
        self.assert_(Test.is_key_set() == False)

    def testSeedBDZ(self):
        """Test function for seting and getting seed from BDZ class"""
        #TODO: Rewrite so the used seed is compatible with BDZ
        Test = bdz()
        self.assert_(Test.get_seed() == None)
        Test.set_seed(3)
        self.assert_(Test.get_seed() == 3)

    def testSetSizeBDZ(self):
        """Tests if the set size fails on the BDZ."""
        Test = bdz()
        self.assert_(Test.set_size((2,5)) == False)

    def testSetGetFunction(self):
        """Tests setting and getting functions of BDZ class"""
        Test = bdz()
        Test.set_ratio(2)
        self.assert_(Test.get_ratio() == 2)
        Test.set_iteration_limit(10)
        self.assert_(Test.get_iteration_limit() == 10)
        Test.set_order(4)
        self.assert_(Test.get_order() == 4)
        self.assert_(Test.get_range() == -1)

    def testGenSeed(self):
        """Tests if generate_seed runs in BDZ class"""
        Test = bdz()
        Exc = False
        try:
           Test.generate_seed()
        except NoData:
           Exc = True
        self.assert_(Exc) #Exception should be generated
        Data = list(("KKK","AAA","TEST"))
        Test.set_keys(Data)
        self.assert_(Test.is_key_set())
        Exc = True
        try:
           Test.generate_seed()
        except NoData:
           Exc = False
        self.assert_(Exc) #Exception should not be generated
        self.assert_(Test.get_range() == 4) 
        
    def testJenkinsHash(self):
       """Computes the hash value for the given keys and tests its corectness"""
       Test = jenkins()
       Test.set_seed(13)
       h = Test.hash("0b000001000100000000111100001000") % 1753
       self.assert_(h == 1309)
      
    def testh3hash(self):
       """Tests h3 hash class"""
       Test = h3_hash()
       Test.set_bitsize(12)
       Test.set_input_size(50)
       Test.generate_seed()
       Test.hash("HGRFSRH")


if __name__ == '__main__':
   suite = unittest.TestLoader().loadTestsFromTestCase(BasicHashTest)
   unittest.TextTestRunner(verbosity=2).run(suite)
