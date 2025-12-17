FROM python:3-slim

# Set environment variables for timezone (optional)
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install necessary packages
RUN apt-get update && \
    apt-get install -y cron curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Create a directory for the config file
RUN mkdir -p /etc/config

# Copy the current directory contents into the container at /app
COPY --chown=root:root . /app
# Install Python dependencies
RUN pip install -r dependencies.txt

# Create script to run the command
RUN echo '#!/bin/bash' > run.sh
RUN echo "/usr/local/bin/python /app/strato_ddns.py -i --config /etc/config/strato_ddns.conf" >> run.sh
RUN chmod +x run.sh

# Create a cron schedule file using an environment variable
RUN echo "*/5 * * * * /app/run.sh >> /proc/1/fd/1 2>&1" > /cronjob && \
    crontab /cronjob

# Run the command on container start and then according to the cron schedule
CMD ["/bin/bash", "-c", "/app/run.sh && cron -f"]
