import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final farmsAsync = ref.watch(farmsProvider);
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('AgriShield'),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications),
            onPressed: () {},
          )
        ],
      ),
      body: farmsAsync.when(
        data: (farms) {
          if (farms.isEmpty) {
            return const Center(child: Text('No farms added yet.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16.0),
            itemCount: farms.length,
            itemBuilder: (context, index) {
              final farm = farms[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 16.0),
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            farm['name'] ?? 'Unknown',
                            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                  fontWeight: FontWeight.bold,
                                ),
                          ),
                          _buildStatusBadge(farm['status'] ?? 'PENDING', colorScheme),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text('Crop: ${farm['crop'] ?? 'Not set'}'),
                      const SizedBox(height: 16),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            children: [
                              Icon(Icons.thermostat, color: colorScheme.secondary, size: 20),
                              const SizedBox(width: 4),
                              const Text('28°C'),
                            ],
                          ),
                          TextButton(
                            onPressed: () {},
                            child: const Text('View Details'),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        icon: const Icon(Icons.add),
        label: const Text('Add Farm'),
        backgroundColor: colorScheme.primary,
        foregroundColor: colorScheme.onPrimary,
      ),
      bottomNavigationBar: BottomNavigationBar(
        selectedItemColor: colorScheme.primary,
        unselectedItemColor: Colors.grey,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.map), label: 'Farms'),
          BottomNavigationBarItem(icon: Icon(Icons.shield), label: 'Insurance'),
          BottomNavigationBarItem(icon: Icon(Icons.warning), label: 'Alerts'),
        ],
      ),
    );
  }

  Widget _buildStatusBadge(String status, ColorScheme colorScheme) {
    Color bg = Colors.grey.shade200;
    Color fg = Colors.grey.shade800;
    if (status == 'VERIFIED') {
      bg = colorScheme.primary.withOpacity(0.1);
      fg = colorScheme.primary;
    } else if (status == 'PENDING') {
      bg = colorScheme.secondary.withOpacity(0.1);
      fg = colorScheme.secondary;
    }
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        status,
        style: TextStyle(color: fg, fontWeight: FontWeight.bold, fontSize: 12),
      ),
    );
  }
}
