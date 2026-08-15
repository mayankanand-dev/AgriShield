import 'dart:ui';
import 'package:flutter/material.dart';
import '../../theme.dart';
import 'crop_photo_scan_screen.dart';
import 'soil_report_screen.dart';
import 'insurance_quote_screen.dart';

class FarmDetailScreen extends StatefulWidget {
  final Map<String, dynamic> farm;
  
  const FarmDetailScreen({super.key, required this.farm});

  @override
  State<FarmDetailScreen> createState() => _FarmDetailScreenState();
}

class _FarmDetailScreenState extends State<FarmDetailScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: NestedScrollView(
        headerSliverBuilder: (context, innerBoxIsScrolled) {
          return [
            SliverAppBar(
              expandedHeight: 200.0,
              pinned: true,
              backgroundColor: AgriShieldTheme.surface,
              iconTheme: const IconThemeData(color: AgriShieldTheme.onSurface),
              flexibleSpace: FlexibleSpaceBar(
                titlePadding: const EdgeInsets.only(left: 16, bottom: 62),
                title: Text(widget.farm['name'] ?? 'Farm Details', style: const TextStyle(color: AgriShieldTheme.onSurface, fontWeight: FontWeight.bold)),
                background: Stack(
                  fit: StackFit.expand,
                  children: [
                    Container(color: AgriShieldTheme.surfaceVariant),
                    const Center(child: Icon(Icons.landscape, size: 64, color: Colors.grey)),
                    DecoratedBox(
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [Colors.transparent, AgriShieldTheme.surface.withOpacity(0.8)],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              bottom: TabBar(
                controller: _tabController,
                isScrollable: true,
                labelColor: AgriShieldTheme.primary,
                unselectedLabelColor: AgriShieldTheme.onSurfaceVariant,
                indicatorColor: AgriShieldTheme.primary,
                tabs: const [
                  Tab(text: 'Overview'),
                  Tab(text: 'Weather'),
                  Tab(text: 'Soil'),
                  Tab(text: 'Insurance'),
                ],
              ),
            ),
          ];
        },
        body: TabBarView(
          controller: _tabController,
          children: [
            _buildOverviewTab(),
            const Center(child: Text('Weather Details Pending')),
            const Center(child: Text('Soil History Pending')),
            const Center(child: Text('Insurance Policies Pending')),
          ],
        ),
      ),
    );
  }

  Widget _buildOverviewTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Crop Health Card
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: AgriShieldTheme.surfaceContainerLowest,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AgriShieldTheme.surfaceVariant),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8)],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Crop Health Status', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(color: AgriShieldTheme.tertiaryFixed, borderRadius: BorderRadius.circular(12)),
                    child: const Text('Healthy', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onTertiaryFixed, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Crop', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant)),
                        Text(widget.farm['crop'] ?? 'Unknown', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                      ],
                    ),
                  ),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('AI Confidence', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant)),
                        const Text('92%', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: AgriShieldTheme.primary)),
                      ],
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        const Text('Quick Actions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        _buildActionCard(
          icon: Icons.camera_alt,
          title: 'Scan Crop Photo',
          subtitle: 'Check for disease using AI',
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const CropPhotoScanScreen())),
        ),
        const SizedBox(height: 12),
        _buildActionCard(
          icon: Icons.upload_file,
          title: 'Upload Soil Report',
          subtitle: 'Update NPK values',
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SoilReportScreen())),
        ),
        const SizedBox(height: 12),
        _buildActionCard(
          icon: Icons.shield,
          title: 'Get Insurance Quote',
          subtitle: 'Protect this farm',
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => InsuranceQuoteScreen(
            farmId: widget.farm['id'] ?? '123',
            crop: widget.farm['crop'] ?? 'Wheat',
            areaM2: 20000,
          ))),
        ),
      ],
    );
  }

  Widget _buildActionCard({required IconData icon, required String title, required String subtitle, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AgriShieldTheme.surfaceContainerLowest,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: AgriShieldTheme.surfaceVariant),
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: AgriShieldTheme.primary.withOpacity(0.1), shape: BoxShape.circle),
              child: Icon(icon, color: AgriShieldTheme.primary),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16)),
                  Text(subtitle, style: const TextStyle(color: AgriShieldTheme.onSurfaceVariant, fontSize: 12)),
                ],
              ),
            ),
            const Icon(Icons.chevron_right, color: AgriShieldTheme.onSurfaceVariant),
          ],
        ),
      ),
    );
  }
}
