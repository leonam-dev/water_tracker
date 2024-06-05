build:
	docker build -t water_tracker .

run: build
	docker run -p 5000:5000 water_tracker

test: build
	docker run --rm water_tracker pytest