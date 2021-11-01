## build environment in docker
## is not necessary, Github Actions do it for us
# FROM node:15-alpine as build
# WORKDIR /app
# ENV PATH /app/node_modules/.bin:$PATH
# COPY package.json ./
# COPY package-lock.json ./
# RUN npm ci --silent
# COPY . ./
# RUN npm run build

# production environment
FROM nginx:stable-alpine
COPY ./build /usr/share/nginx/html
# COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

## run: docker run --rm -it -p 8080:80 ${image-id}
## go to 'localhost:8080' to see react app