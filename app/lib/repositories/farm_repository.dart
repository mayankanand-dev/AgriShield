import '../api/api_client.dart';
import '../models/envelope.dart';

abstract class FarmRepository {
  Future<Envelope<List<Map<String, dynamic>>>> getFarms();
  Future<Envelope<Map<String, dynamic>>> createFarm(Map<String, dynamic> data);
}

class ApiFarmRepository implements FarmRepository {
  final ApiClient client;

  ApiFarmRepository(this.client);

  @override
  Future<Envelope<List<Map<String, dynamic>>>> getFarms() {
    return client.get('/farms', (data) => List<Map<String, dynamic>>.from(data));
  }

  @override
  Future<Envelope<Map<String, dynamic>>> createFarm(Map<String, dynamic> data) {
    return client.post('/farms', data, (data) => data as Map<String, dynamic>);
  }
}

class LocalMockFarmRepository implements FarmRepository {
  @override
  Future<Envelope<List<Map<String, dynamic>>>> getFarms() async {
    await Future.delayed(const Duration(seconds: 1));
    return Envelope(
      success: true,
      data: [
        {
          "id": "123",
          "name": "North Field",
          "crop": "Wheat",
          "status": "VERIFIED",
        }
      ],
    );
  }

  @override
  Future<Envelope<Map<String, dynamic>>> createFarm(Map<String, dynamic> data) async {
    await Future.delayed(const Duration(seconds: 1));
    return Envelope(
      success: true,
      data: {"farm_id": "456", "area_m2": 5000.0},
    );
  }
}
