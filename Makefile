update:
	git pull

client, server:
	python $@/$@.py

install:
	pip3 install p5

glfw:
	sudo apt install libglfw3-dev