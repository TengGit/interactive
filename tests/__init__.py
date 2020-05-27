import unittest
import sys
import io
sys.path.append('src')
import interactive

class Test(unittest.TestCase):
	def setUp(self):
		self.stdin  = sys.stdin
		self.stdout = sys.stdout
		out = io.StringIO()
		sys.stdout = out

	def tearDown(self):
		sys.stdin  = self.stdin
		sys.stdout = self.stdout

	def testChengePrompt(self):
		sys.stdin = io.StringIO()
		prompt_str = '(test) '
		interactive.prompt = prompt_str
		interactive.main()
		self.assertEqual(sys.stdout.getvalue(), prompt_str)


