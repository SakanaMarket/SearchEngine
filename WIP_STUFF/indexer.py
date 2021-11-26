import os
import re
import nltk
import json
import _pickle
import sys
import unicodedata
import copy
from datetime import datetime
from lxml import html
from lxml.html.clean import Cleaner
from urllib.parse import urlparse
from collections import defaultdict
## Ha Tran 5340976
## Leon Luo 72198827

inverted_index = defaultdict(list)
doc_id = 0

class Posting:
	def __init__(self, doc_id, tfidf, op):
		self.doc_id = doc_id
		self.tfidf = tfidf
		self.important = op
	def __repr__(self):
		return "({}, {}, {})".format(self.doc_id, self.tfidf, self.important)
	
def tokenize(j_file):
	a_flag = True
	u_flag = True
	global inverted_index, doc_id
	with open(j_file) as j:
		data = json.load(j)
		url = data["url"]
		
		if data["encoding"].lower() != "utf-8" and data["encoding"].lower() != "ascii":
			doc_id += 1
			return False

		saved = data["content"] 		
		if saved.strip() == "": 
			doc_id += 1
			return False
		saved = re.sub(r"([\w]*[^\x00-\x7F]+[\w]*)", "", saved)
		saved = "".join(ch for ch in saved if unicodedata.category(ch)[0]!="C")
		if data["encoding"].lower() == "ascii":
			saved = saved.encode("ascii")
		elif data["encoding"].lower() == "utf-8":
			saved = saved.encode("utf-8", "ignore")

		doc = html.fromstring(saved)

		body = Cleaner( style=True, links=True, scripts=True, javascript=True, remove_unknown_tags=True)
		body.kill_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "title", "A"]
			
		important = Cleaner( style=True, links=True, scripts=True, javascript=True, remove_unknown_tags=False )
		important.allow_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "title", "body"]
		important.kill_tags = ["canvas", "A"]

		sno = nltk.stem.SnowballStemmer('english')

		bod = [ re.sub(r"\t|\n|\.", " ", x.text).strip() for x in body.clean_html( doc ).xpath("//body//*") if x.text ]
		imp = [ re.sub(r"\t|\n|\.", " ", x.text).strip() for x in important.clean_html( doc ).xpath("//body//*") if x.text ]

		s1 = [ sno.stem(word.lower()) for line in imp for word in re.findall("[a-zA-Z\d\.]{3,}", line) if line ]
		s2 = [ sno.stem(word.lower()) for line in bod for word in re.findall("[a-zA-Z\d\.]{3,}", line) if line ]

		word_dict = defaultdict(int)

		for x in s1:
			word_dict[x]+=1
		for y in s2:
			word_dict[y]+=1
		
		s2 = set(s2)-set(s1)
		s1 = set(s1)

		for word in s2:
			inverted_index[word].append(Posting(doc_id, word_dict[word], 0))
		for word in s1:
			inverted_index[word].append(Posting(doc_id, word_dict[word], 1))
		doc_id += 1
		return True

def write_dictionary( filename ):
	global inverted_index
	if inverted_index:
		with open( filename, "w+") as f:
			for k in sorted( inverted_index ):  		
				f.write("{key},{value}\n".format(key=k,value=inverted_index[k]))	
			inverted_index.clear()	
		
if __name__ == '__main__':
	count = 0
	byte_threshold = 100000000
	num_bytes = 0
	filename_count = 0
	all_files = os.walk("/home/lopes/Datasets/IR/DEV")
	
	while( all_files is not None ):
		try:
			rootdir, dirs, files = next( all_files )
			file_count=0
			length=len(files)
			files=sorted(files)			

			while( file_count < length ):
				if( num_bytes < byte_threshold ):
					filepath = os.path.join( rootdir, files[file_count] )
					print( datetime.now(), filepath )
					if( tokenize( filepath ) ):
						count+=1
					num_bytes += os.path.getsize( filepath )
					file_count+=1
				else:
					write_dictionary("merge/merge{count}".format(count=filename_count))
					filename_count+=1
					num_bytes = 0
		except StopIteration:
			write_dictionary("merge/merge{count}".format(count=filename_count))
			all_files = None
	print("Finished processing...")
