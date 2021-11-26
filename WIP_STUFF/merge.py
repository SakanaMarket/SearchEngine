import os
import re
import uuid

def merge_all_files():
	for rootdir,dirs,files in os.walk("merge"):
		merge_list = files
		length = len(merge_list)
		while( length != 1 ):
			merge_list.append( merge( rootdir, merge_list.pop(-1), merge_list.pop(-1)))
			length=len(merge_list)
		os.rename( os.path.join(rootdir,merge_list[0]), os.path.join(rootdir,"inverted_index.txt"))

def merge( rootdir, fir_file, sec_file ):
	filepath = str(uuid.uuid4())
	h = open( os.path.join( rootdir, filepath ), "w+" )
	f, g = open( os.path.join(rootdir,fir_file), "r" ), open( os.path.join(rootdir,sec_file), "r" )
	
	f_line = format_string( f.readline() )
	g_line = format_string( g.readline() )
	
	while f_line != "" and g_line != "":
		if f_line[0] == g_line[0]:
			fc_num, gc_num = sum( 1 for _ in f_line ), sum( 1 for _ in g_line )
			fc_count, gc_count = 1, 1
			while fc_count < fc_num and gc_count < gc_num:
				fposting = f_line[fc_count]
				gposting = g_line[gc_count]
				temp = []
				if fposting[0] == gposting[0]:
					temp.append((fposting[0],(fposting[1]+gposting[1]),max(fposting[2],gposting[2])))
					fc_count+=1
					gc_count+=1
				elif fposting[0] < gposting[0]:
					temp.append( fposting )
					fc_count+=1
				else:	
					temp.append( gposting )
					gc_count+=1
			while fc_count < fc_num and gc_count >= gc_num:
				fposting = f_line[fc_count]
				temp.append( fposting )
				fc_count+=1
			while fc_count >= fc_num and gc_count < gc_num:
				gposting = g_line[gc_count]
				temp.append( gposting )
				gc_count+=1
				
			h.write( "{key},{val}\n".format(key=f_line[0],val=temp) )
			f_line = format_string( f.readline() )
			g_line = format_string( g.readline() )

		elif f_line[0] < g_line[0]:			
			h.write( "{key},{val}\n".format(key=f_line[0],val=f_line[1:]) )
			f_line = format_string( f.readline() )
		else:
			h.write( "{key},{val}\n".format(key=g_line[0],val=g_line[1:]) )
			g_line = format_string( g.readline() )
	

	if f_line == "" and g_line != "": 
		h.write( "{key},{val}\n".format(key=g_line[0],val=g_line[1:]) )
		g_line = format_string( g.readline() )
		while( g_line != "" ):
			h.write( "{key},{val}\n".format(key=g_line[0],val=g_line[1:]))
			g_line = format_string( g.readline() )
	elif f_line != "" and g_line == "":
		h.write( "{key},{val}\n".format(key=f_line[0],val=f_line[1:]) )
		f_line = format_string( f.readline() )
		while( f_line != "" ):
			h.write( "{key},{val}\n".format(key=f_line[0],val=f_line[1:]))
			f_line = format_string( f.readline() )
	
	h.close()			
	f.close()
	g.close()
	
	os.remove( os.path.join( rootdir, fir_file ) )
	os.remove( os.path.join( rootdir, sec_file ) )

	return filepath

# takes in f_line and g_line
def format_string( string ):
	if string == "":
		return string
	string_list = re.split( ",(?![^()]*\))", string )
	temp = [string_list[0]]
	for val in string_list[1:]:
		temp.append( tuple( int(num) for num in re.sub("[\[\]\(\)\n ]*","",val).split(",")) )
	return temp

if __name__ == "__main__":
	merge_all_files()
