import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers.dart';
import '../../theme.dart';
import 'farm_detail_screen.dart';
import 'add_farm_screen.dart';

import 'dart:async';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  Timer? _pollingTimer;

  @override
  void initState() {
    super.initState();
    _pollingTimer = Timer.periodic(const Duration(seconds: 10), (_) {
      ref.invalidate(farmsProvider);
    });
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final farmsAsync = ref.watch(farmsProvider);

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(60),
        child: ClipRect(
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: AppBar(
              backgroundColor: AgriShieldTheme.surface.withValues(alpha: 0.8),
              elevation: 0,
              title: Row(
                children: [
                  Image.asset('assets/images/logo.webp', height: 24),
                  const SizedBox(width: 8),
                  Text(
                    'Home',
                    style: TextStyle(
                      color: AgriShieldTheme.onSurface,
                      fontWeight: FontWeight.w600,
                      fontSize: 20,
                    ),
                  ),
                ],
              ),
              actions: [
                PopupMenuButton<String>(
                  icon: const Icon(Icons.translate, color: AgriShieldTheme.onSurfaceVariant),
                  onSelected: (value) {
                    // Language logic
                  },
                  itemBuilder: (context) => [
                    const PopupMenuItem(value: 'en', child: Text('English')),
                    const PopupMenuItem(value: 'hi', child: Text('Hindi')),
                  ],
                ),
                Padding(
                  padding: const EdgeInsets.only(right: 8.0),
                  child: InkWell(
                    onTap: () {
                      ref.read(bottomNavIndexProvider.notifier).state = 4; // Navigate to Profile
                    },
                    borderRadius: BorderRadius.circular(16),
                    child: CircleAvatar(
                      radius: 16,
                      backgroundColor: AgriShieldTheme.primaryContainer,
                      child: const Icon(Icons.person, size: 20, color: Colors.white),
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.logout, color: AgriShieldTheme.error),
                  onPressed: () {
                    // Sign out logic
                    Navigator.of(context).pushReplacementNamed('/'); // or back to login
                  },
                ),
                const SizedBox(width: 8),
              ],
            ),
          ),
        ),
      ),
      body: farmsAsync.when(
        data: (farms) {
          return ListView(
            padding: EdgeInsets.only(
              top: MediaQuery.of(context).padding.top + 76, // Safe area + appbar + spacing
              bottom: 100, // Space for bottom nav and fab
              left: 16,
              right: 16,
            ),
            children: [
              _buildWelcomeHeader(ref.watch(userProvider)),
              const SizedBox(height: 24),
              _buildWeatherBanner(ref.watch(weatherProvider)),
              const SizedBox(height: 24),
              const Text(
                'Your Farms',
                style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: AgriShieldTheme.onBackground),
              ),
              const SizedBox(height: 16),
              if (farms.isEmpty)
                const Center(child: Text('No farms added yet.'))
              else
                ...farms.map((farm) => _buildFarmCard(context, farm)),
            ],
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.of(context).push(
            MaterialPageRoute(builder: (context) => const AddFarmScreen()),
          );
        },
        backgroundColor: AgriShieldTheme.primary,
        foregroundColor: AgriShieldTheme.onPrimary,
        elevation: 4,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        child: const Icon(Icons.add, size: 28),
      ),
    );
  }

  Widget _buildWelcomeHeader(AsyncValue<Map<String, dynamic>> userAsync) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        userAsync.when(
          data: (user) {
            final name = user['name']?.toString().split(' ').first ?? 'Farmer';
            return Text(
              'Hello, $name 👋',
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                letterSpacing: -0.5,
                color: AgriShieldTheme.onBackground,
              ),
            );
          },
          loading: () => const Text(
            'Hello 👋',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: AgriShieldTheme.onBackground,
            ),
          ),
          error: (err, stack) => const Text(
            'Hello 👋',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: AgriShieldTheme.onBackground,
            ),
          ),
        ),
        const SizedBox(height: 4),
        const Text(
          'Here is the status of your farms today.',
          style: TextStyle(
            fontSize: 16,
            color: AgriShieldTheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }

  Widget _buildWeatherBanner(AsyncValue<Map<String, dynamic>> weatherAsync) {
    return Container(
      decoration: BoxDecoration(
        color: AgriShieldTheme.primaryContainer,
        borderRadius: BorderRadius.circular(12),
      ),
      padding: const EdgeInsets.all(16),
      child: weatherAsync.when(
        data: (weather) {
          final rawTemp = weather['temp'] ?? weather['temperature_celsius'];
          final String temp = rawTemp is num 
              ? rawTemp.toStringAsFixed(0) 
              : (rawTemp?.toString() ?? '26');
          final condition = weather['condition'] ?? 'Clear';
          
          return Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.2),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.cloud, color: AgriShieldTheme.onPrimaryContainer, size: 28),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '$temp°C, $condition',
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w600,
                        color: AgriShieldTheme.onPrimary,
                      ),
                    ),
                    Text(
                      'Weather data fetched successfully.',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w500,
                        color: AgriShieldTheme.onPrimary.withValues(alpha: 0.9),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          );
        },
        loading: () => const Center(child: CircularProgressIndicator(color: AgriShieldTheme.onPrimaryContainer)),
        error: (err, stack) => const Text('Failed to load weather data', style: TextStyle(color: AgriShieldTheme.onPrimaryContainer)),
      ),
    );
  }

  Widget _buildFarmCard(BuildContext context, Map<String, dynamic> farm) {
    bool hasInsurance = farm['has_insurance'] ?? false;
    String status = farm['status'] ?? 'PENDING';
    
    // Determine colors based on status
    Color topBarColor = AgriShieldTheme.primary;
    Color riskBg = AgriShieldTheme.tertiaryFixed;
    Color riskFg = AgriShieldTheme.onTertiaryFixed;
    Color riskDot = AgriShieldTheme.primary;
    String riskText = 'Low Risk';

    if (status == 'PENDING') {
      topBarColor = AgriShieldTheme.secondaryContainer;
      riskBg = AgriShieldTheme.warningContainer;
      riskFg = AgriShieldTheme.onWarningContainer;
      riskDot = AgriShieldTheme.warningDot;
      riskText = 'Med Risk: Pests';
    } else if (!hasInsurance) {
      topBarColor = Colors.transparent;
      riskBg = AgriShieldTheme.errorContainer;
      riskFg = AgriShieldTheme.onErrorContainer;
      riskDot = AgriShieldTheme.error;
      riskText = 'High Risk: Drought';
    }

    return GestureDetector(
      onTap: () {
        Navigator.of(context).push(MaterialPageRoute(builder: (context) => FarmDetailScreen(farm: farm)));
      },
      child: Container(
        margin: const EdgeInsets.only(bottom: 16),
        decoration: BoxDecoration(
          color: AgriShieldTheme.surfaceContainerLowest,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.04),
              blurRadius: 8,
              offset: const Offset(0, 1),
            )
          ],
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: Column(
            children: [
              // Top Color Bar
              Container(height: 6, width: double.infinity, color: topBarColor),
              Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Header Row with Image
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                farm['crop'] ?? 'Unknown Crop',
                                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: AgriShieldTheme.onSurface),
                              ),
                              const SizedBox(height: 4),
                              Row(
                                children: [
                                  const Icon(Icons.location_on, size: 16, color: AgriShieldTheme.onSurfaceVariant),
                                  const SizedBox(width: 4),
                                  Text(
                                    farm['name'] ?? 'Plot',
                                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: AgriShieldTheme.onSurfaceVariant),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Container(
                            width: 64,
                            height: 64,
                            color: AgriShieldTheme.surfaceVariant,
                            child: const Icon(Icons.landscape, color: Colors.grey),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    // Risk & Weather Row
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                          decoration: BoxDecoration(
                            color: riskBg,
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Row(
                            children: [
                              Container(
                                width: 8,
                                height: 8,
                                decoration: BoxDecoration(
                                  color: riskDot,
                                  shape: BoxShape.circle,
                                  boxShadow: [
                                    BoxShadow(color: riskDot.withValues(alpha: 0.4), blurRadius: 4),
                                  ]
                                ),
                              ),
                              const SizedBox(width: 6),
                              Text(
                                riskText,
                                style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: riskFg),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 16),
                        Row(
                          children: [
                            const Icon(Icons.water_drop, size: 18, color: AgriShieldTheme.onSurfaceVariant),
                            const SizedBox(width: 4),
                            const Text('Soil Moist: 65%', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: AgriShieldTheme.onSurfaceVariant)),
                          ],
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    const Divider(height: 1, color: AgriShieldTheme.surfaceVariant),
                    const SizedBox(height: 12),
                    // Bottom Row
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        if (hasInsurance && status == 'VERIFIED')
                          Row(
                            children: [
                              const Icon(Icons.verified, size: 20, color: AgriShieldTheme.primary),
                              const SizedBox(width: 6),
                              const Text('Insured (PMFBY)', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AgriShieldTheme.primary)),
                            ],
                          )
                        else if (hasInsurance && status == 'PENDING')
                          Row(
                            children: [
                              const Icon(Icons.pending_actions, size: 20, color: AgriShieldTheme.secondaryContainer),
                              const SizedBox(width: 6),
                              Text('Claim Pending', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.orange.shade800)),
                            ],
                          )
                        else
                          Row(
                            children: [
                              const Icon(Icons.gpp_bad, size: 20, color: AgriShieldTheme.onSurfaceVariant),
                              const SizedBox(width: 6),
                              const Text('Not Insured', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: AgriShieldTheme.onSurfaceVariant)),
                            ],
                          ),
                        if (!hasInsurance)
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: AgriShieldTheme.primary.withValues(alpha: 0.1),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: const Text('Protect Now', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AgriShieldTheme.primary)),
                          )
                        else
                          const Icon(Icons.chevron_right, color: AgriShieldTheme.onSurfaceVariant),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
