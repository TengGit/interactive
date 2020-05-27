'''interactive -- terminal interaction helper

'''

import sys as _sys
from traceback import print_exc as _print_exc

_registered = {}
prompt = '--> '

def _input(prompt = ''):
	result = ''
	try:
		result = input(prompt)
	except EOFError:
		pass
	return result

def _map(args, mapspec):
	result = args[1:]
	if mapspec is not None and len(mapspec) > 0:
		length = len(mapspec) - 1
		for i in range(len(result)):
			result[i] = mapspec[i](result[i]) if i <= length else mapspec[length](result[i])
	return result

def _help(cmd):
	if cmd in _registered:
		print('Help for command {}:\n'.format(cmd))
		print(_registered[cmd].__doc__)
		print()

def command(argspec = 0, mapspec = None):
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
					func(*_map(args, mapspec))
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
					func(*_map(args, mapspec))
		wrapped.__doc__ = func.__doc__
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
				_print_exc(file=_sys.stdout)
		elif line[0] == 'help' and len(line) > 1:
			for cmd in line[1:]:
				_help(cmd)
		else:
			print('Available commands:', ' '.join(_registered.keys()))
			print('Enter "help <command> for the help of <command>."')
			print('Enter nothing to exit the program.')
		line = _input(prompt).split()

__all__ = list(filter(lambda s: not s.startswith('_'), dir()))
