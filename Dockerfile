ARG PORT=443
FROM cypress/browsers:latest
RUN apt-get install python3 -y
RUN echo $(python3 -m site --user-base)
COPY requirements.txt .
ENV PATH /home/root/.local/bin:${PATH}
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
# Create a directory to store the chromedriver
# RUN mkdir /app/drivers
# Copy chromedriver to the desired location in the container
COPY drivers/chromedriver .
# Set execute permissions on chromedriver
RUN chmod +x drivers/chromedriver

# CMD uvicorn main:app --host 0.0.0.0 --port $PORT
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:80"]
