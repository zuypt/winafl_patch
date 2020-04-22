import pickle
from ghidra.program.model.block import BasicBlockModel
from ghidra.program.model.block import SimpleBlockModel
from ghidra.program.model.block import SimpleBlockIterator

from docking.widgets.filechooser import GhidraFileChooser
from ghidra.program.model.address import Address
from ghidra.app.plugin.core.colorizer import ColorizingService
from java.awt import Color

def clear_color(block):
	clearBackgroundColor(block)

def highlight(block, c):
	setBackgroundColor(block, c)


COLORS = [Color.GREEN, Color.YELLOW]
COUNT = 0
def process_cov(cov):
	global COUNT
	global SBM

	hit_funcs = {}
	for addr, hitcount in cov:
		block 		= SBM.getCodeBlockAt(toAddr(addr), None)
		if block:
			block_addr 	= block.getMinAddress()
			if block_addr not in MAP:
				MAP[block_addr] = [hitcount]
				highlight(block, COLORS[COUNT])
			else:
				# print block_addr
				
				MAP[block_addr].append(hitcount)
				
				if MAP[block_addr][0] != MAP[block_addr][1]:
					highlight(block, Color.ORANGE)
				else:
					pass
					highlight(block, Color.CYAN)


				cmt = ''
				for hitcount in MAP[block_addr]:
					cmt += str(hitcount) + ' '
				setEOLComment(block_addr, cmt[:-1])

			func = getFunctionContaining(block_addr)
			if func is None:
				print 'Can not find function at', block.getMinAddress()
			else:
				if func.getName() not in hit_funcs:
					hit_funcs[func.getName()] = func
		else:
			print ('*** ' + hex(addr))

	print 'Number of function hit:', len(hit_funcs.keys())
	print 'Number of bb hit:', len(cov)
	for func_name in hit_funcs.keys():
		print func_name, 

	COUNT += 1


fc = GhidraFileChooser(None)
fc.setMultiSelectionEnabled(True)

filepaths = fc.getSelectedFiles()


'''
BBM = BasicBlockModel(currentProgram)
BBM create BB which contains CALL instr
'''

MAP = {}

SBM = SimpleBlockModel(currentProgram)

BlockIterator = SimpleBlockIterator(SBM, None)
while BlockIterator.hasNext():
	blk = BlockIterator.next()
	clear_color(blk)

for filepath in filepaths:
	with open(repr(filepath), 'rb') as f:
		cov_dict = pickle.loads(f.read())
		cov = cov_dict['cov']

		process_cov(cov)



