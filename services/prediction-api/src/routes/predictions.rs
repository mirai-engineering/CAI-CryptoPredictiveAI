use axum::{
    // routing::get,
    extract::{ Query, State },
    Json,
};
use serde::{Deserialize, Serialize};
// use sqlx::postgres::PgPoolOptions;
// use std::env;
use log::info;

use crate::AppState;

#[derive(Deserialize)]
pub struct PredictionParams {
    pair: String,
}

#[derive(Serialize, sqlx::FromRow)]
pub struct PredictionOutput {
    pair: String,
    predicted_price: f64,
    
    // TODO: add these fields with proper types so we can fetch them form the view
    // We need to know the time horizon for which we make the `predicted_price` prediction
    // ts_ms: i8,
    // predicted_ts_ms: i8,
}

pub async fn get_prediction(
    params: Query<PredictionParams>,
    State(app_state): State<AppState>,
) -> Json<PredictionOutput> {

    // TODO: debug why we are getting nulls here. This is what generates an invalid sql query that returns no data.
    let pair = &params.0.pair;
    info!("Requested prediction");

    let pool = app_state.pool;
    let pg_view = app_state.config.pg_view_name;

    // let query = format!("SELECT pair, predicted_price, ts_ms, predicted_ts_ms FROM public.{} WHERE pair = '{}'", pg_view, pair);
    let query = format!("SELECT pair, predicted_price FROM public.{} WHERE pair = '{}'", pg_view, pair);

    let prediction_output = sqlx::query_as::<_, PredictionOutput>(
        &query
    )
    .fetch_one(&pool).await.unwrap();

    info!("Returning prediction to the client");
    
    Json(prediction_output)

}