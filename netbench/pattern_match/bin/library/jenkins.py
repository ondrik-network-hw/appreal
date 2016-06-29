import random
import sys
from b_hash import b_hash
from bitstring import BitArray

class jenkins(b_hash):
    """This class computes jenkins hash function. The key of the function has to be implemented as a string"""
    def generate_seed(self):
        """Seed of Jenkins hash function is a integer value. This works correctly on 32 bit platforms. DO NOT use if int has not 32 bits"""
#        self.seed = random.randint(-sys.maxint-1,sys.maxint)
        self.seed = random.randint(-2147483648,2147483647)
        return True

    def _mix(self, a, b, c):
        """
            Mix three unsigned integers a, b, c.
        """
        a = (a-b) & 0xFFFFFFFF # Keep at 32 bits
        a = (a-c) & 0xFFFFFFFF
        a = (a^(c>>13)) & 0xFFFFFFFF
        b = (b-c) & 0xFFFFFFFF
        b = (b-a) & 0xFFFFFFFF
        b = (b^(a<<8)) & 0xFFFFFFFF
        c = (c-a) & 0xFFFFFFFF
        c = (c-b) & 0xFFFFFFFF
        c = (c^(b>>13)) & 0xFFFFFFFF
        a = (a-b) & 0xFFFFFFFF
        a = (a-c) & 0xFFFFFFFF
        a = (a^(c>>12)) & 0xFFFFFFFF
        b = (b-c) & 0xFFFFFFFF
        b = (b-a) & 0xFFFFFFFF
        b = (b^(a<<16)) & 0xFFFFFFFF
        c = (c-a) & 0xFFFFFFFF
        c = (c-b) & 0xFFFFFFFF
        c = (c^(b>>5)) & 0xFFFFFFFF
        a = (a-b) & 0xFFFFFFFF
        a = (a-c) & 0xFFFFFFFF
        a = (a^(c>>3)) & 0xFFFFFFFF
        b = (b-c) & 0xFFFFFFFF
        b = (b-a) & 0xFFFFFFFF
        b = (b^(a<<10)) & 0xFFFFFFFF
        c = (c-a) & 0xFFFFFFFF
        c = (c-b) & 0xFFFFFFFF
        c = (c^(b>>15)) & 0xFFFFFFFF

        return a, b, c

   
    def hash(self,key):
        b_hash.hash(self,key)
        """
            Compute Jenkins Hash of the key.

            :param key: input data to be hashed as list of integers, one for each byte.
            :type key: list(int)
            :returns: hash value.
            :rtype: int
        """
        a = b = 0x9e3779b9
        c = self.seed

        remain = len(key)
        i = 0
        
        while (remain >= 12):
            a += (ord(key[i+0])) + (ord(key[i+1])<<8) + (ord(key[i+2])<<16) + (ord(key[i+3])<<24)
            a = a & 0xFFFFFFFF # Keep at 32 bits...

            b += (ord(key[i+4])) + (ord(key[i+5])<<8) + (ord(key[i+6])<<16) + (ord(key[i+7])<<24)
            b = b & 0xFFFFFFFF

            c += (ord(key[i+8])) + (ord(key[i+9])<<8) + (ord(key[i+10])<<16) + (ord(key[i+11])<<24)
            c = c & 0xFFFFFFFF

            a, b, c = self._mix(a, b, c)

            i += 12
            remain -= 12


        #c = (c + len(key)) & 0xFFFFFFFF #Not required for constant key size
        # the first byte of c is reserved for the length

        if (remain >= 11):
            c = (c+(ord(key[i+10]) << 24)) & 0xFFFFFFFF
        if (remain >= 10):
            c = (c+(ord(key[i+9]) << 16)) & 0xFFFFFFFF
        if (remain >= 9):
            c = (c+(ord(key[i+8]) << 8)) & 0xFFFFFFFF
        if (remain >= 8):
            b = (b+(ord(key[i+7]) << 24)) & 0xFFFFFFFF
        if (remain >= 7):
            b = (b+(ord(key[i+6]) << 16)) & 0xFFFFFFFF
        if (remain >= 6):
            b = (b+(ord(key[i+5]) << 8)) & 0xFFFFFFFF
        if (remain >= 5):
            b = (b+(ord(key[i+4]))) & 0xFFFFFFFF
        if (remain >= 4):
            a = (a+(ord(key[i+3]) << 24)) & 0xFFFFFFFF
        if (remain >= 3):
            a = (a+(ord(key[i+2]) << 16)) & 0xFFFFFFFF
        if (remain >= 2):
            a = (a+(ord(key[i+1]) << 8)) & 0xFFFFFFFF
        if (remain >= 1):
            a = (a+ord(key[i+0])) & 0xFFFFFFFF

        a = a & 0xFFFFFFFF
        b = b & 0xFFFFFFFF
        c = c & 0xFFFFFFFF

        a, b, c = self._mix(a,b,c)
        #h1_data = BitArray(uint=a,length=32)
        #h2_data = BitArray(uint=b,length=32)
        #h3_data = BitArray(uint=c,length=32)
        #h_key = BitArray(bytes=key,length=20)
        #print(h_key.hex,h1_data.hex,h2_data.hex,h3_data.hex);

        self._last = a
        return a

