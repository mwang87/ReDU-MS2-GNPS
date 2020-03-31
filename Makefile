test-push:
	act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04
test-schedule:
	act schedule -P ubuntu-latest=nektos/act-environments-ubuntu:18.04
