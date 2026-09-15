import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../core/config/api_config.dart';
import '../services/api_client.dart';
import '../../domain/entities/user.dart';

/// Репозиторий пользователя
class UserRepository {
  final ApiClient _apiClient;
  final FlutterSecureStorage _storage;
  
  static const String _accessTokenKey = 'access_token';
  
  UserRepository({ApiClient? apiClient, FlutterSecureStorage? storage})
      : _apiClient = apiClient ?? ApiClient(),
        _storage = storage ?? const FlutterSecureStorage();
  
  /// Получить информацию о текущем пользователе
  Future<User> getCurrentUser() async {
    final token = await _storage.read(key: _accessTokenKey);
    if (token == null || token.isEmpty) {
      throw Exception('Пользователь не авторизован');
    }
    
    final response = await _apiClient.get(ApiConfig.me, token);
    return User.fromJson(response);
  }
}
