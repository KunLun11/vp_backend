import 'package:flutter/material.dart';

/// Расширения для удобной работы с контекстом
extension BuildContextExtensions on BuildContext {
  /// Получить тему
  ThemeData get theme => Theme.of(this);
  
  /// Получить цветовую схему
  ColorScheme get colorScheme => Theme.of(this).colorScheme;
  
  /// Показать Snackbar
  void showSnackBar(String message, {bool isError = false}) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : Colors.green,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
      ),
    );
  }
  
  /// Показать диалог загрузки
  void showLoading({String message = 'Загрузка...'}) {
    showDialog(
      context: this,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const CircularProgressIndicator(),
            const SizedBox(height: 16),
            Text(message),
          ],
        ),
      ),
    );
  }
  
  /// Скрыть диалог
  void hideDialog() {
    Navigator.of(this).pop();
  }
}
