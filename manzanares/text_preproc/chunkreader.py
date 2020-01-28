import re

def ChunkReader(inputfile, chunkSize=1, end=""):
	with open(inputfile, 'r') as f:
		while True:
			data = f.read(chunkSize)
			if not data:
				break
			while  not  re.compile(end).match(data[-1:]):
				next = f.read(1)
				if next != "":
					data += next
				else:
					break
			yield data
	yield ""

