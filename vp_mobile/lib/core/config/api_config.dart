/// Конфигурация API
class ApiConfig {
  /// Базовый URL бекенда
  /// Для Android эмулятора используйте http://10.0.2.2:8000
  /// Для iOS Simulator используйте http://localhost:8000
  /// Для физического устройства используйте IP вашего компьютера
  static const String baseUrl = 'http://localhost:8000/api';
  
  /// Таймаут для HTTP запросов в секундах
  static const int timeoutSeconds = 30;
  
  /// Auth endpoints
  static const String login = '/auth/login/';
  static const String refresh = '/auth/refresh/';
  static const String logout = '/auth/logout/';
  
  /// Registration endpoints
  static const String register = '/register/user/';
  static const String verifyEmail = '/register/verify-email/';
  static const String resendCode = '/register/resend-code/';
  
  /// User endpoints
  static const String me = '/users/me/';
}
