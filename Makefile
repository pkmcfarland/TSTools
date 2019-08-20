# This marks the "test" target as 'phony', which means that it isn't based on actual
# files. Make has a ton of magic in it, and one of the bits of magic is it won't
# rebuild a target if it doesn't think any of its dependencies have changed. Phony
# means its not based on on-disk targets, so always build it when invoked
.PHONY: test

# The test target makes sure all docker images are up to date and runs the test
# suite
test:
	docker-compose down && docker-compose build test && docker-compose run test && docker-compose down
