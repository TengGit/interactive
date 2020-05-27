'''interactive -- terminal interaction helper

'''

_registered = {}
prompt = '--> '

def _input(prompt = ''):
	result = ''
	try:
		result = input(prompt)
	except EOFError:
		pass
	return result

def command():
	def wrapper(func):
		name = func.__name__

		def wrapped(args):
			return func()
		
		_registered[name] = wrapped
		return wrapped
	return wrapper

def main():
	line = _input(prompt).split()
	while len(line) > 0:
		if line[0] in _registered:
			_registered[line[0]](line)
		else:
			# Command isn't registered
			pass
		line = _input(prompt).split()

__all__ = list(filter(lambda s: not s.startswith('_'), dir()))
