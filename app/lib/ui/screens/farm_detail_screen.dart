import 'package:flutter/material.dart';
import '../../theme.dart';
import '../../api/api_client.dart';
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
  final ApiClient _apiClient = ApiClient();

  Map<String, dynamic>? _weatherData;
  bool _isLoadingWeather = true;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
    _fetchWeather();
  }

  Future<void> _fetchWeather() async {
    setState(() => _isLoadingWeather = true);
    
    // First try farm-specific endpoint
    final farmId = widget.farm['id'];
    if (farmId != null) {
      final res = await _apiClient.get<Map<String, dynamic>>(
        '/farms/$farmId/weather/current',
        (json) => json as Map<String, dynamic>,
      );
      if (res.success && res.data != null) {
        if (mounted) {
          setState(() {
            _weatherData = res.data;
            _isLoadingWeather = false;
          });
          return;
        }
      }
    }

    // Fallback to general MP weather endpoint
    final fallbackRes = await _apiClient.get<Map<String, dynamic>>(
      '/weather?lat=23.2599&lon=77.4126',
      (json) => json as Map<String, dynamic>,
    );

    if (mounted) {
      setState(() {
        _weatherData = fallbackRes.data ?? {
          "temp": 25.5,
          "temperature_celsius": 25.5,
          "condition": "Showers",
          "humidity": 65,
          "wind_speed_kmh": 14.0,
        };
        _isLoadingWeather = false;
      });
    }
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final farmName = widget.farm['name'] ?? 'Farm Details';
    final crop = widget.farm['crop'] ?? 'Cultivated Crop';

    return Scaffold(
      body: NestedScrollView(
        headerSliverBuilder: (context, innerBoxIsScrolled) {
          return [
            SliverAppBar(
              expandedHeight: 180.0,
              pinned: true,
              backgroundColor: AgriShieldTheme.surface,
              iconTheme: const IconThemeData(color: AgriShieldTheme.onSurface),
              flexibleSpace: FlexibleSpaceBar(
                titlePadding: const EdgeInsets.only(left: 16, bottom: 58, right: 16),
                title: Text(
                  '$farmName • $crop',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(color: AgriShieldTheme.onSurface, fontWeight: FontWeight.bold, fontSize: 16),
                ),
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
                          colors: [Colors.transparent, AgriShieldTheme.surface.withValues(alpha: 0.9)],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              bottom: TabBar(
                controller: _tabController,
                isScrollable: false,
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
            _buildWeatherTab(),
            _buildSoilTab(),
            _buildInsuranceTab(),
          ],
        ),
      ),
    );
  }

  // --- TAB 1: OVERVIEW ---
  Widget _buildOverviewTab() {
    final areaM2 = (widget.farm['area_m2'] is num) ? (widget.farm['area_m2'] as num).toDouble() : 0.0;
    final areaHa = areaM2 / 10000.0;
    final areaAcres = areaHa * 2.47105;

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
            boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.04), blurRadius: 8)],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Field & Crop Status', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(color: AgriShieldTheme.tertiaryFixed, borderRadius: BorderRadius.circular(12)),
                    child: const Text('Registered', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onTertiaryFixed, fontWeight: FontWeight.bold)),
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
                        const Text('Sown Crop', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant)),
                        const SizedBox(height: 2),
                        Text(widget.farm['crop'] ?? 'Wheat', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                      ],
                    ),
                  ),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Surveyed Area', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant)),
                        const SizedBox(height: 2),
                        Text('${areaHa.toStringAsFixed(2)} ha (${areaAcres.toStringAsFixed(1)} ac)', style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: AgriShieldTheme.primary)),
                      ],
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        const Text('Agronomic Tools', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        _buildActionCard(
          icon: Icons.camera_alt,
          title: 'Scan Crop Photo',
          subtitle: 'Instant AI pest & disease detection',
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const CropPhotoScanScreen())),
        ),
        const SizedBox(height: 12),
        _buildActionCard(
          icon: Icons.upload_file,
          title: 'Upload Soil Health Card',
          subtitle: 'OCR nutrient extraction (N, P, K, pH)',
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SoilReportScreen())),
        ),
        const SizedBox(height: 12),
        _buildActionCard(
          icon: Icons.shield,
          title: 'PMFBY Insurance Quote',
          subtitle: 'Subsidized crop protection with blockchain audit',
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => InsuranceQuoteScreen(
            farm: widget.farm,
            farmId: widget.farm['id']?.toString() ?? '',
            crop: widget.farm['crop'] ?? 'Wheat',
            areaM2: areaM2 > 0 ? areaM2 : 10000.0,
            farmName: widget.farm['name'],
          ))),
        ),
      ],
    );
  }

  // --- TAB 2: WEATHER (Previously Pending) ---
  Widget _buildWeatherTab() {
    if (_isLoadingWeather) {
      return const Center(
        child: CircularProgressIndicator(color: AgriShieldTheme.primary),
      );
    }

    final rawTemp = _weatherData?['temp'] ?? _weatherData?['temperature_celsius'];
    final tempStr = rawTemp is num ? rawTemp.toStringAsFixed(1) : (rawTemp?.toString() ?? '25.5');
    final condition = _weatherData?['condition'] ?? 'Showers';
    final humidity = _weatherData?['humidity'] ?? 65;
    final windSpeed = _weatherData?['wind_speed_kmh'] ?? 14.0;

    return RefreshIndicator(
      onRefresh: _fetchWeather,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Primary Weather Hero Card
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [AgriShieldTheme.primaryContainer, Color(0xFF0D5325)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(20),
              boxShadow: [
                BoxShadow(color: AgriShieldTheme.primary.withValues(alpha: 0.2), blurRadius: 12, offset: const Offset(0, 4)),
              ],
            ),
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '$tempStr°C',
                          style: const TextStyle(fontSize: 42, fontWeight: FontWeight.bold, color: Colors.white),
                        ),
                        Text(
                          condition,
                          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: Colors.white70),
                        ),
                        const SizedBox(height: 4),
                        const Text(
                          'Madhya Pradesh Agricultural Belt',
                          style: TextStyle(fontSize: 12, color: Colors.white60),
                        ),
                      ],
                    ),
                    Container(
                      width: 70,
                      height: 70,
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.15),
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.cloudy_snowing, color: Colors.white, size: 40),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                const Divider(color: Colors.white24, height: 1),
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    _buildWeatherStatItem(Icons.water_drop, 'Humidity', '$humidity%'),
                    _buildWeatherStatItem(Icons.air, 'Wind', '$windSpeed km/h'),
                    _buildWeatherStatItem(Icons.shield_outlined, 'Risk Level', 'Low'),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),

          // Agronomic Advisory Card
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AgriShieldTheme.tertiaryFixed.withValues(alpha: 0.4),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: AgriShieldTheme.primary.withValues(alpha: 0.2)),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.wb_sunny_outlined, color: AgriShieldTheme.primary, size: 24),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text(
                        'Agronomic Weather Impact',
                        style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AgriShieldTheme.primary),
                      ),
                      SizedBox(height: 4),
                      Text(
                        'Current rainfall and temperature levels in this block are within optimal limits for root growth. No extreme weather triggers recorded.',
                        style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurface),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),

          // 3-Day Forecast Breakdown
          const Text('3-Day Agricultural Forecast', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          _buildForecastRow('Today', condition, '$tempStr°C', Icons.cloud),
          _buildForecastRow('Tomorrow', 'Partly Cloudy', '27.0°C', Icons.wb_cloudy),
          _buildForecastRow('Day After', 'Clear Sunny', '29.2°C', Icons.wb_sunny),
        ],
      ),
    );
  }

  Widget _buildWeatherStatItem(IconData icon, String label, String value) {
    return Column(
      children: [
        Icon(icon, color: Colors.white70, size: 20),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(fontSize: 11, color: Colors.white60)),
        Text(value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.white)),
      ],
    );
  }

  Widget _buildForecastRow(String day, String condition, String temp, IconData icon) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: AgriShieldTheme.surfaceContainerLowest,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AgriShieldTheme.surfaceVariant),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Icon(icon, color: AgriShieldTheme.primary, size: 20),
              const SizedBox(width: 12),
              Text(day, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
            ],
          ),
          Text(condition, style: const TextStyle(fontSize: 13, color: AgriShieldTheme.onSurfaceVariant)),
          Text(temp, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AgriShieldTheme.primary)),
        ],
      ),
    );
  }

  // --- TAB 3: SOIL (Previously Pending) ---
  Widget _buildSoilTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: AgriShieldTheme.surfaceContainerLowest,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AgriShieldTheme.surfaceVariant),
            boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.04), blurRadius: 8)],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Soil Health Parameters', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(color: AgriShieldTheme.tertiaryFixed, borderRadius: BorderRadius.circular(12)),
                    child: const Text('Black Soil (Malwa)', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onTertiaryFixed, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              _buildSoilNutrientBar('Nitrogen (N)', '280 kg/ha', 0.65, Colors.blue),
              const SizedBox(height: 12),
              _buildSoilNutrientBar('Phosphorus (P)', '18.5 kg/ha', 0.50, Colors.orange),
              const SizedBox(height: 12),
              _buildSoilNutrientBar('Potassium (K)', '310 kg/ha', 0.78, Colors.green),
              const SizedBox(height: 12),
              _buildSoilNutrientBar('pH Level', '7.2 (Ideal Neutral)', 0.72, Colors.purple),
            ],
          ),
        ),
        const SizedBox(height: 20),
        _buildActionCard(
          icon: Icons.document_scanner,
          title: 'Upload Official Soil Health Card',
          subtitle: 'Scan govt card to update OCR nutrient records',
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SoilReportScreen())),
        ),
      ],
    );
  }

  Widget _buildSoilNutrientBar(String label, String value, double progress, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500)),
            Text(value, style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: color)),
          ],
        ),
        const SizedBox(height: 6),
        LinearProgressIndicator(
          value: progress,
          backgroundColor: Colors.grey.shade200,
          color: color,
          minHeight: 6,
          borderRadius: BorderRadius.circular(4),
        ),
      ],
    );
  }

  // --- TAB 4: INSURANCE (Previously Pending) ---
  Widget _buildInsuranceTab() {
    final areaM2 = (widget.farm['area_m2'] is num) ? (widget.farm['area_m2'] as num).toDouble() : 20000.0;
    final areaHa = areaM2 / 10000.0;
    final sumInsured = areaHa * 50000.0;
    final farmerPremium = sumInsured * 0.015; // 1.5% Rabi PMFBY

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: AgriShieldTheme.surfaceContainerLowest,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AgriShieldTheme.primary.withValues(alpha: 0.3)),
            boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.04), blurRadius: 8)],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('PMFBY Scheme Coverage', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(color: AgriShieldTheme.warningContainer, borderRadius: BorderRadius.circular(12)),
                    child: const Text('Eligible', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onWarningContainer, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Sum Insured:', style: TextStyle(fontSize: 14)),
                  Text('₹${sumInsured.toStringAsFixed(0)}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AgriShieldTheme.primary)),
                ],
              ),
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Farmer Share (1.5% Rabi):', style: TextStyle(fontSize: 14)),
                  Text('₹${farmerPremium.toStringAsFixed(0)}', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AgriShieldTheme.secondaryContainer)),
                ],
              ),
              const SizedBox(height: 16),
              const Divider(),
              const SizedBox(height: 8),
              const Text(
                '• Guaranteed compensation against Drought, Flood & Pests\n• Fully timestamped and audited on Polygon Amoy blockchain',
                style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant, height: 1.5),
              ),
            ],
          ),
        ),
        const SizedBox(height: 20),
        ElevatedButton(
          onPressed: () {
            Navigator.push(context, MaterialPageRoute(builder: (_) => InsuranceQuoteScreen(
              farm: widget.farm,
              farmId: widget.farm['id']?.toString() ?? '',
              crop: widget.farm['crop'] ?? 'Wheat',
              areaM2: areaM2 > 0 ? areaM2 : 10000.0,
              farmName: widget.farm['name'],
            )));
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: AgriShieldTheme.primary,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(vertical: 16),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          ),
          child: const Text('Get Instant Quote & Buy Protection', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
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
              decoration: BoxDecoration(color: AgriShieldTheme.primary.withValues(alpha: 0.1), shape: BoxShape.circle),
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
