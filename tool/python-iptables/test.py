import os, json
# json = r"{'in-interface': 'ens38', 'protocol': 'tcp', 'iprange': {'src-range': '192.168.1.10-192.168.1.200'}, 'tcp': {'dport': '80'}, 'target': 'LOG'}")




def test_manual_rule_append():
	test_inp = {'tcp': {'dport': '22'}, 'protocol': 'tcp', 'comment': {'comment': 'Match tcp.22'}, 'target': 'ACCEPT'}
	print str(test_inp)
	test_inp = str(test_inp).replace('\'',r"\"")
	cmd = "python manual_input.py -A -r \"%s\"" % test_inp
	print cmd
	print os.system(cmd)

def test_manual_rule_insert(position):
	test_inp = {'tcp': {'dport': '22'}, 'protocol': 'tcp', 'comment': {'comment': str(position)+"New0"}, 'target': 'ACCEPT'}
	print str(test_inp)
	test_inp = str(test_inp).replace('\'',r"\"")
	cmd = "python manual_input.py -I %d -r \"%s\"" % (position, test_inp)
	print cmd
	print os.system(cmd)

def test_manual_rule_delete(position):

	cmd = "python manual_input.py -d %d " % (position)
	print cmd
	print os.system(cmd)
def test_blacklist_input():
	test_inp = "--add-rule"
	cmd = "python blacklist_input.py \"%s\"" % test_inp
	print cmd
	pparser.add_argument('--comment',
                        '-m',
                        type=str,
                        help='Comment for the rule')
	print os.system(cmd)
test_manual_rule_insert(1)
# test_manual_rule_delete(1)
def listruletest():
	cmd = "python manual_input.py -L "
	print cmd
	print os.system(cmd)


listruletest()
def convertIPtablesRuleToDict(rule):
	test = "-p tcp --destination-port 22 -m iprange --src-range 192.168.1.100-192.168.1.200 -j ACCEPT"
	cmd = "iptables -A TEST "+ test
