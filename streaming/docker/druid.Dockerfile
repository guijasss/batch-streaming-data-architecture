# Use a base image
FROM openjdk:8-jre-alpine

# Set environment variables
ENV DRUID_VERSION=0.20.0
ENV DRUID_HOME=/opt/druid

# Install necessary tools
RUN apk --no-cache add curl tar bash perl

# Download and extract Apache Druid
RUN mkdir -p $DRUID_HOME && \
    curl -fsSL https://dlcdn.apache.org/druid/29.0.0/apache-druid-29.0.0-bin.tar.gz | \
    tar -xzf - --strip-components=1 -C $DRUID_HOME

# Expose ports
EXPOSE 8081 8082 8083 8090 8091

# Set Druid environment variables
ENV DRUID_XMX=512m
ENV DRUID_XMS=512m
ENV DRUID_NEWSIZE=256m
ENV DRUID_MAXNEWSIZE=256m
ENV DRUID_HOSTNAME=localhost

# # Copy custom configurations
# COPY conf/druid/_common $DRUID_HOME/conf/druid/_common
# COPY conf/druid/$DRUID_HOSTNAME $DRUID_HOME/conf/druid/$DRUID_HOSTNAME

# Set working directory
WORKDIR $DRUID_HOME

# Start Druid
CMD ["bin/start-nano-quickstart"]
