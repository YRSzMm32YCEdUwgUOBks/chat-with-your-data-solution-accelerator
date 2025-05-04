FROM node:20-alpine AS frontend
ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app
WORKDIR /home/node/app
COPY ./code/frontend/package*.json ./
USER node
# RUN npm install --force
RUN npm ci
COPY --chown=node:node ./code/frontend ./frontend
WORKDIR /home/node/app/frontend
RUN npm install --save-dev @types/node @types/jest
RUN npm run build

FROM node:20-alpine AS runtime
WORKDIR /app
# Copy built frontend static assets
COPY --from=frontend /home/node/app/dist/static ./build
# Install a minimal static server
RUN npm install -g serve
EXPOSE 80
# Serve the app on port 80
CMD ["serve", "-s", "build", "-l", "80"]
