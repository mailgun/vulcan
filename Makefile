test:
	trial vulcan
coverage:
	coverage run --source=vulcan `which trial` vulcan
	coverage report --show-missing
pep:
	pep8 vulcan
run:
	python run.py -c development.yml
clean:
	find -name "*pyc" -delete
	find -name "*py~" -delete
	rm -rf _trial_temp
