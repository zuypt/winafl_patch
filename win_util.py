import platform

from ctypes import *
from ctypes.wintypes import *

from util import *

FILE_MAP_ALL_ACCESS = 0xF001F
PAGE_READWRITE 		= 0x04
INVALID_HANDLE_VALUE = DWORD(-1).value

def create_shm(name, sz):
	kernel32_dll = windll.kernel32

	CreateFileMappingA = kernel32_dll.CreateFileMappingA
	CreateFileMappingA.argtypes = (HANDLE, LPVOID, DWORD, DWORD, DWORD, LPCSTR)
	CreateFileMappingA.restype = HANDLE

	MapViewOfFile = kernel32_dll.MapViewOfFile
	MapViewOfFile.restype = LPVOID

	hMapObject = CreateFileMappingA(-1, None, PAGE_READWRITE, 0, sz, c_char_p(bytes(name, 'ansi')))
	if not hMapObject or hMapObject == 0:
		raise Exception('Could not open file mapping object, GetLastError = %d' % GetLastError())

	pBuf = MapViewOfFile(hMapObject, FILE_MAP_ALL_ACCESS, 0, 0, sz)
	if not pBuf or pBuf == 0:
		raise Exception('Could not map view of file, GetLastError = %d' % GetLastError())
	return u8_pointer(pBuf)

def map_shm(name, sz):
	kernel32_dll = windll.kernel32

	OpenFileMappingA = kernel32_dll.OpenFileMappingA
	OpenFileMappingA.argtypes = (DWORD, BOOL, LPCSTR)
	OpenFileMappingA.restype = HANDLE

	MapViewOfFile = kernel32_dll.MapViewOfFile
	MapViewOfFile.argtypes = (HANDLE, DWORD, DWORD, DWORD, DWORD)
	MapViewOfFile.restype = LPVOID

	hMap = OpenFileMappingA(FILE_MAP_ALL_ACCESS, 0, c_char_p(bytes(name, 'ansi')))
	assert(hMap != INVALID_HANDLE_VALUE)
	pBuf = MapViewOfFile(hMap, FILE_MAP_ALL_ACCESS, 0, 0, sz)
	if not pBuf or pBuf == 0:
		raise Exception('Could not map view of file, GetLastError = %d' % GetLastError())
	return u8_pointer(pBuf)