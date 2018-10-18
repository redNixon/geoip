.DEFAULT_GOAL := build

.PHONY: build-max-mind
build-max-mind:
	mkdir -p ~/.maxmind-data
	wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz -P /tmp/
	tar -xf /tmp/GeoLite2-City.tar.gz -C ~/.maxmind-data --strip-components 1 --wildcards --no-anchored *.mmdb
	rm /tmp/GeoLite2-City.tar.gz

	wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz -P /tmp/
	tar -xf /tmp/GeoLite2-Country.tar.gz -C ~/.maxmind-data --strip-components 1 --wildcards --no-anchored *.mmdb
	rm /tmp/GeoLite2-Country.tar.gz

	wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz -P /tmp/
	tar -xf /tmp/GeoLite2-ASN.tar.gz -C ~/.maxmind-data --strip-components 1 --wildcards --no-anchored *.mmdb
	rm /tmp/GeoLite2-ASN.tar.gz

.PHONY: clean
clean:
	pipenv
	rm -rf ~/.maxmind-data/

build-env:
	pipenv install --dev

.PHONY: build
build: build-env build-max-mind

.PHONY: run
run:
	pipenv run python api.py

.PHONY: test
test: build-env
	pipenv run py.test tests/

.PHONY: lint
lint:
	pipenv run pycodestyle ./
	pipenv run pydocstyle api.py
	pipenv run pydocstyle geoip/