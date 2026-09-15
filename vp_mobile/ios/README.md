# iOS configuration for Volley Pro Mobile

## Требования
- iOS 12.0+
- Xcode 15.0+
- CocoaPods

## Настройка

### 1. Установка зависимостей
```bash
cd ios
pod install
cd ..
```

### 2. Разрешения
Добавьте в `ios/Runner/Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
<key>NSPhotoLibraryUsageDescription</key>
<string>Приложению нужен доступ к фото для загрузки аватара</string>
<key>NSCameraUsageDescription</key>
<string>Приложению нужен доступ к камере для фото профиля</string>
```

### 3. Подпись кода
В Xcode:
1. Откройте `ios/Runner.xcworkspace`
2. Выберите проект Runner
3. Вкладка "Signing & Capabilities"
4. Выберите вашу команду разработки

## Сборка

```bash
# Debug
flutter build ios

# Release (App Store)
flutter build ios --release
```

## Запуск на симуляторе

1. Откройте `ios/Runner.xcworkspace` в Xcode
2. Выберите симулятор
3. Нажмите Run (⌘R)

Или через терминал:
```bash
flutter run
```

**Важно:** Для подключения к локальному бекенду используйте `localhost`:
```dart
static const String baseUrl = 'http://localhost:8000/api';
```

## Troubleshooting

### Ошибка CocoaPods
```bash
cd ios
pod deintegrate
pod install
cd ..
```

### Ошибка подписи
Убедитесь, что выбрана правильная команда разработки в Xcode.
