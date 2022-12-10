from genie import testbed
testbed = testbed.load('testbed.yml')
testbed.connect()

output = testbed.parse('show version')
print(output)