import os

if not os.path.exists('build32'):
	os.mkdir('build32')
if not os.path.exists('build64'):
	os.mkdir('build64')

os.chdir('build32')
os.system(r'cmake -G"Visual Studio 15 2017" .. -DDynamoRIO_DIR=C:\DynamoRIO\cmake')
os.system(r'cmake --build . --config Release')

os.chdir('..\\build64')
os.system(r'cmake -G"Visual Studio 15 2017 Win64" .. -DDynamoRIO_DIR=C:\DynamoRIO\cmake')
os.system(r'cmake --build . --config Release')