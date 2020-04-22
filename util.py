import os
import ctypes

basename = os.path.basename
dirname = os.path.dirname
abspath = os.path.abspath
exists = os.path.exists
join = os.path.join


PACKAGE_DIR = dirname(abspath(__file__))

CLIB32 				= join(PACKAGE_DIR, 'clib', 'bin32', 'release')
CLIB64 				= join(PACKAGE_DIR, 'clib', 'bin64', 'release')
FRIDA_SCRIPTDIR 	= join(PACKAGE_DIR, 'frida_scripts')

def addressof(pointer):
	return ctypes.addressof(pointer.contents)

def void_pointer(addr):
	VOIDP = ctypes.POINTER(ctypes.c_void_p)
	p = ctypes.cast(addr, VOIDP)
	return p

def u32_pointer(addr):
	INTP = ctypes.POINTER(ctypes.c_uint)
	p = ctypes.cast(addr, INTP)
	return p

def u64_pointer(addr):
	INTP = ctypes.POINTER(ctypes.c_uint64)
	p = ctypes.cast(addr, INTP)
	return p

def u8_pointer(addr):
	U8P = ctypes.POINTER(ctypes.c_ubyte)
	p = ctypes.cast(addr, U8P)
	return p

def malloc(sz):
	return u8_pointer((ctypes.c_ubyte*sz)())

def str2PCSTR(s):
	return ctypes.c_char_p(bytes(s, 'ansi'))

def next_pow2(n):
	if n == 0:
		return 0
	out = n - 1
	out |= out >> 1
	out |= out >> 2
	out |= out >> 4
	out |= out >> 8
	out |= out >> 16
	return out + 1

