build:
	ghc -x hs extractor -o extractorExec
.PHONY: test
test: build
	mkdir -p test/output
	make Test.test

install:
	apt-get install haskell-platform
	cabal update
	cabal install json

%.test:
	./extractorExec < tests/$*.hs > log
	diff tests/$*.baseline log
	rm -f log

# Operational documentation of test data's origin
copy:
	cp ../../../101results/101repo/contributions/haskellStarter/*.hs tests/haskellStarter
	cp ../../../101results/101repo/contributions/haskellData/*.hs tests/haskellData

clean:
	rm -f log extractorExec *.o *.hi


