FROM node:20-alpine

WORKDIR /app

COPY clients/web/package.json clients/web/package-lock.json* ./
RUN npm install --no-audit --no-fund || true

COPY clients/web ./

EXPOSE 3000

CMD ["npm", "run", "dev"]

