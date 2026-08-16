import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../../theme.dart';

class AddFarmScreen extends StatefulWidget {
  const AddFarmScreen({super.key});

  @override
  State<AddFarmScreen> createState() => _AddFarmScreenState();
}

class _AddFarmScreenState extends State<AddFarmScreen> {
  final List<LatLng> _polygonPoints = [];
  
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
              title: const Text(
                'Farms',
                style: TextStyle(
                  color: AgriShieldTheme.onSurface,
                  fontWeight: FontWeight.w600,
                  fontSize: 20,
                ),
              ),
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
                  polygons: <Polygon<Object>>[
                    Polygon<Object>(
                      points: _polygonPoints,
                      color: AgriShieldTheme.primary.withValues(alpha: 0.3),
                      borderColor: AgriShieldTheme.primary,
                      borderStrokeWidth: 3,
                    ),
                  ],
                ),
              MarkerLayer(
                markers: _polygonPoints.map((point) => Marker(
                  point: point,
                  width: 16,
                  height: 16,
                  child: Container(
                    decoration: BoxDecoration(
                      color: AgriShieldTheme.surfaceContainerLowest,
                      shape: BoxShape.circle,
                      border: Border.all(color: AgriShieldTheme.primary, width: 4),
                    ),
                  ),
                )).toList(),
              ),
            ],
          ),
          // Top Instructions Pill
          Positioned(
            top: MediaQuery.of(context).padding.top + 76,
            left: 24,
            right: 24,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(30),
                  child: BackdropFilter(
                    filter: ImageFilter.blur(sigmaX: 5, sigmaY: 5),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                      decoration: BoxDecoration(
                        color: AgriShieldTheme.surface.withValues(alpha: 0.95),
                        borderRadius: BorderRadius.circular(30),
                        boxShadow: [
                          BoxShadow(color: Colors.black.withValues(alpha: 0.1), blurRadius: 4, offset: const Offset(0, 2)),
                        ],
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.directions_walk, color: AgriShieldTheme.primary, size: 20),
                          const SizedBox(width: 8),
                          const Text('Walk boundary or tap', style: TextStyle(fontWeight: FontWeight.w600, color: AgriShieldTheme.onSurface)),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          // Crosshair
          const Center(
            child: Icon(Icons.my_location, size: 40, color: AgriShieldTheme.primary),
          ),
          // Floating Bottom Action Card
          Positioned(
            bottom: 24,
            left: 16,
            right: 16,
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AgriShieldTheme.surfaceContainerLowest,
                borderRadius: BorderRadius.circular(24),
                boxShadow: [
                  BoxShadow(color: Colors.black.withValues(alpha: 0.1), blurRadius: 20, offset: const Offset(0, 4)),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              const Icon(Icons.straighten, size: 16, color: AgriShieldTheme.onSurfaceVariant),
                              const SizedBox(width: 4),
                              const Text('Calculated Area', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: AgriShieldTheme.onSurfaceVariant)),
                            ],
                          ),
                          const SizedBox(height: 4),
                          RichText(
                            text: TextSpan(
                              children: [
                                TextSpan(
                                  text: (_polygonPoints.length * 0.5).toStringAsFixed(1),
                                  style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AgriShieldTheme.primary, fontFamily: 'Inter'),
                                ),
                                const TextSpan(
                                  text: ' Hectares',
                                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: AgriShieldTheme.onSurfaceVariant, fontFamily: 'Inter'),
                                )
                              ]
                            )
                          ),
                        ],
                      ),
                      InkWell(
                        onTap: () {
                          if (_polygonPoints.isNotEmpty) {
                            setState(() => _polygonPoints.removeLast());
                          }
                        },
                        borderRadius: BorderRadius.circular(24),
                        child: Container(
                          width: 48,
                          height: 48,
                          decoration: BoxDecoration(
                            color: AgriShieldTheme.secondaryContainer.withValues(alpha: 0.2),
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.undo, color: AgriShieldTheme.secondaryContainer),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton(
                    onPressed: _polygonPoints.length >= 3 ? () {
                      if (_hasSelfIntersection(_polygonPoints)) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Invalid boundary: Polygon self-intersects')),
                        );
                        return;
                      }
                      double mockAreaHectares = _polygonPoints.length * 0.5;
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Farm boundary saved! Area: ${mockAreaHectares.toStringAsFixed(1)} ha')),
                      );
                      if (Navigator.canPop(context)) {
                        Navigator.of(context).pop();
                      } else {
                        setState(() {
                          _polygonPoints.clear();
                        });
                      }
                    } : null,
                    style: ElevatedButton.styleFrom(
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: const [
                        Icon(Icons.check_circle),
                        SizedBox(width: 8),
                        Text('Save Boundary'),
                      ],
                    ),
                  )
                ],
              ),
            ),
          )
        ],
      ),
    );
  }

  bool _hasSelfIntersection(List<LatLng> points) {
    if (points.length < 4) return false;
    for (int i = 0; i < points.length; i++) {
      LatLng a1 = points[i];
      LatLng a2 = points[(i + 1) % points.length];
      for (int j = i + 2; j < points.length; j++) {
        if (i == 0 && j == points.length - 1) continue;
        LatLng b1 = points[j];
        LatLng b2 = points[(j + 1) % points.length];
        if (_doIntersect(a1, a2, b1, b2)) return true;
      }
    }
    return false;
  }

  bool _doIntersect(LatLng p1, LatLng q1, LatLng p2, LatLng q2) {
    double orientation(LatLng p, LatLng q, LatLng r) {
      double val = (q.longitude - p.longitude) * (r.latitude - q.latitude) -
          (q.latitude - p.latitude) * (r.longitude - q.longitude);
      if (val == 0) return 0;
      return (val > 0) ? 1 : 2;
    }

    bool onSegment(LatLng p, LatLng q, LatLng r) {
      return q.longitude <= (p.longitude > r.longitude ? p.longitude : r.longitude) &&
          q.longitude >= (p.longitude < r.longitude ? p.longitude : r.longitude) &&
          q.latitude <= (p.latitude > r.latitude ? p.latitude : r.latitude) &&
          q.latitude >= (p.latitude < r.latitude ? p.latitude : r.latitude);
    }

    double o1 = orientation(p1, q1, p2);
    double o2 = orientation(p1, q1, q2);
    double o3 = orientation(p2, q2, p1);
    double o4 = orientation(p2, q2, q1);

    if (o1 != o2 && o3 != o4) return true;
    if (o1 == 0 && onSegment(p1, p2, q1)) return true;
    if (o2 == 0 && onSegment(p1, q2, q1)) return true;
    if (o3 == 0 && onSegment(p2, p1, q2)) return true;
    if (o4 == 0 && onSegment(p2, q1, q2)) return true;
    return false;
  }
}
