FROM node:18

COPY package.json ./
COPY proxy-CheckRawFiles.py proxy-GetRawFiles.py requirements.txt run.sh server.js ./
COPY public/ ./

RUN apt-get update && \
    apt-get install -y python3 python3-pip make g++ && \
    pip3 install -r requirements.txt --break-system-packages

WORKDIR /app

RUN npm install
RUN npm install express-basic-auth ansi-to-html xterm-addon-fit

EXPOSE 3000

CMD ["node", "server.js"]