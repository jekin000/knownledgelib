all:spiderclient.pyc parserserver.pyc parser.pyc spider.pyc store.pyc
	mkdir -p knownledgelib
	cp src/parser.pyc knownledgelib
	cp src/spider.pyc knownledgelib
	cp src/store.pyc knownledgelib
	cp src/spiderclient.pyc knownledgelib
	cp src/parserserver.pyc knownledgelib

parser.pyc:src/parser.py
	python -m compileall src/parser.py

spider.pyc:src/spider.py
	python -m compileall src/spider.py

store.pyc:src/store.py
	python -m compileall src/store.py

spiderclient.pyc:src/spiderclient.py
	python -m compileall src/spiderclient.py
parserserver.pyc:src/parserserver.py
	python -m compileall src/parserserver.py
clean:
	rm -Rf src/*.pyc knownledgelib

