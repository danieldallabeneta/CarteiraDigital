#!/bin/bash

# Espera o SonarQube estar disponível
until curl -s http://sonarqube:9000/api/system/status | grep -q '"status":"OK"'; do
  echo "Aguardando o SonarQube iniciar..."
  sleep 5
done

# Executa o SonarScanner
echo "SonarQube está pronto! Executando o SonarScanner..."
sonar-scanner
