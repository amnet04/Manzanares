import re

def ChunkReader(inputfile, chunkSize=1, end=""):
	with open(inputfile, 'r') as f:
		chunk_count = -1
		while True:
			data = f.read(chunkSize)
			if not data:
				break
			else:
				while  not  re.compile(end).match(data[-1:]):
					next_chunk = f.read(1)
					if next_chunk != "":
						data += next_chunk
					else:
						break
				chunk_count += 1 		
				yield (chunk_count, data)
	yield ""

