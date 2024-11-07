# Specify the base image with JDK
FROM gradle:7.6.1-jdk17 AS build

# Set the working directory
WORKDIR /app

# Copy only the necessary files for the build
COPY gradle/ gradle/
COPY gradlew gradlew
COPY build.gradle.kts settings.gradle.kts ./
COPY src/ src/

# Build the project
RUN chmod +x gradlew
RUN ./gradlew build --no-daemon

# Specify the base image for running the application
FROM openjdk:17-jdk-slim

# Set the working directory
WORKDIR /app

# Copy the compiled application from the previous stage
COPY --from=build /app/build/libs/*.jar app.jar

# Set the command to run the application
ENTRYPOINT ["java", "-jar", "app.jar"]