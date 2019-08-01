FROM node:12-alpine

WORKDIR /app
COPY package.json *yarn* /app/
RUN yarn

COPY . /app
EXPOSE 8080

ENTRYPOINT ["yarn", "start"]
