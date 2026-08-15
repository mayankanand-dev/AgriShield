import 'dart:ui';
import 'package:flutter/material.dart';
import '../../theme.dart';

class SoilReportScreen extends StatelessWidget {
  const SoilReportScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(60),
        child: ClipRect(
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: AppBar(
              backgroundColor: AgriShieldTheme.surface.withOpacity(0.8),
              elevation: 0,
              iconTheme: const IconThemeData(color: AgriShieldTheme.onSurface),
              title: const Text('Farm Details', style: TextStyle(color: AgriShieldTheme.onSurface, fontWeight: FontWeight.w600, fontSize: 20)),
            ),
          ),
        ),
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Upload Section
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AgriShieldTheme.surfaceContainerLowest,
                borderRadius: BorderRadius.circular(20),
                boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8)],
              ),
              child: Column(
                children: [
                  Container(
                    width: 64, height: 64,
                    decoration: const BoxDecoration(color: AgriShieldTheme.primaryContainer, shape: BoxShape.circle),
                    child: const Icon(Icons.upload_file, color: AgriShieldTheme.onPrimaryContainer, size: 32),
                  ),
                  const SizedBox(height: 16),
                  const Text('Upload Soil Report', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                  const SizedBox(height: 8),
                  const Text(
                    'Take a photo or upload a PDF of your recent lab results for better recommendations.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: AgriShieldTheme.onSurfaceVariant),
                  ),
                  const SizedBox(height: 24),
                  Row(
                    children: [
                      Expanded(
                        child: OutlinedButton(
                          onPressed: () {},
                          style: OutlinedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          child: Column(
                            children: const [
                              Icon(Icons.camera_alt, color: AgriShieldTheme.primary, size: 28),
                              SizedBox(height: 8),
                              Text('Camera', style: TextStyle(color: AgriShieldTheme.onSurface)),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: OutlinedButton(
                          onPressed: () {},
                          style: OutlinedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          child: Column(
                            children: const [
                              Icon(Icons.picture_as_pdf, color: AgriShieldTheme.secondary, size: 28),
                              SizedBox(height: 8),
                              Text('File / PDF', style: TextStyle(color: AgriShieldTheme.onSurface)),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: const [
                    Text('Current Estimate', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                    SizedBox(width: 8),
                    Icon(Icons.verified, color: AgriShieldTheme.primary, size: 18),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                  decoration: BoxDecoration(color: AgriShieldTheme.surfaceVariant, borderRadius: BorderRadius.circular(16)),
                  child: Row(
                    children: const [
                      Icon(Icons.history, size: 14, color: AgriShieldTheme.onSurfaceVariant),
                      SizedBox(width: 4),
                      Text('2 months ago', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant)),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            // Results Dashboard
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AgriShieldTheme.surfaceContainerLowest,
                borderRadius: BorderRadius.circular(24),
                boxShadow: [BoxShadow(color: AgriShieldTheme.primaryContainer.withOpacity(0.1), blurRadius: 12)],
              ),
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(color: AgriShieldTheme.tertiaryFixed, borderRadius: BorderRadius.circular(12)),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Icon(Icons.policy, color: AgriShieldTheme.onTertiaryFixed),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: const [
                              Text('DATA SOURCE', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AgriShieldTheme.onTertiaryFixed)),
                              Text('Using regional Soil Health Card data (fallback estimate).', style: TextStyle(fontSize: 14, color: AgriShieldTheme.onTertiaryFixed)),
                            ],
                          ),
                        )
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  GridView.count(
                    crossAxisCount: 2,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    childAspectRatio: 0.85,
                    mainAxisSpacing: 16,
                    crossAxisSpacing: 16,
                    children: [
                      _buildGauge('Nitrogen (N)', '32', 'kg/ha', 'Low', AgriShieldTheme.error, 0.3),
                      _buildGauge('Phosphorus (P)', '18', 'kg/ha', 'Optimal', AgriShieldTheme.primary, 0.7),
                      _buildGauge('Potassium (K)', '145', 'kg/ha', 'Optimal', AgriShieldTheme.primary, 0.8),
                      _buildGauge('Soil pH', '7.8', 'Scale', 'Alkaline', AgriShieldTheme.secondaryContainer, 0.6),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            // Recommendation Card
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AgriShieldTheme.primaryContainer,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Column(
                children: [
                  Row(
                    children: [
                      Container(
                        width: 56, height: 56,
                        decoration: BoxDecoration(
                          color: AgriShieldTheme.surface,
                          shape: BoxShape.circle,
                          image: const DecorationImage(image: NetworkImage('https://picsum.photos/100'), fit: BoxFit.cover),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: const [
                            Text('RECOMMENDED CROP', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AgriShieldTheme.onPrimaryContainer, letterSpacing: 1)),
                            Text('Mustard', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AgriShieldTheme.onPrimaryContainer)),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  const Divider(color: Colors.white24),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: const Text('Tolerates slight alkalinity well. Requires N supplementation.', style: TextStyle(color: AgriShieldTheme.onPrimaryContainer)),
                      ),
                      Container(
                        width: 48, height: 48,
                        decoration: const BoxDecoration(color: AgriShieldTheme.onPrimaryContainer, shape: BoxShape.circle),
                        child: const Icon(Icons.arrow_forward, color: AgriShieldTheme.primaryContainer),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildGauge(String title, String value, String unit, String status, Color color, double progress) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
          width: 80, height: 80,
          child: Stack(
            fit: StackFit.expand,
            children: [
              CircularProgressIndicator(value: progress, strokeWidth: 8, color: color, backgroundColor: AgriShieldTheme.surfaceVariant),
              Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                    Text(unit, style: const TextStyle(fontSize: 10, color: AgriShieldTheme.onSurfaceVariant)),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        const SizedBox(height: 4),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
          decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
          child: Text(status, style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: color)),
        ),
      ],
    );
  }
}
