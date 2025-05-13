# Quizm user backend
**Микросервис отвечающий за работу с пользователями, явяется частью сайта для прохождения квизов Quizm**


## Архитектуры и зависимости

### Используемые технологии

- Python 3.10
- FastAPI
- SQLAlchemy
- Alembic
- Pytest
- Uvicorn
- Black
- Flake8

### Взаимодействие с другими микросервисами

- [Микросервис для работы с квизами](https://github.com/frogen436/quizm-quiz-backend)

## Запуск 

### Запуск через docker

Указать переменные среды и поднять контейнер
```
docker-compose up
```

### Альтернативный запуск без docker
```
uvicorn app.main:app
```

### Переменнтые среды
```dotenv
DB_HOST # Хост базы данных (указать db при запуске через docker)
DB_PORT # Порт бызы данных
DB_NAME # Название бызы данных
DB_USER # Пользователь бызы данных
DB_PASSWORD # Пароль бызы данных
SECRET_KEY # Ключ для шифрования
ALGORITHM # Алгоритм шифрования
QUIZM_BACKEND_ADDRESS # Адрес микросервиса для квизов
QUIZM_FRONTEND_ADDRESS # Адрес фронтенда для принятия CORS запросов
```
## API документация
<details>
<summary><strong>V1</strong></summary>

### Path Table

| Method | Path | Description |
| --- | --- | --- |
| GET | [/api/v1/users/{user_id}](#getapiv1usersuser_id) | Получить пользователя по user_id |
| GET | [/api/v1/users/{user_id}/records](#getapiv1usersuser_idrecords) | Получить записи пользователя по user_id |
| POST | [/api/v1/users:register/](#postapiv1usersregister) | Зарегистрировать пользователя |
| POST | [/api/v1/users:login/](#postapiv1userslogin) | Авторизовать пользователя |
| GET | [/api/v1/users:current-user/](#getapiv1userscurrent-user) | Получить действующего пользователя |
| POST | [/api/v1/users:current-user/records](#postapiv1userscurrent-userrecords) | Добавить запись действующему пользователю |
| POST | [/api/v1/users:logout/](#postapiv1userslogout) | Деактивировать действующего пользователя |
| GET | [/api/v1/records/{quiz_id}](#getapiv1recordsquiz_id) | Получить записи квиза по quiz_id |

### Path Details
<details>
<summary><strong>Routes</strong></summary>

***

#### [GET]/api/v1/users/{user_id}

- Summary  
Получить пользователя по user_id

##### Responses

- 200 Successful Response

`application/json`

```ts
{
  data: {
    // Имя пользователя
    username: string
    // Электронная почта
    email: string
    id: integer
  }
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

#### [GET]/api/v1/users/{user_id}/records

- Summary  
Получить записи пользователя по user_id

##### Responses

- 200 Successful Response

`application/json`

```ts
{
  data: {
    id: integer
    // Id квиза
    quiz_id: integer
    // Название квиза
    quiz_name: Partial(string) & Partial(null)
    // Счёт в %
    score: integer
    // Дата создания
    created_at: string
  }[]
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

#### [POST]/api/v1/users:register/

- Summary  
Зарегистрировать пользователя

##### RequestBody

- application/json

```ts
{
  // Имя пользователя
  username: string
  // Электронная почта
  email: string
  // Пароль, от 5 до 50 знаков
  password: string
}
```

##### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

#### [POST]/api/v1/users:login/

- Summary  
Авторизовать пользователя

##### RequestBody

- application/json

```ts
{
  // Электронная почта
  email: string
  // Пароль, от 5 до 50 знаков
  password: string
}
```

##### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

#### [GET]/api/v1/users:current-user/

- Summary  
Получить действующего пользователя

##### Responses

- 200 Successful Response

`application/json`

```ts
{
  data: {
    // Имя пользователя
    username: string
    // Электронная почта
    email: string
    id: integer
  }
}
```

***

#### [POST]/api/v1/users:current-user/records

- Summary  
Добавить запись действующему пользователю

##### RequestBody

- application/json

```ts
{
  // Id квиза
  quiz_id: integer
  // Счёт в %
  score: integer
}
```

##### Responses

- 200 Successful Response

`application/json`

```ts
{
  data: {
    id: integer
    // Id квиза
    quiz_id: integer
    // Название квиза
    quiz_name: Partial(string) & Partial(null)
    // Счёт в %
    score: integer
    // Дата создания
    created_at: string
  }
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

#### [POST]/api/v1/users:logout/

- Summary  
Деактивировать действующего пользователя

##### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

***

#### [GET]/api/v1/records/{quiz_id}

- Summary  
Получить записи квиза по quiz_id

##### Responses

- 200 Successful Response

`application/json`

```ts
{
  data: {
    id: integer
    // Id квиза
    quiz_id: integer
    // Название квиза
    quiz_name: Partial(string) & Partial(null)
    // Счёт в %
    score: integer
    // Дата создания
    created_at: string
  }[]
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```
</details>
<details>
<summary><strong>Schemas</strong></summary>

### References

#### #/components/schemas/AppResponseList_RecordReturn_

```ts
{
  data: {
    id: integer
    // Id квиза
    quiz_id: integer
    // Название квиза
    quiz_name: Partial(string) & Partial(null)
    // Счёт в %
    score: integer
    // Дата создания
    created_at: string
  }[]
}
```

#### #/components/schemas/AppResponse_RecordReturn_

```ts
{
  data: {
    id: integer
    // Id квиза
    quiz_id: integer
    // Название квиза
    quiz_name: Partial(string) & Partial(null)
    // Счёт в %
    score: integer
    // Дата создания
    created_at: string
  }
}
```

#### #/components/schemas/AppResponse_UserReturn_

```ts
{
  data: {
    // Имя пользователя
    username: string
    // Электронная почта
    email: string
    id: integer
  }
}
```

#### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

#### #/components/schemas/RecordInput

```ts
{
  // Id квиза
  quiz_id: integer
  // Счёт в %
  score: integer
}
```

#### #/components/schemas/RecordReturn

```ts
{
  id: integer
  // Id квиза
  quiz_id: integer
  // Название квиза
  quiz_name: Partial(string) & Partial(null)
  // Счёт в %
  score: integer
  // Дата создания
  created_at: string
}
```

#### #/components/schemas/UserAuth

```ts
{
  // Электронная почта
  email: string
  // Пароль, от 5 до 50 знаков
  password: string
}
```

#### #/components/schemas/UserRegistration

```ts
{
  // Имя пользователя
  username: string
  // Электронная почта
  email: string
  // Пароль, от 5 до 50 знаков
  password: string
}
```

#### #/components/schemas/UserReturn

```ts
{
  // Имя пользователя
  username: string
  // Электронная почта
  email: string
  id: integer
}
```

#### #/components/schemas/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```
</details>
</details>

## Тестирование

```
pytest
```

## Контактная информация
- Telegram : @ma_nikitin