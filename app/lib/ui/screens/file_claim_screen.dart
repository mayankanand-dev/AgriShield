import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import '../../theme.dart';
import '../../providers.dart';
import '../../api/api_client.dart';

class FileClaimScreen extends ConsumerStatefulWidget {
  final String? policyId;
  final String? farmId;
  const FileClaimScreen({super.key, this.policyId, this.farmId});

  @override
  ConsumerState<FileClaimScreen> createState() => _FileClaimScreenState();
}

class _FileClaimScreenState extends ConsumerState<FileClaimScreen> {
  String _selectedIncident = 'Pest Attack';
  DateTime _selectedDate = DateTime.now();
  bool _isSubmitting = false;
  
  // Store picked files
  final List<File> _evidenceFiles = [];
  final ImagePicker _picker = ImagePicker();

  final List<Map<String, dynamic>> _incidentTypes = [
    {'name': 'Hailstorm', 'icon': Icons.grain, 'code': 'hailstorm'},
    {'name': 'Drought', 'icon': Icons.wb_sunny, 'code': 'drought'},
    {'name': 'Flood', 'icon': Icons.flood, 'code': 'flood'},
    {'name': 'Pest Attack', 'icon': Icons.bug_report, 'code': 'pest'},
  ];

  Future<void> _pickImage() async {
    if (_evidenceFiles.length >= 3) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Maximum 3 photos allowed')));
      return;
    }
    
