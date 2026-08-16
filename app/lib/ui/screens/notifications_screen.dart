import 'dart:ui';
import 'package:flutter/material.dart';
import '../../theme.dart';

class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({super.key});

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
              backgroundColor: AgriShieldTheme.surface.withValues(alpha: 0.8),
              elevation: 0,
              iconTheme: const IconThemeData(color: AgriShieldTheme.onSurface),
              title: const Text('Alerts', style: TextStyle(color: AgriShieldTheme.onSurface, fontWeight: FontWeight.w600, fontSize: 20)),
              actions: [
                IconButton(
                  icon: const Icon(Icons.translate, color: AgriShieldTheme.onSurfaceVariant),
                  onPressed: () {},
                ),
                Padding(
                  padding: const EdgeInsets.only(right: 16.0),
                  child: CircleAvatar(
                    radius: 16,
                    backgroundColor: AgriShieldTheme.primaryContainer,
                    child: const Icon(Icons.person, size: 20, color: Colors.white),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      body: ListView(
        padding: EdgeInsets.only(
          top: MediaQuery.of(context).padding.top + 76,
          left: 16, right: 16, bottom: 100,
        ),
        children: [
          _buildNotificationCard(
            icon: Icons.thunderstorm,
            iconBg: AgriShieldTheme.error,
            iconFg: AgriShieldTheme.onError,
            cardBg: AgriShieldTheme.errorContainer,
            title: 'Heavy Rainfall Alert',
            titleColor: AgriShieldTheme.onErrorContainer,
            subtitle: 'Next 48 hrs. Expected 50-70mm rainfall. Secure harvested crops immediately.',
            subtitleColor: AgriShieldTheme.onErrorContainer.withValues(alpha: 0.8),
            metadata: 'High Priority • Just now',
            metadataColor: AgriShieldTheme.error,
          ),
          const SizedBox(height: 16),
          _buildNotificationCard(
            icon: Icons.bug_report,
            iconBg: AgriShieldTheme.secondaryContainer,
            iconFg: AgriShieldTheme.onSecondaryContainer,
            cardBg: AgriShieldTheme.secondaryContainer.withValues(alpha: 0.2),
            title: 'Pest Outbreak Alert',
            titleColor: AgriShieldTheme.onSurface,
            subtitle: 'Fall Armyworm detected in your area. Inspect maize crops within 3 days.',
            subtitleColor: AgriShieldTheme.onSurfaceVariant,
            metadata: 'Medium Priority • 2 hours ago',
            metadataColor: AgriShieldTheme.secondaryContainer,
          ),
          const SizedBox(height: 16),
          _buildNotificationCard(
            icon: Icons.water_drop,
            iconBg: AgriShieldTheme.primaryContainer,
            iconFg: AgriShieldTheme.onPrimaryContainer,
            cardBg: AgriShieldTheme.surfaceVariant.withValues(alpha: 0.3),
            title: 'Irrigation Reminder',
            titleColor: AgriShieldTheme.onSurface,
            subtitle: 'Farm A (Wheat) soil moisture is dropping. Plan irrigation for tomorrow morning.',
            subtitleColor: AgriShieldTheme.onSurfaceVariant,
            metadata: 'Low Priority • Yesterday',
            metadataColor: AgriShieldTheme.onSurfaceVariant,
          ),
        ],
      ),
    );
  }

  Widget _buildNotificationCard({
    required IconData icon,
    required Color iconBg,
    required Color iconFg,
    required Color cardBg,
    required String title,
    required Color titleColor,
    required String subtitle,
    required Color subtitleColor,
    required String metadata,
    required Color metadataColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.04), blurRadius: 4)],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 48, height: 48,
            decoration: BoxDecoration(color: iconBg, shape: BoxShape.circle),
            child: Icon(icon, color: iconFg, size: 28),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: titleColor)),
                const SizedBox(height: 4),
                Text(subtitle, style: TextStyle(fontSize: 14, color: subtitleColor)),
                const SizedBox(height: 8),
                Text(metadata, style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: metadataColor)),
              ],
            ),
          )
        ],
      ),
    );
  }
}
