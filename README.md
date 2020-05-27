# Interactive

Interactive is a Python tool aiming to simplify the coding of command-driving tools.

Command-driving program usually needs to parse the user input, look up the commands, and sometimes provides a `help` function. `interactive` package does these for you, and make everything easier.

Example program:

```python
#!/usr/bin/env python3
import interactive as I
import os

@I.command()
def ls():
	'''Usage: ls
List the content of the current directory.'''
	print(*os.listdir(), sep = '\n')

@I.command((0,1))
def hello(name = 'world'):
	'''Usage: hello [NAME]
Say hello to NAME.'''
	print('Hello, {}!'.format(name))

@I.command((1,0), [float])
def add(*args):
	'''Usage: add NUMBER...
Calculate the sum of NUMBERs and print the result.'''
	print('Sum =', sum(args))

I.prompt = 'Enter command ("help" for help): '
I.main()
```

running:

```
Enter command ("help" for help): help
Available commands: ls hello add
Enter "help <command>" for the help of <command>.
Enter nothing to exit the program.

Enter command ("help" for help): help add
Help for command add:

Usage: add NUMBER...
Calculate the sum of NUMBERs and print the result.

Enter command ("help" for help): add 24 76
Sum = 100.0
Enter command ("help" for help): hello
Hello, world!
Enter command ("help" for help): hello everyone
Hello, everyone!
Enter command ("help" for help): ls
interactive
main.py
Enter command ("help" for help):
```



## License

MIT License.

