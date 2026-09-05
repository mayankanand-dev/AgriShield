import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../theme.dart';
import '../../api/api_client.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final ApiClient _apiClient = ApiClient();
  final _storage = const FlutterSecureStorage();
  
  bool _isLoading = true;
  bool _isEditing = false;
  bool _isSaving = false;
  Map<String, dynamic>? _user;
  final TextEditingController _nameController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchProfile();
  }

  Future<void> _fetchProfile() async {
    final response = await _apiClient.get<Map<String, dynamic>>(
      '/auth/me',
      (json) => json as Map<String, dynamic>,
    );

    if (mounted) {
      setState(() {
        _isLoading = false;
        if (response.success && response.data != null) {
          _user = response.data;
          _nameController.text = _user?['name'] ?? '';
        }
      });
    }
  }

  Future<void> _saveProfile() async {
    setState(() => _isSaving = true);
    final response = await _apiClient.patch<Map<String, dynamic>>(
      '/auth/me',
      {'name': _nameController.text},
      (json) => json as Map<String, dynamic>,
    );

    if (mounted) {
      setState(() {
        _isSaving = false;
        _isEditing = false;
        if (response.success && response.data != null) {
          _user?['name'] = response.data!['name'];
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Profile updated successfully')));
        } else {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to update: ${response.error?.message}')));
        }
      });
    }
  }

  Future<void> _logout() async {
    await _storage.delete(key: 'access_token');
    if (mounted) {
      Navigator.of(context).pushReplacementNamed('/');
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
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
              title: const Text('Profile', style: TextStyle(color: AgriShieldTheme.onSurface, fontWeight: FontWeight.w600, fontSize: 20)),
              actions: [
                if (_isEditing)
                  IconButton(
                    icon: _isSaving 
                        ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: AgriShieldTheme.primary))
                        : const Icon(Icons.check, color: AgriShieldTheme.primary),
                    onPressed: _isSaving ? null : _saveProfile,
                  )
                else
                  IconButton(
                    icon: const Icon(Icons.edit, color: AgriShieldTheme.onSurfaceVariant),
                    onPressed: () => setState(() => _isEditing = true),
                  ),
                IconButton(
                  icon: const Icon(Icons.logout, color: AgriShieldTheme.error),
                  onPressed: _logout,
                )
              ],
            ),
          ),
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _user == null
              ? const Center(child: Text("Failed to load profile."))
              : ListView(
                  padding: EdgeInsets.only(
                    top: MediaQuery.of(context).padding.top + 76,
                    left: 16, right: 16, bottom: 100,
                  ),
                  children: [
                    Center(
                      child: CircleAvatar(
                        radius: 48,
                        backgroundColor: AgriShieldTheme.primaryContainer,
                        child: Text(
                          (_user?['name']?.toString().substring(0, 1) ?? 'U').toUpperCase(),
                          style: const TextStyle(fontSize: 32, color: Colors.white, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),
                    if (_isEditing)
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 32),
                        child: TextFormField(
                          controller: _nameController,
                          decoration: InputDecoration(
                            labelText: 'Full Name',
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          textAlign: TextAlign.center,
                        ),
                      )
                    else
                      Center(
                        child: Text(
                          _user?['name'] ?? 'Unknown User',
                          style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface),
                        ),
                      ),
                    const SizedBox(height: 8),
                    Center(
                      child: Text(
                        _user?['phone'] ?? '',
                        style: const TextStyle(fontSize: 16, color: AgriShieldTheme.onSurfaceVariant),
                      ),
                    ),
                    const SizedBox(height: 32),
                    _buildInfoCard("Role", _user?['role'] ?? 'FARMER'),
                    const SizedBox(height: 16),
                    _buildInfoCard("Account Status", _user?['is_active'] == true ? 'Active' : 'Inactive'),
                  ],
                ),
    );
  }

  Widget _buildInfoCard(String title, String value) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AgriShieldTheme.surfaceVariant.withValues(alpha: 0.3),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AgriShieldTheme.onSurface)),
          Text(value, style: const TextStyle(fontSize: 16, color: AgriShieldTheme.onSurfaceVariant)),
        ],
      ),
    );
  }
}
