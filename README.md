## margeryStapletonArt

### Creation commands:-
docker rm -f margeryStapletonArt

docker build -t my-custom-nginx .

docker run --name margeryStapletonArt -p 8081:8081 -v content:/usr/share/nginx/html:ro -d my-custom-nginx

