FROM nginx:alpine

# Elimina la página por defecto de nginx que interfiere
RUN rm -rf /usr/share/nginx/html/*

# Copia todo el contenido del sitio
COPY web/ /usr/share/nginx/html/

# Asegura los tipos MIME y rutas válidas
COPY nginx.conf /etc/nginx/nginx.conf
