"""Risk scoring inference — loads trained RandomForest pipeline."""
import os, json, time
import joblib
import numpy as np
import pandas as pd
from app import config

_pipeline = None
_metadata = None


def _generate_fallback_metadata(model_path: str, pipeline) -> dict:
    """Auto-generate metadata.json from the loaded pipeline if file is missing."""
    meta = {
        "model": "risk_score",
        "version": "risk-v1.0.0",
        "algorithm": "RandomForestRegressor",
        "target": "risk_score",
        "features": list(pipeline.feature_names_in_) if hasattr(pipeline, "feature_names_in_") else [
            "crop", "area_ha", "rainfall", "temp_mean", "humidity",
            "soil_ph", "nitrogen", "phosphorus", "potassium",
            "ndvi_mean", "ndwi_mean", "ndmi_mean",
            "yield_prediction", "disease_probability", "historical_loss",
        ],
    }
    meta_path = os.path.join(os.path.dirname(model_path), "metadata.json")
    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4)
    except Exception:
        pass
    return meta


def _load():
    global _pipeline, _metadata
    if _pipeline is None:
        _pipeline = joblib.load(config.RISK_MODEL)
        meta_path = os.path.join(os.path.dirname(config.RISK_MODEL), "metadata.json")
        if os.path.exists(meta_path):
            with open(meta_path, encoding="utf-8") as f:
                _metadata = json.load(f)
        else:
            _metadata = _generate_fallback_metadata(config.RISK_MODEL, _pipeline)


def _risk_band(score: float) -> str:
    if score < 0.25:
        return "low"
    if score < 0.5:
        return "medium"
    if score < 0.75:
        return "high"
    return "critical"


def _derive_factors(features: dict, score: float) -> list:
    """Return top contributing risk factors based on feature thresholds."""
    factors = []
    if features.get("rainfall", 0) > 200:
        factors.append({"name": "Excess rainfall", "contribution": 0.25})
    if features.get("ndvi_mean", 0.5) < 0.3:
        factors.append({"name": "Low vegetation index", "contribution": 0.20})
    if features.get("disease_probability", 0) > 0.4:
        factors.append({"name": "Disease pressure", "contribution": 0.30})
    if features.get("historical_loss", 0) > 0.3:
        factors.append({"name": "Historical loss", "contribution": 0.25})
    if features.get("temp_mean", 25) > 38:
        factors.append({"name": "Heat stress", "contribution": 0.15})
    return factors


def score_risk(features: dict) -> dict:
    """
    Score farm risk from a feature dict.
    Any missing column defaults to 0.
    Returns: {risk_score, risk_band, factors, confidence, model_version, low_confidence, inference_ms}
    """
    _load()
    all_cols = _metadata["features"]
    row = {col: features.get(col, 0) for col in all_cols}
    df = pd.DataFrame([row])

    t0 = time.time()
    score = float(_pipeline.predict(df)[0])
    score = max(0.0, min(1.0, score))
    elapsed_ms = int((time.time() - t0) * 1000)

    # Confidence from inter-tree variance
    preprocessor = _pipeline.named_steps["preprocessor"]
    X_transformed = preprocessor.transform(df)
    estimators = _pipeline.named_steps["model"].estimators_
    tree_preds = np.array([e.predict(X_transformed)[0] for e in estimators])
    cv = tree_preds.std() / (tree_preds.mean() + 1e-9)
    confidence = float(max(0.0, min(1.0, 1.0 - cv)))

    return {
        "risk_score": round(score, 3),
        "risk_band": _risk_band(score),
        "factors": _derive_factors(features, score),
        "confidence": round(confidence, 3),
        "model_version": _metadata["version"],
        "low_confidence": confidence < config.MIN_CONFIDENCE,
        "inference_ms": elapsed_ms,
    }
