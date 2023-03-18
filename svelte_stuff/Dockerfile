FROM node:19.8-alpine3.16

WORKDIR /app
COPY . /app

RUN ls

RUN npm install

RUN npm install -g wscat

RUN npm run build

EXPOSE 8080
ENV HOST=0.0.0.0

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "8080"]
