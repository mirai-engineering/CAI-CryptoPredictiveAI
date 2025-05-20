// basic handler that responds with a static string
pub async fn health() -> &'static str {
    // let name: String = "my name".to_string();

    "I am healthy!"
}