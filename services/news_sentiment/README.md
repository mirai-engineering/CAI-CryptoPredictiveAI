## News sentiment service


### How to download historical news

```bash
make download-historial-news
```

### How to evaluate the model

For example, `deepseek-r1:7b` model:

```bash
make evaluate MODEL=openai-generic/deepseek-r1:7b
```

### How to evaluate on a single example

```bash
make evaluate-tricky-example MODEL=openai-generic/deepseek-r1:7b
```
