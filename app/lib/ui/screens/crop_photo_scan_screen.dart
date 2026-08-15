import 'package:flutter/material.dart';
import 'package:camera/camera.dart';

class CropPhotoScanScreen extends StatefulWidget {
  const CropPhotoScanScreen({super.key});

  @override
  State<CropPhotoScanScreen> createState() => _CropPhotoScanScreenState();
}

class _CropPhotoScanScreenState extends State<CropPhotoScanScreen> {
  CameraController? _controller;
  bool _isAssessing = false;
  String? _assessmentResult;

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    final cameras = await availableCameras();
    if (cameras.isNotEmpty) {
      _controller = CameraController(cameras.first, ResolutionPreset.medium);
      await _controller?.initialize();
      if (mounted) setState(() {});
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Scan Crop')),
      body: Stack(
        children: [
          Positioned.fill(child: CameraPreview(_controller!)),
          // Leaf guide overlay
          Center(
            child: Container(
              width: 250,
              height: 350,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.white, width: 2),
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Align(
                alignment: Alignment.bottomCenter,
                child: Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('Align leaf within frame', style: TextStyle(color: Colors.white, shadows: [Shadow(blurRadius: 4, color: Colors.black)])),
                ),
              ),
            ),
          ),
          if (_assessmentResult != null)
            Positioned(
              bottom: 120,
              left: 24,
              right: 24,
              child: Card(
                color: Theme.of(context).colorScheme.surface,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text('Result', style: Theme.of(context).textTheme.titleLarge),
                      const SizedBox(height: 8),
                      Text(_assessmentResult!, style: const TextStyle(fontWeight: FontWeight.bold)),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: FloatingActionButton(
        onPressed: _isAssessing ? null : () async {
          setState(() => _isAssessing = true);
          // Simulate taking picture and calling AI
          await Future.delayed(const Duration(seconds: 2));
          setState(() {
            _isAssessing = false;
            _assessmentResult = 'Diseased: Early Blight (88% confidence)';
          });
        },
        child: _isAssessing ? const CircularProgressIndicator(color: Colors.white) : const Icon(Icons.camera_alt),
      ),
    );
  }
}
