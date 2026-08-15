import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../repositories/farm_repository.dart';
import '../api/api_client.dart';
import '../repositories/insurance_repository.dart';
import '../repositories/claim_repository.dart';

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

final insuranceRepositoryProvider = Provider<InsuranceRepository>((ref) {
  // Change to ApiInsuranceRepository in production
  return ApiInsuranceRepository();
});

final claimRepositoryProvider = Provider<ClaimRepository>((ref) {
  // Change to ApiClaimRepository in production
  return ApiClaimRepository();
});
