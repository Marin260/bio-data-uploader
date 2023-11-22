FROM golang:1.21 

WORKDIR /app

COPY ./ ./

# Go commands
RUN mkdir /app/output
RUN mkdir /app/logs

RUN go build -o bin ./cmd

# Python env
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

RUN python3 -m venv /app/py/venv
RUN . /app/py/venv/bin/activate
ENV PATH="/app/py/venv/bin:$PATH"
RUN pip install -r /app/py/requirements.txt

# Server port
EXPOSE 8080

ENTRYPOINT [ "/app/cmd/bin" ]
