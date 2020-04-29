from PIL import Image as img

# Determines the best picture width and height for n bytes of data
def bestBox(n):
	# Upper bound on smallest measure is the ceiling of the square root of n
	ub = int(n ** 0.5) + 1
	best = [1, n] # Start with a 1 x n rectangle
	for k in range(2, ub):
		if n // k == n / k: # if k divides n
			j = n // k # We have j x k == n
			# if j and k are closer than the current best factors
			if j - k < best[1] - best[0]: 
				# then they make a better box
				best = [k, j]
	return best

def bytesToGrayImage(b):
	l = len(b)
	# Mode "L" is 8-bit grayscale
	return img.frombytes("L", bestBox(l), b)

def grayImageToBytes(i):
	return bytes(i.getdata())

def saveImage(i, filename):
	i.save(filename)
