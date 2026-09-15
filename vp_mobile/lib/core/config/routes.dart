import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../providers/auth_provider.dart';
import '../screens/login/login_screen.dart';
import '../screens/register/register_screen.dart';
import '../screens/home/home_screen.dart';

/// Конфигурация роутинга приложения
class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: '/login',
    routes: [
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        name: 'register',
        builder: (context, state) => const RegisterScreen(),
      ),
      GoRoute(
        path: '/home',
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),
    ],
    redirect: (context, state) {
      final authProvider = context.read<AuthProvider>();
      final isAuthenticated = authProvider.isAuthenticated;
      final isLoading = authProvider.isLoading;
      
      // Пока идет загрузка - не редиректим
      if (isLoading) return null;
      
      final isLoggingIn = state.matchedLocation == '/login';
      final isRegistering = state.matchedLocation == '/register';
      
      // Если авторизован и пытается зайти на экраны входа/регистрации
      if (isAuthenticated && (isLoggingIn || isRegistering)) {
        return '/home';
      }
      
      // Если не авторизован и пытается зайти на главный экран
      if (!isAuthenticated && !isLoggingIn && !isRegistering) {
        return '/login';
      }
      
      return null;
    },
  );
}
