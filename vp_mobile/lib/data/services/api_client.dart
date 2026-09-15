import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/config/api_config.dart';

/// HTTP клиент для работы с API
class ApiClient {
  final http.Client _client;
  
  ApiClient({http.Client? client}) : _client = client ?? http.Client();
  
  /// Получить заголовки с токеном
  Map<String, String> _getHeaders([String? token]) {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }
    return headers;
  }
  
  /// GET запрос
  Future<Map<String, dynamic>> get(String path, [String? token]) async {
    final response = await _client.get(
      Uri.parse('${ApiConfig.baseUrl}$path'),
      headers: _getHeaders(token),
    ).timeout(Duration(seconds: ApiConfig.timeoutSeconds));
    
    return _handleResponse(response);
  }
  
  /// POST запрос
  Future<Map<String, dynamic>> post(
    String path, 
    Map<String, dynamic> data, 
    [String? token]
  ) async {
    final response = await _client.post(
      Uri.parse('${ApiConfig.baseUrl}$path'),
      headers: _getHeaders(token),
      body: jsonEncode(data),
    ).timeout(Duration(seconds: ApiConfig.timeoutSeconds));
    
    return _handleResponse(response);
  }
  
  /// Обработка ответа
  Map<String, dynamic> _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return response.body.isNotEmpty 
          ? jsonDecode(response.body) as Map<String, dynamic>
          : {};
    }
    
    final errorMessage = response.body.isNotEmpty
        ? (jsonDecode(response.body) as Map<String, dynamic>)['detail'] ?? 'Ошибка сервера'
        : 'Ошибка сервера (${response.statusCode})';
    
    throw ApiException(errorMessage, response.statusCode);
  }
  
  /// Dispose
  void dispose() {
    _client.close();
  }
}

/// Исключение API
class ApiException implements Exception {
  final String message;
  final int statusCode;
  
  ApiException(this.message, this.statusCode);
  
  @override
  String toString() => 'ApiException: $message (status: $statusCode)';
}
