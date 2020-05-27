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

	def testEmptyCommand(self):
		sys.stdin = io.StringIO('cmd1\n')
		interactive.main()
		self.assertIn('Success cmd1\n', sys.stdout.getvalue())

	def testSingleArgumentCommand(self):
		sys.stdin = io.StringIO('hello world\n')
		interactive.main()
		self.assertIn('Hello, world\n', sys.stdout.getvalue())

