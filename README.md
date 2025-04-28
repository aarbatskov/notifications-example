# notifications

## Quick Start

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/aarbatskov/notifications-example.git
    cd orders-example
    ```

2. Запуск служебных сервисов: БД, Zookeeper, Kafka:

    ```bash
    docker compose --profile infra up --build -d
    ```
3. Создайте и заполните .env файл в соответствии с .env_example
4. Запуск основного сервиса:

    ```bash
    docker compose --profile api up
