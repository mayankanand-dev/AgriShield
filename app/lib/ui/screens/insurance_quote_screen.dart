import 'package:flutter/material.dart';

class InsuranceQuoteScreen extends StatelessWidget {
  const InsuranceQuoteScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(title: const Text('Insurance Quote')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Estimated Premium',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 8),
            Text(
              '₹1,250',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.displayMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: colorScheme.primary,
                  ),
            ),
            const Text(
              'per hectare / season',
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    _buildRow('Base Rate', '₹1,000'),
                    const Divider(),
                    _buildRow('Weather Risk Adj.', '+ ₹250'),
                    const Divider(),
                    _buildRow('Subsidized Cost (Farmer Share)', '₹1,250', bold: true),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            const Card(
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Text('Coverage Details: Protects against Drought, Hailstorm, Unseasonal Rain, and specific Pest attacks up to ₹50,000 per hectare.'),
              ),
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: () {},
              child: const Text('Buy Policy'),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildRow(String label, String value, {bool bold = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: TextStyle(fontWeight: bold ? FontWeight.bold : FontWeight.normal)),
          Text(value, style: TextStyle(fontWeight: bold ? FontWeight.bold : FontWeight.normal)),
        ],
      ),
    );
  }
}
