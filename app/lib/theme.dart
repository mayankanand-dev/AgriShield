import 'package:flutter/material.dart';

class AgriShieldTheme {
  static const Color primary = Color(0xFF1B7A3D);
  static const Color secondary = Color(0xFFF5821F);
  static const Color background = Color(0xFFF9F9F7);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color error = Color(0xFFBA1A1A);
  static const Color onPrimary = Color(0xFFFFFFFF);
  static const Color onSurface = Color(0xFF1A1C1B);
  
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: const ColorScheme.light(
        primary: primary,
        secondary: secondary,
        background: background,
        surface: surface,
        error: error,
        onPrimary: onPrimary,
        onSurface: onSurface,
      ),
      scaffoldBackgroundColor: background,
      fontFamily: 'Inter',
      appBarTheme: const AppBarTheme(
        backgroundColor: primary,
        foregroundColor: onPrimary,
        elevation: 0,
        centerTitle: true,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: onPrimary,
          minimumSize: const Size(double.infinity, 56), // Large tap target
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8.0),
          ),
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      cardTheme: CardTheme(
        color: surface,
        elevation: 2,
        shadowColor: primary.withOpacity(0.08),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16.0),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surface,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: const BorderSide(color: Color(0xFFBECABC)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: const BorderSide(color: primary, width: 2.0),
        ),
      ),
    );
  }
}
