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

def command(argspec = 0):
	def wrapper(func):
		name = func.__name__
		if isinstance(argspec, int):
			arg_num = argspec
			def wrapped(args):
				if len(args) - 1 != arg_num:
					raise TypeError('{name} requires {require} argument(s), but {actual} given'.format(
						name=args[0], require=arg_num, actual=len(args)-1
					))
				else:
					func(*args[1:])
		elif isinstance(argspec, tuple):
			if not (len(argspec) == 2 and isinstance(argspec[0], int) and isinstance(argspec[1], int)):
				raise TypeError('tuple(int, int) expected')
			def wrapped(args):
				length = len(args) - 1
				if length < argspec[0] or (argspec[1] != 0 and length > argspec[1]):
					raise TypeError('{name} requires {lower} to {upper} argument(s), but {actual} given'.format(
						name=args[0], lower=argspec[0], upper=argspec[1], actual=length
					))
				else:
					func(*args[1:])
		_registered[name] = wrapped
		return wrapped
	return wrapper

def main():
	line = _input(prompt).split()
	while len(line) > 0:
		if line[0] != 'help' and line[0] in _registered:
			try:
				_registered[line[0]](line)
			except Exception as e:
				print('{}: {}'.format(type(e).__name__, str(e)))
		else:
			print('Available commands:', ' '.join(_registered.keys()))
		line = _input(prompt).split()

__all__ = list(filter(lambda s: not s.startswith('_'), dir()))
