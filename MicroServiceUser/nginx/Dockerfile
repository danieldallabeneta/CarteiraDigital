# Usa a imagem oficial do NGINX
FROM nginx:latest

# Remove o arquivo de configuração padrão do NGINX
RUN rm /etc/nginx/nginx.conf

# Copia o arquivo de configuração personalizado do NGINX para dentro do container
COPY ./nginx.conf /etc/nginx/nginx.conf

# Define o diretório de trabalho
WORKDIR /etc/nginx

# Exponha a porta 80 para requisições HTTP
EXPOSE 80

# Comando para iniciar o NGINX no container
CMD ["nginx", "-g", "daemon off;"]
