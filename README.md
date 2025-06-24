## Short description

The goal of this project is to retrieve real-time data from kraken.com and to use ML models to predict crypto prices. This is an ongoing project, where I'm constantly searching for ways to optimze it and to discover new tools, as well as applying new ideas. This project will hopefully show you what a real-life ML project looks like, by having a fully-functional, end-to-end machine learning system.

Feel free to fork it and play on your own.

Currently I'm working on incorporating a sentiment-analysis pipeline using a fine-tuned LLM. To ensure reproducibility and scalability the project is  implemented using Kubernetes/Docker. 
### Tools used

- Kubernetes/Docker
- Python
- SQL
- Apache Kafka/Quixstreams
- RisingWave
- Minio
- Grafana (Data and error visualization)
- Screening of ML models with Scikit-learn
- Optuna (HP optimization)
- Mlflow (Model registry)
- Rust (Prediciton API)
- LLMs

### Quick Set-Up 
From now on I've decided to work in all my projects using `uv` for package management, as its versatility, ease of use and cleaninless are the best I've seen so far. Just take a look at https://docs.astral.sh/uv/.

Before moving forward, take a look at the `pyproject.toml` file in the root of this repo. It is linked to the python packages of all services, which allows a clean and modular management of python libraries, crucial for proper service containarization with Docker.

That being said, all you need to do is clone this repo and run the following command:
```bash
uv sync
```
This will automatically create a `.venv` and install the main dependencies. Additionally, you will need to run the following command once for each service:
```bash
uv add service/service_name
```
to ensure all the dependencies are installed within their own `pyproject.toml` files. 

### How it looks like

First, let's take a look at the current state of the development cluster using k9s:
<p align="center">
  <img src="https://github.com/brunoclbr/CryptoPredictiveAI/blob/bruno/images/k9s_services_all.png?raw=true" width="900" alt="Kafka UI">
</p>

The cluster was created using `kind`. The picture shows an overview of some of the services being deployed in the cluster, and will be referenced throughout this README.

## Data Ingestion Pipeline

The data is retrieved from Kraken and streamed through Apache Kafka for efficient handling and distribution. By port-forwarding the Kafka UI from the Kubernetes cluster, we can inspect what is happening inside the broker:
<p align="center">
  <img src="https://github.com/brunoclbr/CryptoPredictiveAI/blob/bruno/images/kafka_ui.png?raw=true" width="900" alt="Kafka UI">
</p>

In the data ingestion pipeline, the data is fetched and transformed into useful technical indicators to perform stocks-analysis, such as: 

- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Relative Strength Index (RSI)
- among others. 

This is the first step of the feature engineering process, where the input signal (crypto prices) is transformed into a more meaningful representation of the values, which will be later used to train the model. 

After this step, we can proceed to push the data to `RisingWave`. To this end, we install `RisingWave`, `Minio` and `Postgres` inside the same kubernetes service. This allows us to push and store the data by using a SQL query. This means that we need to start a PostgreSQL interactive session on the terminal, by running the following commands:

```bash
kubectl port-forward svc/risingwave-frontend-7849d74db9-dlc28 4567:4567 -n risingwave
psql -h localhost -p 4567 -d dev -U root
```

After port-forwarding the risingwave-service, we can tell `RisingWave` to pull the data from the broker with the `WITH` connector:
<pre><code>```CREATE TABLE technical_indicators (
    pair VARCHAR,
    open FLOAT,
    ...
    PRIMARY KEY (pair, window_start_ms, window_end_ms)
) WITH (
    connector='kafka',
    topic='technical_indicators',
    properties.bootstrap.server='PATH.local:9092'
) FORMAT PLAIN ENCODE JSON; ``` </code></pre>

Then use `\d` on the interactive session to check everything was created succesfully. (Alternatively a push-based approach can be done using the `RisingWave` python SDK)

The data is stored in MinIO buckets for efficient access and durability. `MLflow` is also installed at this stage, though it will be used later during the training phase for model tracking and evaluation.

<p align="center">
  <img src="https://github.com/brunoclbr/CryptoPredictiveAI/blob/bruno/images/minio.png?raw=true" width="900" alt="Kafka UI">
</p>

Finally, we can install and connect `Grafana` to our `Postgres` database to visualize the input features. As an example, here is a candle chart of some ingested crypto data:

<p align="center">
  <img src="https://github.com/brunoclbr/CryptoPredictiveAI/blob/bruno/images/grafana.png?raw=true" width="900" alt="Kafka UI">
</p>

Now, we are ready to enter the training pipeline.

## Training Pipeline
While the rest of the pipelines are up and ready, I'm still working on this part of the README 🚧

You can still wonder through the folders. This part of the project contains data validation, models and training scripts. The runs are registered in `Mlflow` and the predicted data is pushed to `RisingWave` using SQL one more time.

I'm also working in the fine-tuned LLM that will be added to the training pipeline to improve predictive accuracy.

## Inference Pipeline

The inference pipeline fetches the predictions from `RisingWave`  and uses a prediction API built on Rust 🦀 to produce real-time predictions in a efficient manner.
