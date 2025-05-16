#FROM nginx:alpine
#COPY index.html /usr/share/nginx/html/index.html
FROM nginx:alpine
# Copiamos archivos web
COPY web/ /usr/share/nginx/html/
# Copiamos la configuración personalizada
COPY nginx.conf /etc/nginx/nginx.conf
