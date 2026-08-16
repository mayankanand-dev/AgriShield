import 'dart:ui';
import 'package:flutter/material.dart';
import '../../theme.dart';

class CropPhotoScanScreen extends StatefulWidget {
  const CropPhotoScanScreen({super.key});

  @override
  State<CropPhotoScanScreen> createState() => _CropPhotoScanScreenState();
}

class _CropPhotoScanScreenState extends State<CropPhotoScanScreen> with SingleTickerProviderStateMixin {
  bool _showResults = false;
  late AnimationController _scanController;

  @override
  void initState() {
    super.initState();
    _scanController = AnimationController(vsync: this, duration: const Duration(seconds: 2))..repeat(reverse: true);
  }

  @override
  void dispose() {
    _scanController.dispose();
    super.dispose();
  }

  void _captureImage() {
    // Flash effect
    showGeneralDialog(
      context: context,
      barrierColor: Colors.white,
      transitionDuration: const Duration(milliseconds: 100),
      pageBuilder: (context, animation, secondaryAnimation) => const SizedBox.shrink(),
    ).then((_) {
      setState(() {
        _showResults = true;
      });
      _showResultsBottomSheet();
    });
    Future.delayed(const Duration(milliseconds: 100), () {
      if (!mounted) return;
      Navigator.of(context).pop();
    });
  }

