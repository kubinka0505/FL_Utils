exec(open("Data/Scripts/core.py", encoding = "UTF-8").read())

#-=-=-=-#
# Setup

if CLI:
	Directory = os.sys.argv[1]
else:
	prompt_title = "Select directory containing files to remove from starred"
	print(prompt_title, end = "\r")

	Directory = fd.askdirectory(
		title = prompt_title,
		initialdir = os.path.dirname(os.getcwd())
	)

	print(" " * len(prompt_title), end = "\r")
	if not Directory:
		raise SystemExit("Operation cancelled by user.")

Directory = os.path.abspath(Directory)

#-=-=-=-#
# Function

def remove_from_starred(files_dir: str, allowed_extensions: tuple = None, recursive: bool = True, quiet: bool = True, dir_fl_data: str = None):
	"""
	Appends files to the FL Studio "STARRED" tab.

	Args:
		files_dir: Directory containing files to be removed.
		allowed_extensions: Collection containing extensions of the files to be copied. If None, all files are to be copied.
		recursive: Traverse subdirectories in order to find files.
		dir_fl_data: FL Studio DATA directory. If None, directory is retrieved automatically.
		quiet: Determines whether console output messages should appear.

	Raises:
		FileNotFoundError: If one of the directories or file responsible for "STARRED" tab does not exist.
	"""

	RunTime = time()

	if not dir_fl_data:
		dir_fl_data = os.path.expanduser(r"~/Documents/Image-Line/FL Studio")

	if allowed_extensions:
		allowed_extensions = tuple(set(["." + Format.lower().strip(".") for Format in allowed_extensions]))
	else:
		allowed_extensions = ""

	tags = os.path.join(dir_fl_data, "Settings/Browser", "Tags")

	#-=-=-=-#
	# Error handling

	traceback = 0

	if not os.path.exists(tags):
		traceback = "Tags file", tags
	if not os.path.exists(dir_fl_data):
		traceback = "FL Studio directory", dir_fl_data

	if traceback:
		raise FileNotFoundError(f'{0} does not exist ("{1}")'.format(*traceback))

	#-=--=-=-#
	# Get files

	Wildcard = "*.*"
	if recursive:
		Wildcard = "**/" + Wildcard

	Files = []

	for File in Path(files_dir).rglob("*.*"):
		File = str(File.resolve())

		if File.lower().endswith((allowed_extensions)):
			Files.append(File)

	Files.sort(key = str)

	Amount = len(Files)
	if not quiet:
		Counter = 0

	#-=--=-=-#
	# Append files

	with open(tags, "r") as Starred:
		Starred_Content = Starred.read()
		Starred_Files = Starred_Content.strip("\n")
		Starred_Files = Starred_Files.split("\n")

	#---#

	with open(tags, "w") as Starred:
		for File in Files:
			File_Display = os.path.basename(File)
			Line = f'"{File.lower()}",*'

			try:
				Width = os.get_terminal_size()[0]
			except ValueError:
				Width = 0

			if Line.lower() in Starred_Content.lower():
				Starred_Content = Starred_Content.replace(
					Line + "\n",
					""
				)

				if not quiet:
					Counter += 1
					Counter_STR = str(Counter).rjust(len(str(Amount)), "0")

					Message = f'[{Counter_STR}/{Amount}] "{File_Display}" has been removed from starred'
					Message += " " * (Width - len(Message) - 1)

					print("\r", end = Message)
			else:
				if not quiet:
					Counter_STR = str(Counter).rjust(len(str(Amount)), "0")

					Message = f'[{Counter_STR}/{Amount}] "{File_Display}" is not starred'
					Message += " " * (Width - len(Message) - 1)

					print("\r", end = Message)

		#-=-=-=-#

		Starred.write(Starred_Content)

	#---#

	RunTime = timedelta(seconds = time() - RunTime)

	print()
	if not quiet:
		print()
		print(f"Removed {Counter} files in {str(RunTime)[2:-3]}s")

#-=-=-=-#
# Execute

try:
	remove_from_starred(
		Directory,
		allowed_extensions = ("WAV", "FLAC", "MP3", "OGG"),
		recursive = True,
		quiet = False
	)
except (EOFError, KeyboardInterrupt):
	print("\n" + "Operation cancelled by user.")
except Exception as Error:
	Error = Error.__class__.__name__, Error

	print("{0}: {1}".format(*Error))
	MsgBox.showerror(*Error)

	raise SystemExit()