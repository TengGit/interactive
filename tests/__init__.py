import unittest
import sys
import io
sys.path.append('src')
import interactive

@interactive.command()
def cmd1():
	print('Success cmd1')

@interactive.command(1)
def hello(who):
	print('Hello, %s' % who)

@interactive.command((1,3))
def multi(first, second = None, third = None):
	if second is None:
		print('Single:', first)
	elif third is None:
		print('Double:', first, second)
	else:
		print('Triple:', first, second, third)

@interactive.command(2, (int,))
def plus(a, b):
	print(a + b)

@interactive.command()
def nothing():
	'''This function does nothing.'''
	pass

class Test(unittest.TestCase):
	def setUp(self):
		self.stdin  = sys.stdin
		self.stdout = sys.stdout
		self.prompt = interactive.prompt
		out = io.StringIO()
		sys.stdout = out

	def tearDown(self):
		sys.stdin  = self.stdin
		sys.stdout = self.stdout
		interactive.prompt = self.prompt

	def testChengePrompt(self):
		sys.stdin = io.StringIO()
		prompt_str = '(test) '
		interactive.prompt = prompt_str
		interactive.main()
		self.assertEqual(sys.stdout.getvalue(), prompt_str)

	def runCommand(self, str):
		sys.stdout = io.StringIO()
		sys.stdin  = io.StringIO(str + '\n')
		interactive.main()
		allstr = sys.stdout.getvalue()
		prompt = interactive.prompt
		length = len(prompt)
		assert len(allstr) >= length * 2
		assert allstr.startswith(self.prompt)
		assert allstr.endswith(self.prompt)
		return allstr[length:-length]

	def testEmptyCommand(self):
		self.assertEqual('Success cmd1\n', self.runCommand('cmd1'))

	def testSingleArgumentCommand(self):
		self.assertEqual('Hello, world\n', self.runCommand('hello world'))

	def testVariableArgumentCommand(self):
		self.assertEqual('Single: test\n', self.runCommand('multi test'))
		self.assertEqual('Double: blah blow\n', self.runCommand('multi blah blow'))
		self.assertEqual('Triple: foo bar baz\n', self.runCommand('multi foo bar baz'))

	def testErrorPrompt(self):
		self.assertNotEqual('Success cmd1\n', self.runCommand('cmd1 fail'))
	
	def testHelp(self):
		self.assertTrue(self.runCommand('help').startswith('Available commands:'), 'Help command error')

	def testMapspec(self):
		self.assertEqual('42\n', self.runCommand('plus 19 23'))
	
	def testDoc(self):
		self.assertIn('This function does nothing.', self.runCommand('help nothing'))
