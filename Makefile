SHELL := /bin/bash

help:
	@echo ""
	@echo "--------------- STT docker compose commands ---------------"
	@echo ""
	@echo "make"
	@echo "    stt-all-docker"
	@echo "        Install all supported speech to text (stt) services (local and third party)."
	@echo "    stt-all-kaldi-docker"
	@echo "        Install all supported speech to text (stt) services (based on docker kaldi images and third party)."
	@echo "    stt-kaldi-fr-docker"
	@echo "        Install only kaldi french speech to text service."
	@echo "    stt-kaldi-en-docker"
	@echo "        Install only kaldi english speech to text service."
	@echo "    stt-local-docker"
	@echo "        Install only local speech to text services."
	@echo "    stt-local-fr-docker"
	@echo "        Install only french speech to text (stt) local service."
	@echo "    stt-local-en-docker"
	@echo "        Install only english speech to text (stt) local service"
	@echo "    stt-third-party-docker"
	@echo "        Install only third-party speech to text services."
	@echo ""


# stt docker compose make commands
stt-all-docker:
	docker-compose \
		--env-file ./.env \
		-f ./stt/docker-compose-stt.yml \
		up -d

stt-all-kaldi-docker:
	docker-compose \
	--env-file ./.env \
	-f ./stt/docker-compose-stt-kaldi.yml \
	up -d

stt-kaldi-fr-docker:
	docker-compose \
		--env-file ./.env \
		-f ./stt/kaldi-docker/docker-compose.yml \
		up stt-fr_fr -d

stt-kaldi-en-docker:
	docker-compose \
		--env-file ./.env \
		-f ./stt/kaldi-docker/docker-compose.yml \
		up stt-en_us -d

stt-local-docker:
	docker-compose \
		--env-file ./.env \
		-f ./stt/docker-compose-stt-local.yml \
		up -d

stt-local-fr-docker:
	docker-compose \
		--env-file ./.env \
		-f ./stt/docker-compose-stt-local.yml \
		up stt-fr_fr -d

stt-local-en-docker:
	docker-compose \
		--env-file ./.env \
		-f ./stt/docker-compose-stt-local.yml \
		up stt-en_us -d

stt-third-party-docker:
	docker-compose \
		--env-file ./.env \
		-f ./stt/docker-compose-stt.yml \
		up stt-third-party -d