import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class SoilReportScreen extends StatefulWidget {
  const SoilReportScreen({super.key});

  @override
  State<SoilReportScreen> createState() => _SoilReportScreenState();
}

class _SoilReportScreenState extends State<SoilReportScreen> {
  bool _hasReport = false;
  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      setState(() => _hasReport = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Soil Health')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (!_hasReport)
              Container(
                padding: const EdgeInsets.all(16.0),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.secondaryContainer,
                  borderRadius: BorderRadius.circular(8.0),
                ),
                child: const Text(
                  'No soil report uploaded. Using regional Soil Health Card fallback data.',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
              ),
            const SizedBox(height: 24),
            OutlinedButton.icon(
              onPressed: _pickImage,
              icon: const Icon(Icons.upload_file),
              label: const Text('Upload Soil Report (Image/PDF)'),
            ),
            const SizedBox(height: 24),
            const Text('Soil Parameters', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildGauge('N', '120 kg/ha'),
                _buildGauge('P', '45 kg/ha'),
                _buildGauge('K', '210 kg/ha'),
                _buildGauge('pH', '6.5'),
              ],
            ),
            const SizedBox(height: 32),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('AI Recommendation', style: TextStyle(fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Text('Based on this soil profile, we recommend planting Wheat or Mustard this Rabi season.')
                  ],
                ),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildGauge(String label, String value) {
    return Column(
      children: [
        Container(
          width: 60,
          height: 60,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: Colors.green, width: 4),
          ),
          child: Center(child: Text(label, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18))),
        ),
        const SizedBox(height: 8),
        Text(value, style: const TextStyle(fontSize: 12)),
      ],
    );
  }
}
