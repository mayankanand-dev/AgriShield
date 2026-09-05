import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../repositories/farm_repository.dart';
import '../api/api_client.dart';
import '../repositories/insurance_repository.dart';
import '../repositories/claim_repository.dart';

// Global state for bottom navigation index
final bottomNavIndexProvider = StateProvider<int>((ref) => 0);

// Change to ApiFarmRepository in production
final farmRepositoryProvider = Provider<FarmRepository>((ref) {
  return ApiFarmRepository(ApiClient());
});

final farmsProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final repo = ref.watch(farmRepositoryProvider);
  final response = await repo.getFarms();
  if (response.success && response.data != null) {
    return response.data!;
  } else {
    throw Exception(response.error?.message ?? "Failed to load farms");
  }
});

final userProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final client = ApiClient();
  final response = await client.get<Map<String, dynamic>>('/auth/me', (json) => json as Map<String, dynamic>);
  if (response.success && response.data != null) {
    return response.data!;
  } else {
    throw Exception(response.error?.message ?? "Failed to load profile");
  }
});

final weatherProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final client = ApiClient();
  // We use a default lat/lon for the dashboard general weather. 
  // In a real app, this might come from device location or the first farm.
  final response = await client.get<Map<String, dynamic>>('/weather?lat=28.6139&lon=77.2090', (json) => json as Map<String, dynamic>);
  if (response.success && response.data != null) {
    return response.data!;
  } else {
    throw Exception(response.error?.message ?? "Failed to load weather");
  }
});

final insuranceRepositoryProvider = Provider<InsuranceRepository>((ref) {
  // Change to ApiInsuranceRepository in production
  return ApiInsuranceRepository();
});

final claimRepositoryProvider = Provider<ClaimRepository>((ref) {
  // Change to ApiClaimRepository in production
  return ApiClaimRepository();
});
