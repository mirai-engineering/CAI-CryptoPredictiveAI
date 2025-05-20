use axum::{
    routing::get,
    Router,
};
use std::env;
use sqlx::PgPool;
use log::info;

mod routes;
mod db;
mod config;

use routes::health::health;
use routes::predictions::get_prediction;
use config::Config;

#[derive(Clone)]
struct AppState {
    pool: PgPool,
    config: Config,
}

// This is how you denote the entrypoint of a Rust program that uses async with tokio
#[tokio::main]
async fn main() {

    // Start the logger as early as possible as you can
    env_logger::init();

    // Load environment variables into a config struct
    let config: Config = Config::from_env();

    // Creating a single PgPool at start up
    info!("Creating pg pool...");
    let pool = db::get_pool(
        &config.pg_host,
        &config.pg_port,
        &config.pg_database,
        &config.pg_user,
        &config.pg_password,
    ).await;
    info!("Created pg pool!");

    // Creating the app state struct
    let app_state = AppState { pool, config: config.clone() };

    // build our application with a route
    let app = Router::new()
        // `GET /` goes to `root`
        .route("/health", get(health))
        .route("/predictions", get(get_prediction))
        .with_state(app_state);

    // run our app with hyper, listening globally on port 3000
    // let port = env::var("PORT").unwrap_or("3009".to_string());
    let listener = tokio::net::TcpListener::bind(format!("0.0.0.0:{}", &config.api_port)).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}