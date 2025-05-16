#FROM nginx:alpine
#COPY index.html /usr/share/nginx/html/index.html
FROM nginx:alpine
COPY web/ /usr/share/nginx/html/
