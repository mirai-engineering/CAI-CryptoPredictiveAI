use sqlx::postgres::PgPoolOptions;
use sqlx::PgPool;
// use std::env;

pub async fn get_pool(
    pg_host: &String,
    pg_port: &u16,
    pg_database: &String,
    pg_user: &String,
    pg_password: &String,
) -> PgPool {

    // export PREDICTION_API_DATABASE_URL="postgres://root:123@localhost:4567/dev"
    let database_url = format!(
        "postgres://{}:{}@{}:{}/{}",
        pg_user, pg_password, pg_host, pg_port, pg_database);

    // let database_url = env::var("PREDICTION_API_DATABASE_URL").unwrap();

    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url).await.unwrap();

    pool
}