# Stage 1: build the static files with Node.
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: serve the built files with a non-root Nginx (runs as uid 101, port 8080).
FROM nginxinc/nginx-unprivileged:1.31-alpine
# Apply the latest Alpine security patches (needs root), then run as non-root.
USER root
RUN apk upgrade --no-cache
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
USER 101
EXPOSE 8080
