class EnvelopeError {
  final String code;
  final String message;
  final Map<String, dynamic>? details;

  EnvelopeError({required this.code, required this.message, this.details});

  factory EnvelopeError.fromJson(Map<String, dynamic> json) {
    return EnvelopeError(
      code: json['code'] ?? 'UNKNOWN',
      message: json['message'] ?? 'Unknown error',
      details: json['details'] as Map<String, dynamic>?,
    );
  }
}

class Envelope<T> {
  final bool success;
  final T? data;
  final EnvelopeError? error;

  Envelope({required this.success, this.data, this.error});

  factory Envelope.fromJson(Map<String, dynamic> json, T Function(dynamic) fromJsonData) {
    return Envelope(
      success: json['success'] ?? false,
      data: json['success'] == true && json['data'] != null ? fromJsonData(json['data']) : null,
      error: json['error'] != null ? EnvelopeError.fromJson(json['error']) : null,
    );
  }
}
