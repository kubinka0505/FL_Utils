exec(open("Data/Scripts/core.py", encoding = "UTF-8").read())

#-=-=-=-#
# Setup

if CLI:
	Show_Directory_After_Copying = os.sys.argv[1].lower() in ("true", "1", "t", "y", "yes")
else:
	open_dir_prompt = MsgBox.askyesnocancel(
		"Question",
		"Open output directory in file explorer after copying?",
		default = "no"
	)

	if open_dir_prompt:
		Show_Directory_After_Copying = True
	if open_dir_prompt is False:
		Show_Directory_After_Copying = False
	if open_dir_prompt is None:
		raise SystemExit("Operation cancelled by user.")

#-=-=-=-#
# Function

def copy_starred(dir_out: str = None, allowed_extensions: tuple = None, quiet: bool = True, dir_fl_data: str = None):
	"""
	Copies all files from the FL Studio "STARRED" tab to target destination.

	Args:
		dir_out: Directory to which the files are to be copied. If None, directory is created automatically.
		allowed_extensions: Collection containing extensions of the files to be copied. If None, all files are to be copied.
		dir_fl_data: FL Studio DATA directory. If None, directory is retrieved automatically.
		quiet: Determines whether console output messages should appear.

	Raises:
		FileNotFoundError: If one of the directories or file responsible for "STARRED" tab does not exist.

	Returns:
		Output directory. 
	"""

	RunTime = time()

	if not dir_out:
		dir_out = os.path.join("Files", "_BackupStarred")

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
	# Copying files

	with open(tags, "r") as Starred:
		Starred_Files = Starred.read().strip("\n")
		Starred_Files = Starred_Files.split("\n")
		if len(Starred_Files) < 2:
			raise ValueError("No starred files found")

		Starred_Files = [File.split('"')[1] for File in Starred_Files[1:]]
		Starred_Files = [str(Path(File).resolve()) for File in Starred_Files if os.path.exists(File)]
		Starred_Files = [File for File in Starred_Files if os.path.splitext(File.lower())[-1].endswith(allowed_extensions)]

		if not Starred_Files:
			raise ValueError("No starred files with allowed extensions has been found")

		Amount = len(Starred_Files)
		if not quiet:
			Counter = 0

		#-=-=-=-#

		for File in Starred_Files:
			File_SD = os.path.relpath(os.path.splitdrive(File)[-1])
			Dir_SD = os.path.abspath(os.path.splitdrive(dir_out)[-1])

			File_SD = File_SD.replace(".." + os.sep, "")
			Dir_SD = os.path.join(Dir_SD, os.path.dirname(File_SD))

			Destination = os.path.join(Dir_SD, os.path.basename(File))

			#-=-=-=-#

			if not quiet:
				Counter += 1
				Counter_STR = str(Counter).rjust(len(str(Amount)), "0")
				try:
					Width = os.get_terminal_size()[0]
				except ValueError:
					Width = 0
				Message = f'[{Counter_STR}/{Amount}] Copying "{os.path.basename(File)}"'
				Message += " " * (Width - len(Message) - 1)
 
			os.makedirs(Dir_SD, exist_ok = True)
			copy(File, Destination)

			if not quiet:
				print("\r", end = Message)

	#-=-=-=-#

	RetVal = os.path.abspath(os.path.normpath(dir_out))
	RunTime = timedelta(seconds = time() - RunTime)

	print()
	if not quiet:
		print()
		print(f"Done in {str(RunTime)[2:-3]}s")
		print(f'Saved in "{RetVal}"')

	return RetVal

#-=-=-=-#
# Execute

try:
	Destination = copy_starred(
		0,
		allowed_extensions = ("WAV", "FLAC", "MP3", "OGG"),
		quiet = False
	)
except (EOFError, KeyboardInterrupt):
	print("\n" + "Operation cancelled by user.")
except Exception as Error:
	Error = Error.__class__.__name__, Error

	print("{0}: {1}".format(*Error))
	MsgBox.showerror(*Error)

	raise SystemExit()

#-=-=-=-#
# Show directory

if Show_Directory_After_Copying:
	if os.sys.platform.lower().startswith("win"):
		Command = r'C:\Windows\explorer.exe "{0}"'
	else:
		Command = r'open "{0}"'
	Command = Command.format(Destination)

	os.system(Command)