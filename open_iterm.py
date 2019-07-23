import sublime
import sublime_plugin
import pipes
import os
from pprint import pprint
import subprocess

def get_root_paths(view):
	'''
	Get all root directories for project
	'''
	return view.window().folders()

def get_paths_from_selection(selection):
	'''
	Get paths for selected items in sidebar.
	'''
	paths = []
	for single_path in selection:
		if os.path.isdir(single_path):
			paths.append(single_path)
		else:
			paths.append(os.path.dirname(single_path))

	return paths

def get_file_path(view):
	'''
	Get the directory of the current file
	'''
	file = view.file_name()
	if file is not None:
		p = []
		p.append(os.path.dirname(file))
		return p

	file = view.window().active_view().file_name()
	if file is not None:
		p = []
		p.append(os.path.dirname(file))
		return p

class OpenItermCommand(sublime_plugin.WindowCommand):
	def __init__(self, *args, **kwargs):
		sublime_plugin.WindowCommand.__init__(self, *args, **kwargs)

		self.paths = []
		self.debug_info = {}
		self.debug_info['settings'] = {}

	def run(self, *dummy, **kwargs):
		file = kwargs.get('file', False)
		if file:
			paths = get_paths_from_selection(kwargs.get('paths', []))
		else:
			paths = get_root_paths(self.window.active_view())

		if not paths:
			paths = get_file_path(self.window.active_view())

		pprint(paths)
		self.paths = paths
		self.settings = sublime.load_settings('OpenIterm.sublime-settings')

		if len(self.paths) == 1:
			self.open_terminal_command(self.paths[0])
		elif len(self.paths) > 1:
			self.window.show_quick_panel(
				self.paths,
				self.open_selected_directory
			)

	def open_selected_directory(self, selected_index):
		'''
		This method is invoked by sublime quick panel
		'''
		if selected_index != -1:
			self.open_terminal_command(self.paths[selected_index])

	def open_terminal_command(self, path,):
		'''
		Open terminal with javascript
		'''
		command = []

		# get osascript from settings or just use default value
		command.append(self.settings.get('osascript'))

		# set path and terminal
		command.append('{dir}/OpenIterm/OpenIterm.js'.format(
			dir=sublime.packages_path()
		))
		command.append(pipes.quote(path))

		# open terminal
		proc = subprocess.Popen(
			command,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			startupinfo=None)
		(out, err) = proc.communicate()

		if self.settings.get('debug'):
			self.debug_info['path'] = path
			self.debug_info['cmd'] = ' '.join(command)
			self.debug_info['process_out'] = out
			self.debug_info['process_err'] = err
			self.debug_info['settings']['osascript'] = self.settings.get('osascript');
			self.debug()

	def debug(self):
		'''
		show some debug stuff when needed
		'''
		if self.settings.get('debug'):
			pprint("OpenIterm DEBUG START---")
			pprint(self.debug_info)
			pprint("OpenIterm DEBUG END---")

