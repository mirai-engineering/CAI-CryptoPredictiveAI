-- I don't have the timestamp of the prediction as PRIMARY KEY.
-- This way the predictor generator will overwrite the prediction for the same pair, model_name, model_version, predicted_ts_ms.
CREATE TABLE price_predictions (
    pair VARCHAR,
    ts_ms BIGINT,
    
    -- useful for monitoring the model performance
    model_name VARCHAR,
    model_version INT,
    
    predicted_ts_ms BIGINT,
    
    predicted_price FLOAT,
    PRIMARY KEY (pair, ts_ms, model_name, model_version, predicted_ts_ms)
);