    final source = await showDialog<ImageSource>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Select Photo Source'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt),
              title: const Text('Camera'),
              onTap: () => Navigator.pop(context, ImageSource.camera),
            ),
            ListTile(
              leading: const Icon(Icons.photo_library),
              title: const Text('Gallery'),
              onTap: () => Navigator.pop(context, ImageSource.gallery),
            ),
          ],
        ),
      ),
    );

    if (source != null) {
      final XFile? image = await _picker.pickImage(source: source);
      if (image != null) {
        setState(() {
          _evidenceFiles.add(File(image.path));
        });
      }
    }
  }

  void _removeImage(int index) {
    setState(() {
      _evidenceFiles.removeAt(index);
    });
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
              title: const Text('Insurance', style: TextStyle(color: AgriShieldTheme.onSurface, fontWeight: FontWeight.w600, fontSize: 20)),
            ),
          ),
        ),
      ),
      body: ListView(
        padding: EdgeInsets.only(
          top: MediaQuery.of(context).padding.top + 76,
          left: 16, right: 16, bottom: 120,
        ),
        children: [
          // Instruction
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: AgriShieldTheme.primaryContainer.withValues(alpha: 0.1), borderRadius: BorderRadius.circular(12)),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.info, color: AgriShieldTheme.primary),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text('File a Crop Damage Claim', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
                      SizedBox(height: 4),
                      Text('Please select the incident type and upload at least 2 clear photos of the affected area.', style: TextStyle(fontSize: 14, color: AgriShieldTheme.onSurfaceVariant)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          
          // Incident Type
          const Text('Select Incident Type', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
          const SizedBox(height: 12),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 2, crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 1.5),
            itemCount: _incidentTypes.length,
            itemBuilder: (context, index) {
              final incident = _incidentTypes[index];
              final isSelected = _selectedIncident == incident['name'];
              return InkWell(
                onTap: () => setState(() => _selectedIncident = incident['name']),
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  decoration: BoxDecoration(
                    color: isSelected ? AgriShieldTheme.primaryContainer.withValues(alpha: 0.2) : AgriShieldTheme.surface,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: isSelected ? AgriShieldTheme.primary : AgriShieldTheme.surfaceVariant, width: isSelected ? 2 : 1),
                    boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.02), blurRadius: 4)],
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(color: isSelected ? AgriShieldTheme.primary.withValues(alpha: 0.1) : AgriShieldTheme.surfaceVariant, shape: BoxShape.circle),
                        child: Icon(incident['icon'], color: isSelected ? AgriShieldTheme.primary : AgriShieldTheme.onSurfaceVariant, size: 28),
                      ),
                      const SizedBox(height: 8),
                      Text(incident['name'], style: TextStyle(fontWeight: FontWeight.w600, color: AgriShieldTheme.onSurface)),
                    ],
                  ),
                ),
              );
            },
          ),
          const SizedBox(height: 24),
          
          // Date Picker
          const Text('Date of Incident', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
          const SizedBox(height: 8),
          InkWell(
            onTap: () async {
              final date = await showDatePicker(context: context, initialDate: _selectedDate, firstDate: DateTime(2020), lastDate: DateTime.now());
              if (date != null) setState(() => _selectedDate = date);
            },
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
              decoration: BoxDecoration(color: AgriShieldTheme.surface, borderRadius: BorderRadius.circular(12), boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.02), blurRadius: 4)]),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('${_selectedDate.toLocal()}'.split(' ')[0], style: const TextStyle(fontSize: 18, color: AgriShieldTheme.onSurface)),
                  const Icon(Icons.calendar_month, color: AgriShieldTheme.onSurfaceVariant),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          
          // Evidence
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: const [
              Text('Upload Evidence Photos', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
              Text('2 of 3 minimum', style: TextStyle(fontSize: 12, color: AgriShieldTheme.onSurfaceVariant)),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              for (int i = 0; i < 3; i++) ...[
                if (i < _evidenceFiles.length)
                  Expanded(
                    child: Container(
                      height: 100,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(12),
                        image: DecorationImage(image: FileImage(_evidenceFiles[i]), fit: BoxFit.cover)
                      ),
                      child: Stack(
                        children: [
                          Positioned(
                            top: 4, right: 4,
                            child: InkWell(
                              onTap: () => _removeImage(i),
                              child: Container(
                                padding: const EdgeInsets.all(4),
                                decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.8), shape: BoxShape.circle),
                                child: const Icon(Icons.close, size: 16, color: AgriShieldTheme.error),
                              ),
                            ),
                          )
                        ],
                      ),
                    ),
                  )
                else
                  Expanded(
                    child: InkWell(
                      onTap: _pickImage,
                      child: _buildAddPhotoBtn(),
                    )
                  ),
                if (i < 2) const SizedBox(width: 12),
              ]
            ],
          ),
          const SizedBox(height: 48),
          
          // Submit
          ElevatedButton(
            onPressed: _isSubmitting || _evidenceFiles.length < 2 ? null : () async {
              setState(() => _isSubmitting = true);
              
              // 1. Upload files first
              final apiClient = ApiClient();
              List<String> uploadedFileIds = [];
              
              for (var file in _evidenceFiles) {
                final uploadRes = await apiClient.uploadFile<Map<String, dynamic>>(
                  '/files', 
                  file.path, 
                  (json) => json as Map<String, dynamic>
                );
                
                if (uploadRes.success && uploadRes.data != null) {
                  uploadedFileIds.add(uploadRes.data!['id']);
                } else {
                  if (mounted && context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to upload photo: ${uploadRes.error?.message}')));
                    setState(() => _isSubmitting = false);
                  }
                  return;
                }
              }

              // 2. Submit Claim with file IDs
              final repo = ref.read(claimRepositoryProvider);
              String policyId = widget.policyId ?? '';
              
              if (policyId.isEmpty) {
                final policiesRes = await ref.read(insuranceRepositoryProvider).getPolicies();
                if (policiesRes.success && policiesRes.data != null && policiesRes.data!.isNotEmpty) {
                  policyId = policiesRes.data!.first['id']?.toString() ?? '';
                }
              }

              final selectedItem = _incidentTypes.firstWhere(
                (e) => e['name'] == _selectedIncident,
                orElse: () => {'code': 'pest'},
              );
              final eventCode = selectedItem['code'] ?? 'pest';

              final res = await repo.createClaim({
                "policy_id": policyId,
                "incident_date": _selectedDate.toIso8601String().split('T')[0],
                "event_type": eventCode,
                "description": "Crop damage claim filed via farmer mobile app",
                "evidence_ids": uploadedFileIds
              });
              
              if (mounted && context.mounted) {
                setState(() => _isSubmitting = false);
                if (res.success) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Claim submitted and AI assessed successfully!'),
                      backgroundColor: AgriShieldTheme.primary,
                      behavior: SnackBarBehavior.floating,
                    ),
                  );
                  ref.invalidate(farmsProvider);
                  if (Navigator.canPop(context)) Navigator.pop(context);
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Failed: ${res.error?.message ?? "Failed to submit claim"}'),
                      backgroundColor: AgriShieldTheme.error,
                      behavior: SnackBarBehavior.floating,
                    ),
                  );
                }
              }
            },
            style: ElevatedButton.styleFrom(minimumSize: const Size.fromHeight(56), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30))),
            child: _isSubmitting
              ? const CircularProgressIndicator(color: Colors.white)
              : Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: const [
                    Icon(Icons.send),
                    SizedBox(width: 8),
                    Text('Submit Claim', style: TextStyle(fontSize: 18)),
                  ],
                ),
          ),
        ],
      ),
    );
  }

  Widget _buildAddPhotoBtn() {
    return Container(
      height: 100,
      decoration: BoxDecoration(color: AgriShieldTheme.surfaceVariant.withValues(alpha: 0.5), borderRadius: BorderRadius.circular(12), border: Border.all(color: AgriShieldTheme.surfaceVariant, style: BorderStyle.solid)),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: const [
          Icon(Icons.add_a_photo, color: AgriShieldTheme.primary, size: 28),
          SizedBox(height: 4),
          Text('Add Photo', style: TextStyle(fontSize: 12, color: AgriShieldTheme.primary, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
