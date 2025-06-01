### Short description

The goal of this project is to retrieve real-time data from kraken.com and to use ML models to predict crypto prices. This is an ongoing project where I'm constantly searching for ways to optimze it and to discover new tools and apply new ideas. This project is mainly for learning purposes by having a fully-functional, real, end-to-end machine learning system.

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

### How it looks like

Let's take a look first at the state of the development cluster using k9s:
<p align="center">
  <img src="https://github.com/brunoclbr/CryptoPredictiveAI/blob/bruno/images/k9s_services_all.png?raw=true" width="500" alt="Kafka UI">
</p>

The cluster was created using `kind`. The picture shows an overview of some of the services being deployed in the cluster and will be referenced throughout this README.

## Data Ingestion Pipeline

The data is retrieved from Kraken and processed with Apache Kafka for efficient data-handling and storage. By port-forwarding the UI from the Kubernetes cluseter we can see what is happeing inside the broker:
<p align="center">
  <img src="https://github.com/brunoclbr/CryptoPredictiveAI/blob/bruno/images/kafka_ui.png?raw=true" width="500" alt="Kafka UI">
</p>

In the ingestion pipeline the data is fetched and transformed into useful technical indicators to perform stocks-analysis, such as: Simple Moving Average (SMA), Exponential Moving Average (EMA), Relative Strength Index (RSI), among others. This is the first step of the feature engineering process, where the input signal (crypto prices) is transformed into useful values to train the model. 

After this step, we can proceed to push the data to `RisingWave`. To this end, we install `RisingWave`, `Minio` and `Postgres` inside the same kubernetes service. This allows to push data using a SQL query so that `RisingWave` pulls the data using:
<pre><code>```CREATE TABLE technical_indicators (
    pair VARCHAR,
    open FLOAT,
    ...
    PRIMARY KEY (pair, window_start_ms, window_end_ms)
) WITH (
    connector='kafka',
    topic='technical_indicators',
    properties.bootstrap.server='PATH.local:9092'
) FORMAT PLAIN ENCODE JSON;; ``` </code></pre>

Alternatively a pushed-based approach can be done using the `RisingWave` python SDK.

With `Minio` the data will be efficiently stored into buckets. `Mlflow` is also installed in this step, but will be used during the training process for model monitoring and evaluation. The next picture shows the `Minio` interface:

<p align="center">
  <img src="https://github.com/brunoclbr/CryptoPredictiveAI/blob/bruno/images/minio.png?raw=true" width="500" alt="Kafka UI">
</p>

Finally, we can install and connect `Grafana` to our `Postgres` database to visualize the input features:

<p align="center">
  <img src="https://github.com/brunoclbr/CryptoPredictiveAI/blob/bruno/images/grafana.png?raw=true" width="500" alt="Kafka UI">
</p>

Now, we are ready to enter the training pipeline.

## Training Pipeline

## Inference Pipeline