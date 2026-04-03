# Frontend Dockerfile
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/ .

# Build the application
RUN npm run build

# Install serve for production
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Serve the build
CMD ["serve", "-s", "dist", "-l", "3000"]