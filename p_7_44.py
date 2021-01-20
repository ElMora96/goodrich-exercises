"""Write a simple text editor that stores and displays a string of characters
using the positional list ADT, together with a cursor object that highlights
a position in this string. A simple interface is to print the string and then
to use a second line of output to underline the position of the cursor. Your
editor should support the following operations:
• left: Move cursor left one character (do nothing if at beginning).
• right: Move cursor right one character (do nothing if at end).
• insert c: Insert the character c just after the cursor.
• delete: Delete the character just after the cursor (do nothing at end)."""
###############LIBRARIES###########################
from os import  system
from libs.positional_list import PositionalList 

###############EDITOR###############
class StringPositionalList(PositionalList):
	"""Subclass of PositionalList to represent strings for SimpleEditor"""
	def __init__(self, input_string = None):
		"""Extend to read given input string"""
		super().__init__()
		if input_string:
			if not isinstance(input_string, str): #Check if given input is a string
				raise TypeError("Input must be a string")
			else:
				self._initialize_string(input_string)

	def __str__(self):
		"""String representation"""
		string = '' #Empty string
		for element in self:
			string += str(element)
		return string

	def  _initialize_string(self, string):
		"""Load Initial String"""
		pos = self.add_first(string[0]) #Initialize position pointer e set first element
		for char in string[1:]: #Iterate over other chars
			pos = self.add_after(char, pos) #Add char and update position



class SimpleEditor():
	"""PositionalList-based minimal text editor"""
	class _Interface:
		"""Simple CLI""" 
		def __init__(self, editor):
			"""container is the outer editor object"""
			self._container = editor
			self._string = editor.string
			self._prompt = '>>>' #Prompt to insert commands
			self._position = self._string.last() #Initialize position
			self._cursor = self._container._Cursor(self._container, self._position) #Build initial cursor
			while(True): #Program loop
				self._refresh()
		
		def _refresh(self):
			"""Refresh ClI at each update"""
			system("cls") #Clear screen
			print("""Mora's SimpleEditor. Supported Commands: 'left', 'right', 'delete', insertion of a char. """)
			print(self._string)
			print(self._cursor)
			print(self._prompt, end ='')
			self._read_input()			
			

		def _read_input(self):
			"""Read CLI input and perform corresponding update actions"""
			cli_input = input()
			if cli_input == 'left':
				if self._position != self._string.first():
					self._position = self._string.before(self._position) #Move cursor left; do nothing if beginning
			elif cli_input == 'right':
				if self._position != self._string.last():
					self._position = self._string.after(self._position) #Move cursor right
			elif isinstance(cli_input, str) and  len(cli_input) == 1: #Short-circuits
				self._position = self._string.add_after(cli_input, self._position)#Insert the character just after the cursor
			elif cli_input == 'delete':
				if self._position != self._string.last():
					self._string.delete(self._string.after(self._position)) #Delete the character just after the cursor
			else:
				print("Invalid Input, try again.")
			self._cursor = self._container._Cursor(self._container, self._position) #Refresh cursor

	class _Cursor:
		"""Cursor object that highlights current position"""
		def __init__(self, editor, p):
			"""editor is the outer object, p is the PositionalList position"""
			self._original_string = editor.string
			self._position = p

		def __str__(self):
			"""String represenation"""
			string = '' #Empty string
			pos = self._original_string.first() #Initialize position
			for char in self._original_string: #Iterate over list
				if pos == self._position: 
					string += '_' #If position is current; place a cursor
				else:
					string += ' ' #Else place an empty char
				pos = self._original_string.after(pos)
			return string

	def __init__(self, input_string = None):
		"""Text Editor"""
		self.string = StringPositionalList(input_string)
		self._CLI = self._Interface(self)
		 

###############UNIT TEST###############
if __name__ == "__main__":
	value = "Follow the White Rabbit"
	mora_edit = SimpleEditor(value)

