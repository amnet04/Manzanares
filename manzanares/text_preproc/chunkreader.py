import re

def ChunkReader(inputfile, chunkSize=1, end=""):
	with open(inputfile, 'r') as f:
		while True:
			data = f.read(chunkSize)
			if not data:
				break
			while  not  re.compile(r'{}'.format(end)).match(data[-1:]):
				data+=f.read(1)
			yield data
	yield ""

