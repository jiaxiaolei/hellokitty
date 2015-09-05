from pybloomfilter import BloomFilter
# appconfig.py

BF_ROOT = BloomFilter(10000000, 0.01)

BF_RESOURCES = BloomFilter(10000000, 0.01)