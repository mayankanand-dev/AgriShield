import 'package:flutter/material.dart';

class ClaimTimelineScreen extends StatelessWidget {
  const ClaimTimelineScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(title: const Text('Claim Status')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: colorScheme.surface,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: colorScheme.primary.withOpacity(0.3)),
              ),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.verified, color: colorScheme.primary),
                      const SizedBox(width: 8),
                      Text('Verified on blockchain', style: TextStyle(color: colorScheme.primary, fontWeight: FontWeight.bold)),
                    ],
                  ),
                  const SizedBox(height: 8),
                  const Text('0x8a92...b4f1', style: TextStyle(fontFamily: 'Courier', fontSize: 12)),
                ],
              ),
            ),
            const SizedBox(height: 32),
            _buildTimelineStep(context, 'Submitted', 'Oct 12, 2026', isCompleted: true),
            _buildTimelineStep(context, 'AI Assessed', 'Oct 13, 2026 (Damage: 45%)', isCompleted: true),
            _buildTimelineStep(context, 'Under Review', 'Currently with claims officer', isCompleted: false, isCurrent: true),
            _buildTimelineStep(context, 'Approved', 'Pending', isCompleted: false, isLast: true),
          ],
        ),
      ),
    );
  }

  Widget _buildTimelineStep(BuildContext context, String title, String subtitle, {bool isCompleted = false, bool isCurrent = false, bool isLast = false}) {
    final colorScheme = Theme.of(context).colorScheme;
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Column(
          children: [
            Container(
              width: 24,
              height: 24,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isCompleted ? colorScheme.primary : (isCurrent ? colorScheme.secondary : Colors.grey.shade300),
              ),
              child: isCompleted ? const Icon(Icons.check, size: 16, color: Colors.white) : null,
            ),
            if (!isLast)
              Container(
                width: 2,
                height: 50,
                color: isCompleted ? colorScheme.primary : Colors.grey.shade300,
              )
          ],
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              const SizedBox(height: 4),
              Text(subtitle, style: TextStyle(color: Colors.grey.shade700)),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ],
    );
  }
}
