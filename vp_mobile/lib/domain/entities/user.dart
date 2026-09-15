import 'package:equatable/equatable.dart';

/// Сущность пользователя
class User extends Equatable {
  final String id;
  final String email;
  final String phone;
  final String role;
  
  const User({
    required this.id,
    required this.email,
    required this.phone,
    required this.role,
  });
  
  /// Создать из JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] ?? '',
      email: json['email'] ?? '',
      phone: json['phone'] ?? '',
      role: json['role'] ?? 'player',
    );
  }
  
  /// Преобразовать в JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'phone': phone,
      'role': role,
    };
  }
  
  @override
  List<Object?> get props => [id, email, phone, role];
  
  /// Пустой пользователь
  static const empty = User(
    id: '',
    email: '',
    phone: '',
    role: 'player',
  );
  
  /// Проверка на пустоту
  bool get isEmpty => id.isEmpty;
  
  /// Проверка на заполненность
  bool get isNotEmpty => id.isNotEmpty;
}
