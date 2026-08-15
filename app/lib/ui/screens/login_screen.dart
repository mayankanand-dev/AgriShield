import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _emailController = TextEditingController();
  final _otpController = TextEditingController();
  bool _otpSent = false;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 48),
              Icon(Icons.shield, size: 64, color: colorScheme.primary),
              const SizedBox(height: 24),
              Text(
                'Sign In',
                style: textTheme.headlineMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: colorScheme.primary,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text(
                'Enter your email to receive a secure OTP',
                style: textTheme.bodyLarge,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 48),
              TextField(
                controller: _emailController,
                keyboardType: TextInputType.emailAddress,
                decoration: const InputDecoration(
                  labelText: 'Email Address',
                  prefixIcon: Icon(Icons.email),
                ),
                enabled: !_otpSent,
              ),
              if (_otpSent) ...[
                const SizedBox(height: 24),
                TextField(
                  controller: _otpController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    labelText: 'Enter OTP',
                    prefixIcon: Icon(Icons.password),
                  ),
                ),
              ],
              const SizedBox(height: 32),
              ElevatedButton(
                onPressed: () {
                  if (!_otpSent) {
                    setState(() => _otpSent = true);
                  } else {
                    // Navigate to Dashboard
                  }
                },
                child: Text(_otpSent ? 'Verify & Login' : 'Send OTP'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
