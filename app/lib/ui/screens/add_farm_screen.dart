import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

class AddFarmScreen extends StatefulWidget {
  const AddFarmScreen({super.key});

  @override
  State<AddFarmScreen> createState() => _AddFarmScreenState();
}

class _AddFarmScreenState extends State<AddFarmScreen> {
  final List<LatLng> _polygonPoints = [];
  
  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Farm Boundary'),
      ),
      body: Stack(
        children: [
          FlutterMap(
            options: MapOptions(
              initialCenter: const LatLng(20.5937, 78.9629), // Center of India
              initialZoom: 5.0,
              onTap: (tapPosition, point) {
                setState(() {
                  _polygonPoints.add(point);
                });
              },
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'dev.mayankanand.agrishield',
              ),
              if (_polygonPoints.isNotEmpty)
                PolygonLayer(
                  polygons: [
                    Polygon(
                      points: _polygonPoints,
                      color: colorScheme.primary.withOpacity(0.3),
                      borderColor: colorScheme.primary,
                      borderStrokeWidth: 3,
                      isFilled: true,
                    ),
                  ],
                ),
              MarkerLayer(
                markers: _polygonPoints.map((point) => Marker(
                  point: point,
                  width: 12,
                  height: 12,
                  child: Container(
                    decoration: BoxDecoration(
                      color: colorScheme.secondary,
                      shape: BoxShape.circle,
                    ),
                  ),
                )).toList(),
              ),
            ],
          ),
          Positioned(
            bottom: 24,
            left: 24,
            right: 24,
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Vertices: ${_polygonPoints.length}', style: Theme.of(context).textTheme.titleMedium),
                        TextButton.icon(
                          onPressed: () => setState(() => _polygonPoints.clear()),
                          icon: const Icon(Icons.clear),
                          label: const Text('Clear'),
                          style: TextButton.styleFrom(foregroundColor: colorScheme.error),
                        )
                      ],
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: _polygonPoints.length >= 3 ? () {
                        // Validate and Save logic
                      } : null,
                      child: const Text('Save Boundary'),
                    )
                  ],
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}
