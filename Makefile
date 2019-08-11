.PHONY: test
test:
	docker-compose down && docker-compose build test && docker-compose run test && docker-compose down