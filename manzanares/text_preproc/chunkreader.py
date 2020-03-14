import re

def ChunkReader(inputfile, chunkSize=1, end=""):
	with open(inputfile, 'r') as f:
		chunk_count = -1
		resto = "" 
		while True:
			data = resto + f.read(chunkSize)
			if not data:
				break
			else:
				
				while  not  re.compile(end).match(data[-1:]):
					next_chunk = f.read(1)
					
					if next_chunk != "":
						data += next_chunk
					else:
						break
						
				if "+" in end:
					while  re.compile(end).match(next_chunk):
						next_chunk  = f.read(1)
						if re.compile(end).match(next_chunk):
							data += next_chunk
						else:
							resto = next_chunk

				chunk_count += 1 		
				yield (chunk_count, data)
	yield False

