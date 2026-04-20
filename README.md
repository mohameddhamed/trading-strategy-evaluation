# Trading Strategy Evaluation Framework

A vectorized backtesting framework in Python for evaluating quantitative trading strategies against market benchmarks.

## Local Setup (Without Docker)
Download the `uv` package manager if you don't have it, then run this after cloning the repository to install dependencies locally:

```commandline
uv sync
```

## Development Environment (Docker - Recommended)

To ensure a standardized environment across all operating systems, this project uses Docker. 

### Prerequisites
- Docker Desktop installed and running.

### Starting the Engine
To build the image and start the backend container (which currently serves as a placeholder for our future API), run the following command from the root of the project:

```commandline
docker-compose up --build
```
*Note: Because the `/src`, `/data`, `/scripts`, and `/app` directories are mounted as volumes, any code changes you make locally will instantly be reflected inside the container. You do not need to rebuild the image unless you add new dependencies.*

### Running the Strategy Demo
To test the quantitative logic and verify that the trading strategies (e.g., SMA Crossover, RSI Reversion) are generating signals and returns correctly, run the demo script inside the container:

```commandline
docker-compose run backend uv run python -m scripts.demo_strategies
```
This will generate a dummy dataset of 100 days, execute the algorithms, and print a pandas DataFrame showing the daily prices, strategy signals (+1, 0, -1), and daily returns.

### API Documentation & Testing (Swagger UI)
The engine runs a FastAPI backend server to communicate with the frontend UI.

Once the Docker container is running (`docker-compose up`), you can access the automatically generated interactive API documentation by navigating to:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

From this interface, you can explore the available endpoints, view the expected JSON schemas (like the `StrategyRequest` payload), and send live test requests directly to the engine.