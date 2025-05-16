FROM nginx:alpine

# Copiar archivos HTML y CSS (contenidos en la carpeta web)
COPY web/ /usr/share/nginx/html/

# Copiar configuración personalizada de NGINX
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
