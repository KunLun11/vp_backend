# Android configuration for Volley Pro Mobile

## Требования
- Min SDK: 21 (Android 5.0)
- Target SDK: 34 (Android 14)
- Kotlin: 1.9.0+

## Настройка

### 1. Локальные свойства
Создайте файл `android/local.properties`:
```properties
sdk.dir=/path/to/your/Android/sdk
flutter.sdk=/path/to/your/flutter
```

### 2. Ключи для подписи
Для релизной сборки создайте `android/key.properties`:
```properties
storePassword=<password>
keyPassword=<password>
keyAlias=<alias>
storeFile=<path-to-keystore>
```

### 3. Разрешения
Приложение запрашивает следующие разрешения:
- INTERNET - доступ к сети
- ACCESS_NETWORK_STATE - состояние сети

## Сборка

```bash
# Debug APK
flutter build apk

# Release APK
flutter build apk --release

# App Bundle (для Google Play)
flutter build appbundle --release
```

## Запуск на эмуляторе

1. Создайте эмулятор в Android Studio
2. Запустите эмулятор
3. Выполните `flutter run`

**Важно:** Для подключения к локальному бекенду измените URL в `lib/core/config/api_config.dart`:
```dart
static const String baseUrl = 'http://10.0.2.2:8000/api';
```
