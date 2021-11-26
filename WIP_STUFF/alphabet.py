def categorize_index():
	alpha = [ chr(n) for n in range(97,123) ]
	f = open("inverted_index.txt", "r")
	g = open("alphabet.txt","w")
		
	counter=0
	a_counter=0	
	for line in f:
		if( a_counter > 25 ):
			break	
		if line.startswith( alpha[a_counter] ):
			g.write("{alpha},{index}\n".format(alpha=alpha[a_counter],index=counter))
			a_counter+=1		
		counter+=len(line)
	
	f.close()
	g.close()

def print_alpha():
	f = open("inverted_index.txt", "r")	
	g = open("alphabet.txt","r")
		
	for line in g:
		a_o = line.split(",")
		f.seek( int( a_o[1] ))	
		print("{alpha},{word}".format(alpha=a_o[0], word=f.readline()))
	
	f.close()
	g.close()


if __name__ == "__main__":
	print_alpha()						
