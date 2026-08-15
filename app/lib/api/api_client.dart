import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/envelope.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ApiClient {
  final String baseUrl;

  ApiClient({this.baseUrl = "http://localhost:8000/api/v1"});

  Future<Map<String, String>> _getHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  Future<Envelope<T>> get<T>(String endpoint, T Function(dynamic) fromJsonData) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl$endpoint'),
        headers: await _getHeaders(),
      );
      return _processResponse(response, fromJsonData);
    } catch (e) {
      return Envelope(success: false, error: EnvelopeError(code: 'NETWORK_ERROR', message: e.toString()));
    }
  }

  Future<Envelope<T>> post<T>(String endpoint, Map<String, dynamic> body, T Function(dynamic) fromJsonData, {Map<String, String>? extraHeaders}) async {
    try {
      final headers = await _getHeaders();
      if (extraHeaders != null) {
        headers.addAll(extraHeaders);
      }
      final response = await http.post(
        Uri.parse('$baseUrl$endpoint'),
        headers: headers,
        body: jsonEncode(body),
      );
      return _processResponse(response, fromJsonData);
    } catch (e) {
      return Envelope(success: false, error: EnvelopeError(code: 'NETWORK_ERROR', message: e.toString()));
    }
  }

  Envelope<T> _processResponse<T>(http.Response response, T Function(dynamic) fromJsonData) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      final jsonBody = jsonDecode(response.body);
      return Envelope.fromJson(jsonBody, fromJsonData);
    } else {
      try {
        final jsonBody = jsonDecode(response.body);
        return Envelope.fromJson(jsonBody, fromJsonData); // API returns envelope on error too
      } catch (_) {
        return Envelope(
          success: false,
          error: EnvelopeError(
            code: 'HTTP_${response.statusCode}',
            message: 'Failed with status ${response.statusCode}',
          )
        );
      }
    }
  }
}
