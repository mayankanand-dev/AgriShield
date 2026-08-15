import 'package:flutter/material.dart';

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),
              // Placeholder for Logo
              Icon(
                Icons.shield,
                size: 80,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(height: 24),
              Text(
                'Welcome to AgriShield',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: Theme.of(context).colorScheme.primary,
                    ),
              ),
              const SizedBox(height: 16),
              Text(
                'AI-powered crop insurance and farm monitoring',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyLarge,
              ),
              const Spacer(),
              const Text(
                'Select Language / भाषा चुनें',
                textAlign: TextAlign.center,
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () {
                  // Navigate to Login
                },
                child: const Text('English'),
              ),
              const SizedBox(height: 12),
              OutlinedButton(
                onPressed: () {
                  // Navigate to Login
                },
                style: OutlinedButton.styleFrom(
                  minimumSize: const Size(double.infinity, 56),
                  side: BorderSide(color: Theme.of(context).colorScheme.primary),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8.0),
                  ),
                ),
                child: const Text('हिंदी'),
              ),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }
}
