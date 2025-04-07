# Session 1

### Table of contents


## Goals for today

- [x] Deploy Kafka in our dev kubernetes cluster.
- [x] Deploy the Kafka UI in our dev kubernetes cluster.
- [x] Push some fake data to Kafka

    Kind configuration sets up the port forwarding to the kafka broker.

    ```
    # kind-with-portmapping.yaml
    - containerPort: 31234
        hostPort: 31234
        listenAddress: "127.0.0.1"
        protocol: TCP
    ```

    Trick to check connectivity to the Kafka broker on TCP:
    ```
    $ nc -vvv localhost 31234
    ```

- [x] Push some real data to Kafka


## Questions

- How do we notify to ML algo to retrain with new features?
- Is the feature pipeline different the data pipeline?
- Do we make predictions with the same features used to train the models?
- Where does the correction of unexpected missing values happen: in the feature store or during inference in the inference pipeline? unexpected missing values designate deviation from the training dataset.
- We use features with data that is arriving all the time. Ideally, this new data should have similarity to the features that you trained the model on
- Can we deploy everywhere we want with kuberrnetees?
- Do we need GPU for this project locally?
- Can you tell us about the pros and cons for kafka in case of batch or real time problems?
- First time trying out Kubernetes and Docker, any resources before jumping onto?
- Can we imagine outliers detection in this project? If yes, in what step will they be treated?
- Give us some equivalent tools of kafka ?
- Cons and pros for kafka ?
- Suppose your API is producing data fastly and your service is down. Does kafka have live limits for keeping data ?
- Does kafka handle retries in case of failures?
- Do we need the port forwarding command in the install_kafka_ui.sh script

- For installing kafka into kubernetes cluster, are these standard scripts or do we need to modify sometimes?

- The trade producer will be running in the same cluster as the trade producer, so which port should we use?

- Are topic in kafka contains images ?

- Great Pau, can you generate algorithm (step by step ) for websocket.py micro service with all methods you defined to build ,, It will helpful to understand and build ourselves ( basically low level design )?

- @Pau, how do you suggest to utilize Tuesdays or learn effectively after the each session?

## Feedback

- Add diagrams 
- Use devcontainer

- Push trades image to the ghcr and make it public.
    - Marius to create basic deployment.yaml with env values for kafka.
    - A4000