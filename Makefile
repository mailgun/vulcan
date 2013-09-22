test: clean
	go test
coverage: clean
	gocov test | gocov report
annotate: clean
	FILENAME=$(shell uuidgen)
	gocov test  > /tmp/--go-test-server-coverage.json
	gocov annotate /tmp/--go-test-server-coverage.json $(fn)
all:
	go install github.com/mailgun/vulcan
	go install github.com/mailgun/vulcan/vulcan
clean:
	find -name flymake_* -delete
run: all
	GOMAXPROCS=4 vulcan -stderrthreshold=INFO -logtostderr=true -c=http://localhost:5000 -b=memory -lb=random -csnode=localhost -cskeyspace=vulcan_dev
sloccount:
	 find . -name "*.go" -print0 | xargs -0 wc -l
