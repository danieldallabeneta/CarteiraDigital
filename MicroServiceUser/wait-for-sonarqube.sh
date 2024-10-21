#!/bin/bash

# Espera o SonarQube estar disponível
until $(curl --output /dev/null --silent --head --fail http://sonarqube:9000); do
  printf '.'
  sleep 5
done

sonar-scanner