class jenkins_wrapper(jenkins):
    """
        This class enables usage of the base jenkins class with input key divided into two parts like in class jenkins_fast.
    """
    def hash(self, key):
        """
            Concatenate the two parts of input key and return the result of jenkins hash function.
            Warning: the concatenation is per byte, the results is different then concatenation of BitArrays.

            :param key: input data to be hashed divided into two parts.
            :type key: tuple(int, int)
            :returns: Hash value.
            :rtype: int
        """
        return jenkins.hash(self, key[1] + key[0])

class jenkins_fast(jenkins):
    """
        This class defines faster variant of the jenkins hash function. The idea is that tthe key is divided into two parts by the user of the function.
        First part is hashed by classical jenkins hash function while the other part is just xored to the output of the jenkins hash.
    """
    
    def hash(self,key):
        """
            Key should be two tuple, where the first item is the key for jenkins hash while the second part is only xored to the first part.
            
            :param key: input data to be hashed divided into two parts.
            :type key: tuple(int, int)
            :returns: Hash value.
            :rtype: int
        """
        h1 = jenkins.hash(self,key[0]);
        h1_data = BitArray(uint=h1,length=32)
#        h2_data = BitArray(bytes=key[1])
        h2_data = BitArray(bytes=key[1]) 
        h2_data.prepend(BitArray(uint=0,length=32-(len(h2_data))))
        #h = h1^key[1];
        h3 = h1_data ^ h2_data;
        #print(h1_data.hex,h2_data.hex,h3.hex)
        #print(h3.uint &0x00000FFF)
        return h3.uint #& 0x000007FF;

class jenkins_compress(jenkins_wrapper):
    def __init__(self, output_size):
        """
            Class contructor.

            :param output_size: The size in bits of the hash value.
            :type output_size: int
        """
        jenkins.__init__(self)
        self.output_size = output_size

    def set_output_size(self, output_size):
        """
            Set the size of output hash value.

            :param output_size: The size in bits of the hash value.
            :type output_size: int
        """
        self.output_size = output_size

    def get_output_size(self):
        """
            Return the size of output hash value.

            :returns: The size in bits of the hash value.
            :rtype: int
        """
        return self.output_size

    def hash(self, key):
        """
            Compute the hash value of input data and truncate the result to the size specified by output_size.

            :param key: input data to be hashed divided into two parts.
            :type key: tuple(int, int)
            :returns: Hash value.
            :rtype: int
        """
        return jenkins_wrapper.hash(self, key) & (2 ** self.output_size - 1)
