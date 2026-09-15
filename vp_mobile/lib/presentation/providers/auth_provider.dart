import 'package:flutter/material.dart';
import '../../domain/entities/user.dart';
import '../../data/repositories/auth_repository.dart';
import '../../data/repositories/user_repository.dart';

/// Провайдер для управления состоянием аутентификации
class AuthProvider with ChangeNotifier {
  final AuthService _authService;
  final UserRepository _userRepository;
  
  User? _user;
  bool _isLoading = false;
  String? _error;
  
  AuthProvider({
    AuthService? authService,
    UserRepository? userRepository,
  })  : _authService = authService ?? AuthService(),
        _userRepository = userRepository ?? UserRepository();
  
  /// Текущий пользователь
  User? get user => _user;
  
  /// Статус загрузки
  bool get isLoading => _isLoading;
  
  /// Ошибка
  String? get error => _error;
  
  /// Авторизован ли пользователь
  bool get isAuthenticated => _user != null;
  
  /// Инициализация (проверка токена при старте)
  Future<void> init() async {
    _isLoading = true;
    notifyListeners();
    
    try {
      if (await _authService.isAuthenticated()) {
        _user = await _userRepository.getCurrentUser();
      }
    } catch (e) {
      _error = e.toString();
      await logout();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
  
  /// Вход
  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      await _authService.login(email, password);
      _user = await _userRepository.getCurrentUser();
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }
  
  /// Регистрация
  Future<bool> register({
    required String email,
    required String password,
    required String phone,
    required String role,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      await _authService.register(
        email: email,
        password: password,
        phone: phone,
        role: role,
      );
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }
  
  /// Подтверждение email
  Future<bool> verifyEmail(String email, String code) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      await _authService.verifyEmail(email, code);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }
  
  /// Повторная отправка кода
  Future<bool> resendCode(String email) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      await _authService.resendCode(email);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }
  
  /// Выход
  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();
    
    try {
      await _authService.logout();
    } catch (_) {
      // Игнорируем ошибки
    }
    
    _user = null;
    _error = null;
    _isLoading = false;
    notifyListeners();
  }
  
  /// Очистить ошибку
  void clearError() {
    _error = null;
    notifyListeners();
  }
}
