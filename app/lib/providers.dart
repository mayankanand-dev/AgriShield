import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../repositories/farm_repository.dart';
import '../api/api_client.dart';

// Change to ApiFarmRepository in production
final farmRepositoryProvider = Provider<FarmRepository>((ref) {
  return LocalMockFarmRepository();
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
