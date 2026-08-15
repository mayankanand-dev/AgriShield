import 'package:flutter/material.dart';

class FarmDetailScreen extends StatelessWidget {
  const FarmDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('North Field'),
          bottom: const TabBar(
            isScrollable: true,
            labelColor: Colors.white,
            unselectedLabelColor: Colors.white70,
            tabs: [
              Tab(text: 'Overview'),
              Tab(text: 'Weather'),
              Tab(text: 'Soil'),
              Tab(text: 'Insurance'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            _buildOverviewTab(context, colorScheme),
            const Center(child: Text('Weather Details (Integration Pending)')),
            const Center(child: Text('Soil Data (Integration Pending)')),
            const Center(child: Text('Insurance Policy Details')),
          ],
        ),
      ),
    );
  }

  Widget _buildOverviewTab(BuildContext context, ColorScheme colorScheme) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Satellite placeholder
          Container(
            height: 200,
            decoration: BoxDecoration(
              color: Colors.grey.shade300,
              borderRadius: BorderRadius.circular(16.0),
              image: const DecorationImage(
                image: NetworkImage('https://via.placeholder.com/600x400.png?text=Satellite+View'),
                fit: BoxFit.cover,
              )
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Crop Health', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Icon(Icons.check_circle, color: colorScheme.primary),
                      const SizedBox(width: 8),
                      const Text('Healthy (92% Confidence)', style: TextStyle(fontWeight: FontWeight.bold)),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          const Text('Quick Actions', style: TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          ElevatedButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.camera_alt),
            label: const Text('Scan Crop Photo'),
          ),
          const SizedBox(height: 8),
          OutlinedButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.upload_file),
            label: const Text('Upload Soil Report'),
          ),
          const SizedBox(height: 8),
          TextButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.shield),
            label: const Text('Get Insurance Quote'),
          )
        ],
      ),
    );
  }
}
