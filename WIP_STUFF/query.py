import nltk
import re
import math
from collections import defaultdict

def find_term( word ):
	a = open("alphabet.txt", "r")
	f = open("inverted_index.txt", "r")
	
	if not word[0].isalpha():
		return ""
		
	a_line = a.readline()
	while( a_line[0] != word[0] ):
		a_line = a.readline()
	f.seek( int(a_line.split(",")[1]) )
	
	f_line = f.readline()
	while( f_line[0] == word[0] ):
		if( f_line.startswith( word ) ):
			return re.split(",(?![^()]*\))",f_line)
		f_line=f.readline()
	
	a.close()
	f.close()
		
	return ""


def find( query ):
	if len(query) < 3: return []
	sno = nltk.stem.SnowballStemmer('english')
	with open( "out.txt", "r" ) as f:
		N = int( f.readline().split(":")[1] )
	
	score_dict = defaultdict(float)	
	L = [ find_term(sno.stem(word.lower())) for word in query.split() ]
	for tpost in L:
		df = len(tpost)-1			
		for ind in range(1,df):
			post = re.sub("[\(\)\[\]\n ]*","",tpost[ind]).split(",")
			tfidf = int(post[2]) + ((1+math.log(int(post[1]),10))*math.log((N/df),10))
			score_dict[post[0]] += tfidf
		
	return [ idtourl(k) for k in sorted(score_dict,key=score_dict.get)[-1:-6:-1]]

def idtourl( key ):
	f = open( "idurl.txt", "r" )
	for n in range(int(key)):
		next(f)
	url = f.readline().split(",")[1].strip("\n")
	f.close()
	return url
	
def search_interface():
	usr_query = input("Enter a query: ")
	while usr_query != "":
		results = find( usr_query )
		for r in results:
			print( r )
		usr_query = input("Enter another query: ")					


if __name__=='__main__':
	search_interface()

