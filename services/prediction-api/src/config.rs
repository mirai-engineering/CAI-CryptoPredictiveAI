use std::env;

#[derive(Clone)]
pub struct Config {
    pub pg_host: String,
    pub pg_port: u16,
    pub pg_database: String,
    pub pg_user: String,
    pub pg_password: String,
    pub pg_view_name: String,
    pub api_port: u16,
}

impl Config {
    /// Loads configuration parameters from environment variables that have the same
    /// name in uppercase.
    pub fn from_env() -> Self {
        Self {
            pg_host: env::var("PG_HOST").unwrap(),
            pg_port: env::var("PG_PORT").unwrap().parse::<u16>().unwrap(),
            pg_database: env::var("PG_DATABASE").unwrap(),
            pg_user: env::var("PG_USER").unwrap(),
            pg_password: env::var("PG_PASSWORD").unwrap(),
            pg_view_name: env::var("PG_VIEW_NAME").unwrap(),
            api_port: env::var("API_PORT").unwrap().parse::<u16>().unwrap(),
        }
    }
}