'''interactive -- terminal interaction helper

'''

prompt = '--> '

def _input(prompt = ''):
	result = ''
	try:
		result = input(prompt)
	except EOFError:
		pass
	return result

def main():
	line = _input(prompt)
	while len(line) > 0:
		line = _input(prompt)

__all__ = list(filter(lambda s: not s.startswith('_'), dir()))
