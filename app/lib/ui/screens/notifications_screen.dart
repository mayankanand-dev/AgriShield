import 'package:flutter/material.dart';

class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Alerts')),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          _buildAlertCard(
            context,
            icon: Icons.warning,
            title: 'High Pest Risk (Locust)',
            subtitle: 'AI detects 60% chance of locust swarm in your district within 48h.',
            color: Theme.of(context).colorScheme.error,
          ),
          _buildAlertCard(
            context,
            icon: Icons.water_drop,
            title: 'Irrigation Advisory',
            subtitle: 'Soil moisture is low (22%). Recommend irrigating North Field today.',
            color: Theme.of(context).colorScheme.secondary,
          ),
          _buildAlertCard(
            context,
            icon: Icons.shield,
            title: 'Policy Active',
            subtitle: 'Your PMFBY insurance policy for Wheat is now active.',
            color: Theme.of(context).colorScheme.primary,
          ),
        ],
      ),
    );
  }

  Widget _buildAlertCard(BuildContext context, {required IconData icon, required String title, required String subtitle, required Color color}) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12.0),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16.0),
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.1),
          child: Icon(icon, color: color),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Padding(
          padding: const EdgeInsets.top(8.0),
          child: Text(subtitle),
        ),
      ),
    );
  }
}
