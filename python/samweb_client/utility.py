
from exceptions import *

# Calculate the enstore style CRC for a file
# Raises a standard python IOError in case of failures
# Uses the adler32 algorithm from zlib, except with an initial
# value of 0, instead of 1, and adler32 returns a signed int (ie 32 bits)
# while we want an unsigned value



def fileChecksum(path, checksum_types=None, oldformat=False):
    """Calculate enstore compatible CRC value"""
    try:
        f =open(path,'rb')
    except (IOError, OSError), ex:
        raise Error(str(ex))
    try:
        return calculateChecksum(f, checksum_types=checksum_types, oldformat=oldformat)
    finally:
        f.close()

def calculateChecksum(fileobj, checksum_types=None, oldformat=False):
    algorithms = {}
    if oldformat:
        if not (checksum_types is None or checksum_types==['enstore']):
            raise Error("Old format checksums only support enstore type")
        algorithms["enstore"] = _get_checksum_algorithm("enstore")
    else:
        if checksum_types is None: checksum_types = ["enstore"]
        for ct in checksum_types:
            algorithms[ct] = _get_checksum_algorithm(ct)

    readblocksize = 1024*1024
    while 1:
        try:
            s = fileobj.read(readblocksize)
        except (OSError, IOError), ex:
            raise Error(str(ex))
        if not s: break
        for a in algorithms.itervalues():
            a.update(s)

    if oldformat:
        return { "crc_value" : algorithms["enstore"].value(), "crc_type" : "adler 32 crc type" }
    else:
        return [ "%s:%s" % (a,v.value()) for a,v in algorithms.iteritems() ]

# for compatibility
def fileEnstoreChecksum(path):
    return fileChecksum(path, oldformat=True)
def enstoreChecksum(fileobj):
    return calculateChecksum(fileobj, oldformat=True)

# Don't create the algorithm classes unless they are actually needed

_Adler32 = None
def _make_adler32(startval=None):
    global _Adler32
    import zlib
    if _Adler32:return _Adler32(startval)

    class _Adler32(object):
        def __init__(self, startval=None):
            if startval is not None:
                self._value = zlib.adler32('', startval)
            else:
                self._value = zlib.adler32('')
        def update(self, data):
            self._value = zlib.adler32(data, self._value)
        def value(self):
            crc = long(self._value)
            if crc < 0:
                # Return 32 bit unsigned value
                crc  = (crc & 0x7FFFFFFFL) | 0x80000000L
            return crc

    return _Adler32(startval)

_Hasher = None
def _make_hash(algorithm):

    global _Hasher
    if not _Hasher:
        class _Hasher(object):
            def __init__(self, hasher):
                self.hash = hasher
            def update(self, data):
                self.hash.update(data)
            def value(self):
                return self.hash.hexdigest()

    try:
        from hashlib import md5,sha1,new
    except ImportError:
        from md5 import new as md5
        from sha import new as sha1
        new = None

    if algorithm == 'md5':
        return _Hasher(md5())
    elif algorithm == 'sha1':
        return _Hasher(sha1())
    elif new:
        try:
            return _Hasher(new(algorithm))
        except ValueError:
            pass

    raise Error("No checksum algorithm for %s" % algorithm)

def _get_checksum_algorithm(algorithm):

    if algorithm == 'enstore':
        return _make_adler32(0)
    elif algorithm == 'adler32':
        return _make_adler32()
    else:
        return _make_hash(algorithm)

