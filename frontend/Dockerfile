# Node base image
FROM node:20-alpine

# Working directory
WORKDIR /app

# package.json copy 
COPY package*.json .

# Dependencies install 
RUN npm install

# whole frontend copy 
COPY . .

# Build 
RUN npm run build

# Port expose 
EXPOSE 5173

# Dev server run 
CMD ["npm", "run", "dev", "--", "--host"]