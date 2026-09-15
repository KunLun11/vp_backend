import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../core/config/api_config.dart';
import '../services/api_client.dart';

/// Сервис аутентификации
class AuthService {
  final ApiClient _apiClient;
  final FlutterSecureStorage _storage;
  
  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';
  
  AuthService({ApiClient? apiClient, FlutterSecureStorage? storage})
      : _apiClient = apiClient ?? ApiClient(),
        _storage = storage ?? const FlutterSecureStorage();
  
  /// Вход по email и паролю
  Future<Map<String, String>> login(String email, String password) async {
    final response = await _apiClient.post(
      ApiConfig.login,
      {'email': email, 'password': password},
    );
    
    final accessToken = response['access'] as String;
    final refreshToken = response['refresh'] as String;
    
    await _saveTokens(accessToken, refreshToken);
    
    return {'access': accessToken, 'refresh': refreshToken};
  }
  
  /// Регистрация пользователя
  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    required String phone,
    required String role,
  }) async {
    return await _apiClient.post(
      ApiConfig.register,
      {
        'email': email,
        'password': password,
        'phone': phone,
        'role': role,
      },
    );
  }
  
  /// Подтверждение email
  Future<Map<String, dynamic>> verifyEmail(String email, String code) async {
    return await _apiClient.post(
      ApiConfig.verifyEmail,
      {'email': email, 'code': code},
    );
  }
  
  /// Повторная отправка кода подтверждения
  Future<Map<String, dynamic>> resendCode(String email) async {
    return await _apiClient.post(
      ApiConfig.resendCode,
      {'email': email},
    );
  }
  
  /// Обновление токенов
  Future<Map<String, String>> refreshToken(String refreshToken) async {
    final response = await _apiClient.post(
      ApiConfig.refresh,
      {'refresh_token': refreshToken},
    );
    
    final newAccessToken = response['access'] as String;
    final newRefreshToken = response['refresh'] as String;
    
    await _saveTokens(newAccessToken, newRefreshToken);
    
    return {'access': newAccessToken, 'refresh': newRefreshToken};
  }
  
  /// Выход
  Future<void> logout() async {
    final accessToken = await _storage.read(key: _accessTokenKey);
    if (accessToken != null) {
      try {
        await _apiClient.post(ApiConfig.logout, {}, accessToken);
      } catch (_) {
        // Игнорируем ошибки при выходе
      }
    }
    await _clearTokens();
  }
  
  /// Получить текущий токен
  Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }
  
  /// Проверка авторизации
  Future<bool> isAuthenticated() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }
  
  /// Сохранить токены
  Future<void> _saveTokens(String access, String refresh) async {
    await _storage.write(key: _accessTokenKey, value: access);
    await _storage.write(key: _refreshTokenKey, value: refresh);
  }
  
  /// Очистить токены
  Future<void> _clearTokens() async {
    await _storage.delete(key: _accessTokenKey);
    await _storage.delete(key: _refreshTokenKey);
  }
}
