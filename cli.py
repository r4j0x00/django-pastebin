from argparse import *
from requests import post, get
from os import path
def get_lang_name(extension):
    l = {'py':'python','js':'javascript','c':'c','pl':'perl','css':'css','html':'html','rb':'ruby','php':'php'}
    if extension in l:
        return l[extension]
    return None

def main():
	parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
	description="""\
	    Cli For Pastebin Flask.
	    syntax highlighting is optional and is automatically chosen if file has extension.""")
	parser.add_argument('-f','--file', help='File To Post')
	parser.add_argument('-l', '--language', help='Language for syntax highlight')
	parser.add_argument('-d', '--disablesyntax', action='store_true', help='disable syntax higlight')
	parser.add_argument('-s', '--showlanguages', action='store_true', help='Languages Available for syntax highlighting')
	parser.add_argument('-H','--host', help='Default localhost',default='127.0.0.1')
	parser.add_argument('-p','--port', help='Default port 80',default='80')
	args = parser.parse_args()

	host = "http://{}:{}/".format(args.host,args.port)
	langs = ['python', 'javascript', 'c', 'ruby', 'perl', 'php', 'css', 'html']

	if args.showlanguages:
		print ("[+] Available Languages:")
		for i in langs:
	        	print (i)
		exit()
	r=''
	if args.file == None:
		parser.print_help()
		exit()
	elif args.file != None and args.language != None:
		file_data = open(args.file, 'r').read()
		if args.language.lower() in langs:
			print ("[+] Highlighting Syntax for "+args.language)
			r = post(host, data={"cont":file_data, "lang":args.language.lower()})
		else:
			print ("[+] Syntax Highlighting Not Available For The Language")
			r = post(host, data={"cont":file_data, "lang":"None"})

	elif args.file != None and args.language == None and args.disablesyntax == False:
		file_data = open(args.file, 'r').read()
		file_name = path.splitext(args.file)
		ext = file_name[1][1:]
		lang = get_lang_name(ext)
		if lang != None:
			print ("[+] Highlighting Syntax for "+lang)
			r = post(host, data={"cont":file_data, "lang":str(lang)})
	else:
		file_data = open(args.file, 'r').read()
		r = post(host, data={"cont":file_data, "lang":"None"})

	try:
		pasted = r.content.decode()[27:][:-11]
		print ("[+] Link to paste: "+pasted)
	except:
		pass

if __name__ == '__main__':
	main()