  void _showResultsBottomSheet() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildResultsSheet(),
    ).whenComplete(() {
      setState(() {
        _showResults = false;
      });
    });
  }

  Widget _buildResultsSheet() {
    return Container(
      decoration: const BoxDecoration(
        color: AgriShieldTheme.surface,
        borderRadius: BorderRadius.vertical(top: Radius.circular(32)),
        boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 40, offset: Offset(0, -12))],
      ),
      padding: const EdgeInsets.only(bottom: 24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(height: 16),
          Container(width: 48, height: 6, decoration: BoxDecoration(color: AgriShieldTheme.surfaceVariant, borderRadius: BorderRadius.circular(4))),
          const SizedBox(height: 24),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      decoration: BoxDecoration(color: AgriShieldTheme.tertiaryFixed, borderRadius: BorderRadius.circular(16)),
                      child: const Text('Analysis Complete', style: TextStyle(color: AgriShieldTheme.onTertiaryFixed, fontSize: 12, fontWeight: FontWeight.bold)),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: const [
                        Icon(Icons.check_circle, color: AgriShieldTheme.primaryContainer, size: 24),
                        SizedBox(width: 8),
                        Text('Status: Healthy', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                      ],
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: const [
                        Icon(Icons.verified, size: 16, color: AgriShieldTheme.onSurfaceVariant),
                        SizedBox(width: 4),
                        Text('Confidence: 98%', style: TextStyle(fontSize: 16, color: AgriShieldTheme.onSurfaceVariant)),
                      ],
                    ),
                  ],
                ),
                Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    color: AgriShieldTheme.surfaceVariant,
                    borderRadius: BorderRadius.circular(16),
                    image: const DecorationImage(image: NetworkImage('https://picsum.photos/100'), fit: BoxFit.cover),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(color: AgriShieldTheme.secondaryContainer, borderRadius: BorderRadius.circular(16)),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.5), shape: BoxShape.circle),
                    child: const Icon(Icons.eco, color: AgriShieldTheme.onSecondaryContainer),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text('Minor leaf spot detected', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSecondaryContainer)),
                        SizedBox(height: 4),
                        Text('The plant is generally healthy, but we noticed a minor spot. No immediate intervention required.', style: TextStyle(fontSize: 14, color: AgriShieldTheme.onSecondaryContainer)),
                      ],
                    ),
                  )
                ],
              ),
            ),
          ),
          const SizedBox(height: 32),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Row(
              children: [
                Expanded(
                  flex: 2,
                  child: ElevatedButton(
                    onPressed: () => Navigator.pop(context),
                    style: ElevatedButton.styleFrom(backgroundColor: AgriShieldTheme.surfaceVariant, foregroundColor: AgriShieldTheme.onSurfaceVariant),
                    child: const Row(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(Icons.refresh), SizedBox(width: 8), Text('Retake')]),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  flex: 3,
                  child: ElevatedButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Row(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(Icons.save), SizedBox(width: 8), Text('Save')]),
                  ),
                ),
              ],
            ),
          )
        ],
      ),
    );
  }

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
              title: const Text('Farm Details', style: TextStyle(color: AgriShieldTheme.onSurface, fontWeight: FontWeight.w600, fontSize: 20)),
            ),
          ),
        ),
      ),
      body: Column(
        children: [
          // Viewfinder
          Expanded(
            flex: 4,
            child: ClipRRect(
              borderRadius: const BorderRadius.vertical(bottom: Radius.circular(32)),
              child: Stack(
                fit: StackFit.expand,
                children: [
                  Container(
                    color: AgriShieldTheme.surfaceVariant,
                    child: const Image(image: NetworkImage('https://picsum.photos/400/600'), fit: BoxFit.cover),
                  ),
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Colors.black45, Colors.transparent, Colors.black45]),
                    ),
                  ),
                  Positioned(
                    top: MediaQuery.of(context).padding.top + 76,
                    left: 24, right: 24,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        _buildIconButton(Icons.flash_auto),
                        _buildIconButton(Icons.cameraswitch),
                      ],
                    ),
                  ),
                  Positioned(
                    top: MediaQuery.of(context).padding.top + 140,
                    left: 0, right: 0,
                    child: Center(
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(30),
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 5, sigmaY: 5),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                            color: Colors.white.withValues(alpha: 0.9),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: const [
                                Icon(Icons.center_focus_strong, color: AgriShieldTheme.primary, size: 20),
                                SizedBox(width: 8),
                                Text('Align leaf within the guide', style: TextStyle(fontWeight: FontWeight.w600)),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  Center(
                    child: SizedBox(
                      width: 250, height: 350,
                      child: Stack(
                        children: [
                          Container(
                            decoration: BoxDecoration(border: Border.all(color: AgriShieldTheme.primaryContainer, width: 2, style: BorderStyle.solid), borderRadius: BorderRadius.circular(16)),
                          ),
                          if (!_showResults)
                            AnimatedBuilder(
                              animation: _scanController,
                              builder: (context, child) {
                                return Positioned(
                                  top: _scanController.value * 350,
                                  left: 0, right: 0,
                                  child: Container(height: 2, decoration: const BoxDecoration(color: AgriShieldTheme.primaryContainer, boxShadow: [BoxShadow(color: AgriShieldTheme.primaryContainer, blurRadius: 8)])),
                                );
                              },
                            ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          // Capture Controls
          Expanded(
            flex: 1,
            child: Container(
              color: AgriShieldTheme.background,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    decoration: BoxDecoration(color: AgriShieldTheme.surfaceVariant, borderRadius: BorderRadius.circular(20)),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4), decoration: BoxDecoration(color: AgriShieldTheme.surface, borderRadius: BorderRadius.circular(16)), child: const Text('1x', style: TextStyle(fontWeight: FontWeight.bold))),
                        const SizedBox(width: 8),
                        const Padding(padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4), child: Text('2x', style: TextStyle(fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurfaceVariant))),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  GestureDetector(
                    onTap: _captureImage,
                    child: Container(
                      width: 80, height: 80,
                      decoration: BoxDecoration(color: AgriShieldTheme.surfaceVariant, shape: BoxShape.circle, border: Border.all(color: AgriShieldTheme.surface, width: 4)),
                      child: Center(
                        child: Container(width: 64, height: 64, decoration: const BoxDecoration(color: AgriShieldTheme.primary, shape: BoxShape.circle), child: const Icon(Icons.camera_alt, color: Colors.white, size: 32)),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildIconButton(IconData icon) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(30),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 5, sigmaY: 5),
        child: Container(
          width: 48, height: 48,
          decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.2), shape: BoxShape.circle),
          child: Icon(icon, color: Colors.white),
        ),
      ),
    );
  }
}
