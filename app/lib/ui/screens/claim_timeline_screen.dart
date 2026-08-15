import 'dart:ui';
import 'package:flutter/material.dart';
import '../../theme.dart';

class ClaimTimelineScreen extends StatelessWidget {
  final String claimId;

  const ClaimTimelineScreen({super.key, this.claimId = 'IND-8472'});

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
              title: const Text('Insurance', style: TextStyle(color: AgriShieldTheme.onSurface, fontWeight: FontWeight.w600, fontSize: 20)),
            ),
          ),
        ),
      ),
      body: ListView(
        padding: EdgeInsets.only(
          top: MediaQuery.of(context).padding.top + 76,
          left: 16, right: 16, bottom: 24,
        ),
        children: [
          // Header Card
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: AgriShieldTheme.surfaceContainerLowest,
              borderRadius: BorderRadius.circular(16),
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8)],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('Claim #$claimId', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      decoration: BoxDecoration(color: AgriShieldTheme.primary.withOpacity(0.1), borderRadius: BorderRadius.circular(16)),
                      child: Row(
                        children: const [
                          Icon(Icons.sync, size: 16, color: AgriShieldTheme.primary),
                          SizedBox(width: 4),
                          Text('In Progress', style: TextStyle(fontSize: 12, color: AgriShieldTheme.primary, fontWeight: FontWeight.w600)),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                const Text('Wheat Crop Damage • Multi-Peril', style: TextStyle(color: AgriShieldTheme.onSurfaceVariant)),
                const SizedBox(height: 12),
                Row(
                  children: const [
                    Icon(Icons.calendar_today, size: 16, color: AgriShieldTheme.primary),
                    SizedBox(width: 8),
                    Text('Filed: Oct 12, 2023', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant)),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          
          // Timeline
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: AgriShieldTheme.surfaceContainerLowest,
              borderRadius: BorderRadius.circular(16),
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8)],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Processing Status', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                const SizedBox(height: 24),
                
                _buildTimelineStep(
                  title: 'Claim Submitted',
                  subtitle: 'Oct 12, 10:45 AM',
                  isCompleted: true,
                  isLast: false,
                ),
                _buildTimelineStep(
                  title: 'Satellite & AI Assessment',
                  subtitle: 'Damage severity estimated at 42% based on NDVI data.',
                  isCompleted: true,
                  isLast: false,
                  child: Container(
                    margin: const EdgeInsets.only(top: 8),
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(color: AgriShieldTheme.surfaceVariant.withOpacity(0.5), borderRadius: BorderRadius.circular(8)),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: const [
                        Icon(Icons.visibility, size: 16, color: AgriShieldTheme.primary),
                        SizedBox(width: 8),
                        Text('View Satellite Imagery', style: TextStyle(fontSize: 12, color: AgriShieldTheme.primary, fontWeight: FontWeight.w600)),
                      ],
                    ),
                  ),
                ),
                _buildTimelineStep(
                  title: 'Under Local Review',
                  subtitle: 'Your local agriculture officer is verifying the AI report.',
                  isCompleted: false,
                  isActive: true,
                  isLast: false,
                  child: Container(
                    margin: const EdgeInsets.only(top: 12),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(color: AgriShieldTheme.surfaceVariant.withOpacity(0.3), borderRadius: BorderRadius.circular(12)),
                    child: Row(
                      children: [
                        Container(
                          width: 40, height: 40,
                          decoration: const BoxDecoration(shape: BoxShape.circle, image: DecorationImage(image: NetworkImage('https://picsum.photos/100'), fit: BoxFit.cover)),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: const [
                              Text('Officer R. Sharma', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                              Text('Assigned Verifier', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant)),
                            ],
                          ),
                        ),
                        Container(
                          width: 40, height: 40,
                          decoration: BoxDecoration(color: AgriShieldTheme.surfaceVariant, shape: BoxShape.circle),
                          child: const Icon(Icons.call, color: AgriShieldTheme.primary, size: 20),
                        ),
                      ],
                    ),
                  ),
                ),
                _buildTimelineStep(
                  title: 'Payout Approved',
                  subtitle: 'Awaiting final sign-off.',
                  isCompleted: false,
                  isLast: true,
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          
          // Blockchain Badge
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: AgriShieldTheme.tertiaryFixed, borderRadius: BorderRadius.circular(16)),
            child: Row(
              children: [
                Container(
                  width: 48, height: 48,
                  decoration: const BoxDecoration(color: AgriShieldTheme.onTertiaryFixed, shape: BoxShape.circle),
                  child: const Icon(Icons.verified_user, color: AgriShieldTheme.tertiaryFixed),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Verified on Blockchain', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AgriShieldTheme.onTertiaryFixed)),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                            decoration: BoxDecoration(color: AgriShieldTheme.onTertiaryFixed.withOpacity(0.8), borderRadius: BorderRadius.circular(4)),
                            child: const Text('0x4a2...7f9', style: TextStyle(fontFamily: 'monospace', fontSize: 12, color: AgriShieldTheme.tertiaryFixed)),
                          ),
                          const SizedBox(width: 8),
                          const Icon(Icons.content_copy, size: 16, color: AgriShieldTheme.onTertiaryFixed),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 32),
          
          // Contact Support
          OutlinedButton(
            onPressed: () {},
            style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(56), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16))),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: const [
                Icon(Icons.help_outline),
                SizedBox(width: 8),
                Text('Contact Support', style: TextStyle(fontSize: 16)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTimelineStep({required String title, required String subtitle, required bool isCompleted, bool isActive = false, required bool isLast, Widget? child}) {
    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 24,
            child: Column(
              children: [
                Container(
                  width: 24, height: 24,
                  decoration: BoxDecoration(
                    color: isCompleted ? AgriShieldTheme.primary : (isActive ? AgriShieldTheme.surfaceContainerLowest : AgriShieldTheme.surfaceVariant),
                    border: isActive ? Border.all(color: AgriShieldTheme.primary, width: 2) : null,
                    shape: BoxShape.circle,
                  ),
                  child: isCompleted 
                    ? const Icon(Icons.check, size: 16, color: Colors.white)
                    : (isActive ? Center(child: Container(width: 10, height: 10, decoration: const BoxDecoration(color: AgriShieldTheme.primary, shape: BoxShape.circle))) : null),
                ),
                if (!isLast)
                  Expanded(child: Container(width: 2, color: isCompleted ? AgriShieldTheme.primary : AgriShieldTheme.surfaceVariant)),
              ],
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(bottom: 32.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: isActive ? AgriShieldTheme.primary : (isCompleted ? AgriShieldTheme.onSurface : AgriShieldTheme.onSurfaceVariant.withOpacity(0.7)))),
                  const SizedBox(height: 4),
                  Text(subtitle, style: TextStyle(fontSize: 14, color: isCompleted || isActive ? AgriShieldTheme.onSurfaceVariant : AgriShieldTheme.onSurfaceVariant.withOpacity(0.7))),
                  if (child != null) child,
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
