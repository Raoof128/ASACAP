# Stage 1: Build the React application
FROM node:16-alpine as build

WORKDIR /app

COPY ./services/frontend/webapp/package.json ./
COPY ./services/frontend/webapp/package-lock.json ./

RUN npm install

COPY ./services/frontend/webapp ./

RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:1.21.6-alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
