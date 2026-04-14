Download `uv` package manager if you don't have it, then run this after cloning repository:

```commandline
uv sync
```

## Development Environment (Docker)

To ensure a standardized environment across all operating systems, this project uses Docker. 

### Prerequisites
- Docker Desktop installed and running.

### Starting the Environment
To build the image and start the backend container, run the following command from the root of the project:

```commandline
docker-compose up --build