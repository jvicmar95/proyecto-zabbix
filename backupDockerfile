FROM nginx:alpine

# Elimina la página por defecto
RUN rm -rf /usr/share/nginx/html/*

# Copia archivos HTML y CSS
COPY web/ /usr/share/nginx/html/

# Copia configuración personalizada
COPY nginx.conf /etc/nginx/nginx.conf
