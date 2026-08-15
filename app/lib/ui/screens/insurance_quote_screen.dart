import 'dart:ui';
import 'package:flutter/material.dart';
import '../../theme.dart';

class InsuranceQuoteScreen extends StatelessWidget {
  final String farmId;
  final String crop;
  final double areaM2;

  const InsuranceQuoteScreen({super.key, required this.farmId, required this.crop, required this.areaM2});

  @override
  Widget build(BuildContext context) {
    double hectares = areaM2 / 10000;
    double premium = hectares * 1240 / 2.4; // mock calc

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
              title: const Text('Policy Enrollment', style: TextStyle(color: AgriShieldTheme.onSurface, fontWeight: FontWeight.w600, fontSize: 20)),
            ),
          ),
        ),
      ),
      body: Stack(
        children: [
          ListView(
            padding: EdgeInsets.only(
              top: MediaQuery.of(context).padding.top + 76,
              left: 16, right: 16, bottom: 120, // leave space for fixed CTA
            ),
            children: [
              // Hero
              Column(
                children: [
                  const Text('Total Premium', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurfaceVariant, letterSpacing: 1)),
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Padding(
                        padding: EdgeInsets.only(top: 8, right: 4),
                        child: Text('₹', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AgriShieldTheme.primary)),
                      ),
                      Text(premium.toStringAsFixed(0), style: const TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: AgriShieldTheme.primary)),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                    decoration: BoxDecoration(color: AgriShieldTheme.surfaceVariant.withOpacity(0.5), borderRadius: BorderRadius.circular(16)),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: const [
                        Icon(Icons.verified, size: 16, color: AgriShieldTheme.primary),
                        SizedBox(width: 8),
                        Text('PMFBY Approved Quote', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AgriShieldTheme.onSurface)),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 32),
              
              // Summary Card
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: AgriShieldTheme.surfaceContainerLowest,
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8)],
                ),
                child: Column(
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 48, height: 48,
                          decoration: BoxDecoration(color: AgriShieldTheme.tertiaryFixed, borderRadius: BorderRadius.circular(24)),
                          child: const Icon(Icons.agriculture, color: AgriShieldTheme.onTertiaryFixed),
                        ),
                        const SizedBox(width: 16),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(crop, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                            const SizedBox(height: 4),
                            Row(
                              children: [
                                const Icon(Icons.straighten, size: 16, color: AgriShieldTheme.onSurfaceVariant),
                                const SizedBox(width: 4),
                                Text('${hectares.toStringAsFixed(1)} Hectares', style: const TextStyle(color: AgriShieldTheme.onSurfaceVariant)),
                              ],
                            ),
                          ],
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    const Divider(),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: const [
                        Text('Village', style: TextStyle(color: AgriShieldTheme.onSurfaceVariant)),
                        Text('Rampur, Block 4', style: TextStyle(fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: const [
                        Text('Coverage Period', style: TextStyle(color: AgriShieldTheme.onSurfaceVariant)),
                        Text('Nov \'24 - Apr \'25', style: TextStyle(fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              
              // Breakdown Card
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: AgriShieldTheme.surface,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AgriShieldTheme.surfaceVariant),
                ),
                child: Column(
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.receipt_long, color: AgriShieldTheme.primary, size: 20),
                        SizedBox(width: 8),
                        Text('Premium Breakdown', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: AgriShieldTheme.onSurface)),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Base Rate'),
                        Text('₹${(premium * 0.9).toStringAsFixed(0)}'),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: const [
                            Text('Risk Adjustment'),
                            SizedBox(width: 8),
                            Icon(Icons.info, size: 16, color: AgriShieldTheme.primary),
                          ],
                        ),
                        Text('₹${(premium * 0.1).toStringAsFixed(0)}'),
                      ],
                    ),
                    const SizedBox(height: 16),
                    const Divider(),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Farmer Share (2%)', style: TextStyle(fontWeight: FontWeight.bold)),
                        Text('₹${premium.toStringAsFixed(0)}', style: const TextStyle(fontWeight: FontWeight.bold)),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(color: AgriShieldTheme.primary.withOpacity(0.1), borderRadius: BorderRadius.circular(12), border: Border.all(color: AgriShieldTheme.primary.withOpacity(0.2))),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Icon(Icons.security, color: AgriShieldTheme.primary, size: 16),
                          SizedBox(width: 12),
                          Expanded(child: Text('Government subsidies of ₹5,600 have already been applied to this quote.', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant))),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 32),
              
              // Trust Badges
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _buildTrustBadge(Icons.gpp_good, 'Govt Approved'),
                  const SizedBox(width: 32),
                  _buildTrustBadge(Icons.support_agent, '24/7 Support'),
                  const SizedBox(width: 32),
                  _buildTrustBadge(Icons.payments, 'Secure Pay'),
                ],
              ),
            ],
          ),
          
          // Fixed Bottom CTA
          Positioned(
            bottom: 0, left: 0, right: 0,
            child: ClipRect(
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                child: Container(
                  padding: const EdgeInsets.fromLTRB(16, 16, 16, 32),
                  decoration: BoxDecoration(
                    color: AgriShieldTheme.surface.withOpacity(0.9),
                    border: const Border(top: BorderSide(color: AgriShieldTheme.surfaceVariant)),
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      ElevatedButton(
                        onPressed: () {},
                        style: ElevatedButton.styleFrom(backgroundColor: AgriShieldTheme.secondaryContainer, foregroundColor: AgriShieldTheme.onSecondaryContainer),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.lock),
                            const SizedBox(width: 8),
                            Text('Pay ₹${premium.toStringAsFixed(0)} to Buy Policy'),
                          ],
                        ),
                      ),
                      const SizedBox(height: 8),
                      const Text('By proceeding, you agree to the PMFBY Terms & Conditions.', style: TextStyle(fontSize: 10, color: AgriShieldTheme.onSurfaceVariant)),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTrustBadge(IconData icon, String text) {
    return Column(
      children: [
        Icon(icon, size: 32, color: AgriShieldTheme.primary),
        const SizedBox(height: 4),
        Text(text, style: const TextStyle(fontSize: 10, color: AgriShieldTheme.onSurfaceVariant)),
      ],
    );
  }
}
