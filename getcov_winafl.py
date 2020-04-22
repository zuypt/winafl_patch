from ctypes import *
import sys
import pickle
from util import *
from win_util import *

'''for 32bit change this to 4'''
PTR_SZ = 8

module_t_sz = 264

MAX_COV_MODULE =  8
MAP_SZ = 2**16
fuzzer_id  = sys.argv[1]

map_str = 'afl_shm_%s_MAP' % fuzzer_id
var_str = 'afl_shm_%s_VAR' % fuzzer_id
virgin_str = 'afl_shm_%s_VIRGIN' % fuzzer_id
module_str = 'afl_shm_%s_MOD' % fuzzer_id

MAP = map_shm(map_str, MAP_SZ*PTR_SZ)
MOD_INFO = map_shm(module_str, module_t_sz*MAX_COV_MODULE)
VIRGIN = map_shm(virgin_str, MAP_SZ)

def get_module_info():
	modules = []

	for i in range(MAX_COV_MODULE):
		start = u64_pointer(MOD_INFO)[module_t_sz//PTR_SZ*i]
		if start:
			mod = {}
			end = u64_pointer(MOD_INFO)[module_t_sz//PTR_SZ*i+1]
			j = 2*PTR_SZ + module_t_sz*i
			module_name = ''
			while MOD_INFO[j] != 0:
				module_name += chr(MOD_INFO[j])
				j += 1
			
			mod['start'] = start
			mod['end'] = end
			mod['name'] = module_name


			print (mod)
			modules.append(mod)
		else:
			break
	return modules

modules = get_module_info()

def get_map():
	r = []

	m = u64_pointer(MAP)
	for blk_id in range(MAP_SZ//PTR_SZ):
		addr = m[blk_id]
		if (addr == 0):
			break
		# print (hex(addr))
		assert(addr not in r)
		for mod in modules:
			if addr >= mod['start'] and addr <= mod['end']:
				addr -= mod['start']
				break
		r.append((addr, 1))

	return r

cov_dict = {
	'cov': get_map()
}

f = open('map.pkl', 'wb')
f.write(pickle.dumps(cov_dict, protocol=2))
f.close()


