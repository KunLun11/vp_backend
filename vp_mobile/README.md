# Volley Pro Mobile

Мобильное приложение для сервиса записи на волейбольные игры. Разработано на Flutter для кроссплатформенности (iOS + Android).

## Требования

- **Flutter SDK**: >= 3.19.0
- **Dart**: >= 3.3.0
- **Backend**: Запущенный бекенд Volley Pro (по умолчанию `http://localhost:8000`)

## Быстрый старт

### 1. Установка зависимостей

```bash
cd vp_mobile

# Установить все зависимости Flutter
flutter pub get
```

### 2. Настройка окружения

Приложение по умолчанию подключается к бекенду на `http://localhost:8000`.

**Для Android Emulator:**
- Используйте IP `10.0.2.2` вместо `localhost`
- Измените в `lib/core/config/api_config.dart`:
  ```dart
  static const String baseUrl = 'http://10.0.2.2:8000/api';
  ```

**Для iOS Simulator:**
- `localhost` работает корректно
- Оставьте как есть: `http://localhost:8000/api`

**Для физического устройства:**
- Используйте IP вашего компьютера в локальной сети
- Например: `http://192.168.1.100:8000/api`

### 3. Запуск приложения

```bash
# Запуск на подключенном устройстве или эмуляторе
flutter run

# Запуск на конкретном устройстве
flutter devices  # Показать список устройств
flutter run -d <device_id>

# Запуск в режиме отладки с подробными логами
flutter run --verbose
```

### 4. Сборка релизной версии

```bash
# Android APK
flutter build apk --release

# Android App Bundle (для Google Play)
flutter build appbundle --release

# iOS (только на macOS)
flutter build ios --release
```

## Структура проекта

```
vp_mobile/
├── lib/
│   ├── main.dart                    # Точка входа
│   ├── core/
│   │   ├── config/                  # Конфигурация (API URL, темы)
│   │   ├── theme/                   # Тема приложения
│   │   └── utils/                   # Утилиты
│   ├── data/
│   │   ├── models/                  # Модели данных
│   │   ├── repositories/            # Репозитории
│   │   └── services/                # API сервисы
│   ├── domain/
│   │   └── entities/                # Бизнес-сущности
│   └── presentation/
│       ├── screens/                 # Экраны приложения
│       ├── widgets/                 # Переиспользуемые виджеты
│       └── providers/               # State management (Provider)
├── assets/
│   ├── images/                      # Изображения
│   └── fonts/                       # Шрифты
├── android/                         # Android проект
├── ios/                             # iOS проект
└── pubspec.yaml                     # Зависимости и конфигурация
```

## Архитектура

Приложение следует архитектуре **Clean Architecture** с разделением на слои:

- **Presentation**: UI, виджеты, экраны, state management
- **Domain**: Бизнес-логика, сущности, use cases
- **Data**: Работа с API, модели, репозитории

State management реализован через **Provider**.

## Основные экраны

| Экран | Описание |
|-------|----------|
| Login | Вход по email и паролю |
| Register | Регистрация нового пользователя |
| Verify Email | Подтверждение email кодом |
| Home | Главный экран со списком игр |
| Profile | Профиль пользователя |

## API Endpoints

Приложение использует следующие endpoints бекенда:

### Authentication
- `POST /api/auth/login/` - Вход
- `POST /api/auth/refresh/` - Обновление токена
- `POST /api/auth/logout/` - Выход

### Registration
- `POST /api/register/user/` - Регистрация
- `POST /api/register/verify-email/` - Подтверждение email
- `POST /api/register/resend-code/` - Повторная отправка кода

### Users
- `GET /api/users/me/` - Информация о текущем пользователе

## Зависимости

Основные пакеты:
- `provider` - State management
- `http` - HTTP клиент
- `shared_preferences` - Локальное хранилище
- `flutter_secure_storage` - Безопасное хранение токенов
- `go_router` - Навигация и роутинг
- `google_fonts` - Кастомные шрифты
- `flutter_svg` - SVG изображения

## Разработка

### Генерация моделей

Модели создаются вручную в `lib/data/models/`. Каждая модель имеет методы:
- `fromJson(Map<String, dynamic>)` - десериализация
- `toJson()` - сериализация

### Добавление нового экрана

1. Создать файл в `lib/presentation/screens/`
2. Добавить роут в `lib/core/config/routes.dart`
3. При необходимости создать provider в `lib/presentation/providers/`

## Troubleshooting

### Ошибка подключения к API
- Проверьте, что бекенд запущен
- Для Android эмулятора используйте `10.0.2.2` вместо `localhost`
- Проверьте firewall настройки

### Ошибка сборки iOS
```bash
cd ios
pod install
cd ..
```

### Проблемы с зависимостями
```bash
flutter clean
flutter pub get
```

## Лицензия

Проект является частью платформы Volley Pro.
