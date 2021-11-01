# Проект с настроенной инфраструктурой для ШРИ

- В качестве приложения используется стартовая страница React
- В качестве CI используется Github Actions
- Для секретов используется встроенная в Github секретница
- Артефакты (докер образ) пушатся в Github Container Registry и доступно на странице репозитория на вкладке Packages
- Для работы с трекером используется |･ω･) Python

- Чтобы закоммитить через conventional commits нужно установить commitizen ('npm i -g commitizen'), 'git add .' и запустить 'git cz'
- Папочка archive - это мои тщетные попытки баш скриптом общаться с трекером с коммитами на русском языке ~(>\_<~)

## Запускаем приложение

`docker run --rm -it -p 8080:80 ghcr.io/iskhakov-public/todoapp:v0.0.6`

Переходим в "localhost:8080", а там привет)
Внутри работает нджинкс и раздает статику

Всем приятного просмотра!!
°˖✧◝(⁰▿⁰)◜✧˖°
