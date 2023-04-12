FROM node:19-alpine as builder
RUN apk add python3 make g++
WORKDIR /app
COPY . .
RUN npm install --development && npm run build


FROM nginx:1.23-alpine
EXPOSE 80
COPY ./docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/nginx/html