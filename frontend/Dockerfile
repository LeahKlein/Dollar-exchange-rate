FROM node:14

WORKDIR /app

# העתק את כל הקבצים לתוך התמונה
COPY . .

WORKDIR /app/my-app

EXPOSE 3000

# התקן את התלויות
RUN npm install

CMD ["npm", "start"]