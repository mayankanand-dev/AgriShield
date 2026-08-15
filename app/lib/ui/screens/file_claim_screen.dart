import 'package:flutter/material.dart';

class FileClaimScreen extends StatefulWidget {
  const FileClaimScreen({super.key});

  @override
  State<FileClaimScreen> createState() => _FileClaimScreenState();
}

class _FileClaimScreenState extends State<FileClaimScreen> {
  String? _selectedEvent;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('File a Claim')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('What happened?', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8.0,
              children: [
                _buildChoiceChip('Hailstorm', Icons.ac_unit),
                _buildChoiceChip('Drought', Icons.wb_sunny),
                _buildChoiceChip('Flood', Icons.water),
                _buildChoiceChip('Pest', Icons.bug_report),
              ],
            ),
            const SizedBox(height: 24),
            const Text('When did it happen?', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            OutlinedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.calendar_today),
              label: const Text('Select Date'),
            ),
            const SizedBox(height: 24),
            const Text('Evidence Photos', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Container(
              height: 120,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey, style: BorderStyle.solid),
                borderRadius: BorderRadius.circular(8.0),
              ),
              child: const Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.add_a_photo, size: 32, color: Colors.grey),
                    SizedBox(height: 8),
                    Text('Tap to upload photos')
                  ],
                ),
              ),
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: _selectedEvent != null ? () {} : null,
              child: const Text('Submit Claim'),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildChoiceChip(String label, IconData icon) {
    final selected = _selectedEvent == label;
    final colorScheme = Theme.of(context).colorScheme;
    return ChoiceChip(
      label: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: selected ? colorScheme.onPrimary : colorScheme.onSurface),
          const SizedBox(width: 4),
          Text(label),
        ],
      ),
      selected: selected,
      onSelected: (val) {
        setState(() => _selectedEvent = val ? label : null);
      },
      selectedColor: colorScheme.primary,
      labelStyle: TextStyle(color: selected ? colorScheme.onPrimary : colorScheme.onSurface),
    );
  }
}
