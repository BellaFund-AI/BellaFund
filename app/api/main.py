"""
Investment Analytics API Endpoints
Provides interfaces for AI scoring and market monitoring
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from models import TokenScoreRequest
from typing import Dict, Optional, List
from .security import limiter, verify_api_key
from streaming.data_processor import StreamProcessor
import asyncio
from trading.strategy_engine import TradingEngine
from services.model_explainer import ScoreExplainer
from services.alert_manager import AlertManager
from pydantic import BaseModel
from services.root_cause_analyzer import RootCauseAnalyzer
from services.alert_repository import AlertRepository
from services.workflow_engine import WorkflowEngine
from services.alert_correlator import AlertCorrelator
from services.feature_history import FeatureHistory
from services.performance_tracker import PerformanceTracker
import pandas as pd
from fastapi import WebSocket
from services.autoscaler import AutoScaler
from services.resource_monitor import ResourceMonitor
from services.tracing import TracingCollector
from fastapi import Request
from services.tracing import tracer
import numpy as np
from services.auto_rollback import TraceAwareRollback
from services.feature_guard import FeatureGuard
from services.tracing_storage import TraceCompressor
from services.lifecycle_manager import LifecyclePolicy
from services.cost_analyzer import StorageCostAnalyzer
from services.adaptive_policy import AdaptivePolicyEngine
from services.trace_archiver import TraceArchiver
from services.access_analyzer import AccessPatternAnalyzer
from services.storage_optimizer import StorageOptimizer
from services.cache_monitor import CacheMonitor
from services.cache_trainer import CacheTrainer
from services.cache import Cache
from services.cloud_storage import MultiCloudStorage
from services.storage_tier_optimizer import StorageTierOptimizer
from services.data_verifier import DataConsistencyVerifier
from services.verification_queue import VerificationQueue
from services.data_repair import DataRepairEngine
from services.repair_advisor import RepairAdvisor
from services.repair_explainer import RepairExplainer
from services.ab_testing import ABTestManager
from datetime import datetime

app = FastAPI(
    title="BellaFund API",
    description="AI-powered Investment Analytics Service",
    version="0.1.0"
)

@app.post("/score", response_model=Dict[str, float], tags=["Scoring"])
@limiter.limit("10/minute")
async def get_token_score(request: TokenScoreRequest):
    """Evaluate token investment potential
    Args:
        request: Token metadata and market indicators
    Returns:
        JSON: Normalized score and factor breakdown
    Raises:
        HTTPException: For invalid input data
    """
    try:
        result = ai_scorer.predict_score(request.token_data)
        # Log performance metrics
        ai_scorer.performance_monitor.log_performance(
            y_true=[request.token_data['actual_roi']],  # From subsequent data
            y_pred=[result['score']],
            features=request.token_data
        )
        # Check for auto-rollback
        if ai_scorer.auto_rollback():
            logger.warning("Model rolled back to previous version")
            
        return result
    except InvalidInputError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/whale/{token_address}", tags=["Monitoring"])
async def get_whale_activity(token_address: str):
    """Track large holder transactions
    Args:
        token_address: Blockchain address of the token
    Returns:
        List: Recent whale transactions with metadata
    """
    return chain_analyzer.detect_whale_activity(token_address)

@app.on_event("startup")
async def load_models():
    """Initialize AI models on server startup"""
    global ai_scorer
    ai_scorer = TokenScorer(model_path='models/production_model.pkl')

@app.on_event("startup")
async def start_stream_processor():
    """Initialize real-time data processing"""
    global processor
    processor = StreamProcessor(bootstrap_servers='kafka:9092')
    asyncio.create_task(processor.start_processing(ai_scorer))

@app.get("/realtime/{symbol}", tags=["Market Data"])
async def get_realtime_data(symbol: str):
    """Get latest processed market data"""
    return {
        "symbol": symbol,
        "metrics": processor.get_latest_metrics(symbol)
    }

@app.post("/rebalance", tags=["Trading"])
@limiter.limit("1/minute")
async def trigger_rebalance(api_key: str = Depends(verify_api_key)):
    """Execute portfolio rebalancing strategy"""
    portfolio = get_current_holdings()
    scores = ai_scorer.get_latest_scores()
    return TradingEngine().execute_strategy(portfolio, scores)

explainer = ScoreExplainer(ai_scorer.model)

@app.post("/explain", tags=["Analysis"])
async def explain_score(request: TokenScoreRequest):
    """Explain model's scoring decision"""
    try:
        explanation = explainer.explain_prediction(request.token_data)
        return {
            **ai_scorer.predict_score(request.token_data),
            "explanation": explanation
        }
    except Exception as e:
        raise HTTPException(500, detail=f"Explanation failed: {str(e)}")

alert_manager = AlertManager()

@app.post("/alert", tags=["Monitoring"])
async def trigger_manual_alert(alert: dict):
    """Simulate alert triggering for testing"""
    alert_manager.trigger_alert(alert)
    return {"status": "alert_sent"}

class AlertAckRequest(BaseModel):
    alert_id: str
    silence_duration: Optional[int] = 3600  # 默认静音1小时

@app.post("/alerts/acknowledge", tags=["Monitoring"])
async def acknowledge_alert(request: AlertAckRequest):
    """Acknowledge alert and silence for duration"""
    alert_manager.acknowledge_alert(request.alert_id, request.silence_duration)
    return {"status": "acknowledged"}

@app.post("/alerts/silence", tags=["Monitoring"])
async def silence_alert_type(alert_type: str, duration: int):
    """Silence specific alert type"""
    alert_manager.silence_alert_type(alert_type, duration)
    return {"status": f"{alert_type} alerts silenced for {duration} seconds"}

@app.post("/analyze/root-cause", tags=["Analysis"])
async def analyze_root_cause(drift_report: dict):
    """Analyze root cause of data drift"""
    analyzer = RootCauseAnalyzer(metadata_repository)
    analysis_results = analyzer.analyze_drift(drift_report)
    return {
        "root_causes": analysis_results,
        "recommended_actions": [
            "检查外部数据源连接",
            "验证数据采集管道",
            "重新训练模型"
        ]
    }

alert_repo = AlertRepository()

@app.get("/alerts/history", tags=["Monitoring"])
async def get_alert_history(hours: int = 24):
    """Get recent alert history"""
    return alert_repo.get_recent_alerts(hours)

@app.post("/alerts/auto-resolve", tags=["Monitoring"])
async def auto_resolve_alert_type(alert_type: str):
    """Trigger automated resolution workflow"""
    workflow_engine.process_alert({'type': alert_type})
    return {"status": f"{alert_type} resolution initiated"}

@app.get("/alerts/stats", tags=["Monitoring"])
async def get_alert_stats():
    """Get alert statistics"""
    return {
        "total_last_24h": alert_repo.get_alert_count(hours=24),
        "by_severity": alert_repo.get_severity_distribution(),
        "resolution_rate": alert_repo.get_resolution_rate(),
        "common_types": alert_repo.get_common_alert_types()
    }

correlator = AlertCorrelator()

@app.get("/alerts/related/{alert_id}", tags=["Analysis"])
async def get_related_alerts(alert_id: str):
    """Get related alert events"""
    try:
        return correlator.find_related_alerts(alert_id)
    except Exception as e:
        raise HTTPException(500, detail=f"关联分析失败: {str(e)}")

@app.get("/models/versions", tags=["Model Management"])
async def get_model_versions():
    """Get all model version metadata"""
    return {
        "current_version": ai_scorer.current_version,
        "versions": ai_scorer.model_versions
    }

@app.get("/features/importance", tags=["Analysis"])
async def get_feature_importance_history(feature: str, days: int = 30):
    """Get feature importance history trend"""
    return feature_history.get_trend(feature, days).to_dict(orient='records')

@app.get("/models/compare", tags=["Analysis"])
async def compare_model_versions(
    version1: str = Query(..., description="Base model version"),
    version2: str = Query(..., description="Comparison model version")
):
    """Compare two model versions across multiple dimensions"""
    try:
        return ai_scorer.compare_versions(version1, version2)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/models/rollback/{version}", tags=["Model Management"])
async def rollback_model_version(version: str):
    """Roll back to specified model version
    Args:
        version: Target version identifier
    Returns:
        dict: Rollback confirmation with new active version
    """
    try:
        ai_scorer.rollback_to_version(version)
        return {
            "status": "success",
            "current_version": ai_scorer.current_version
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

performance_tracker = PerformanceTracker()

@app.get("/models/metrics", tags=["Monitoring"])
async def get_performance_metrics(
    version: str = Query(None, description="Filter by model version"),
    days: int = Query(30, description="Time window in days"),
    metrics: str = Query("accuracy,precision,recall", description="Comma-separated list of metrics")
):
    """Get historical performance metrics with filtering"""
    try:
        df = performance_tracker.get_metrics(
            version=version,
            window=pd.Timedelta(days=days)
        )
        return df[['timestamp', 'version'] + metrics.split(',')].to_dict(orient='records')
    except KeyError as e:
        raise HTTPException(400, detail=f"Invalid metric requested: {str(e)}")

@app.get("/models/benchmarks", tags=["Analysis"])
async def get_performance_benchmarks():
    """Get target performance benchmarks"""
    return {
        "benchmarks": performance_tracker.baselines,
        "current_values": performance_tracker.get_metrics().iloc[-1].to_dict()
    }

@app.post("/models/benchmark", tags=["Analysis"])
async def run_benchmark(
    version: str = Query(..., description="Model version to test"),
    dataset: str = Query("validation", description="Test dataset to use")
):
    """Execute comprehensive model benchmark"""
    benchmark_results = ai_scorer.run_benchmark(
        version=version,
        dataset=dataset
    )
    return {
        "version": version,
        "dataset": dataset,
        **benchmark_results
    }

@app.post("/models/monitoring", tags=["Monitoring"])
async def check_performance_health():
    """Execute comprehensive performance health check"""
    results = {
        'anomalies': performance_tracker.detect_anomalies(ai_scorer.current_version),
        'benchmark_gaps': performance_tracker.calculate_benchmark_gaps(),
        'version_comparison': ai_scorer.compare_versions(
            ai_scorer.current_version,
            ai_scorer.get_previous_version()
        )
    }
    return results

@app.websocket("/performance/stream")
async def performance_stream(websocket: WebSocket):
    """WebSocket for real-time performance metrics"""
    await websocket.accept()
    while True:
        latest = performance_tracker.get_metrics(window=pd.Timedelta(minutes=1))
        await websocket.send_json(latest.to_dict(orient='records'))
        await asyncio.sleep(5)  # Update every 5 seconds

@app.post("/autoscale", tags=["Infrastructure"])
async def trigger_autoscale(api_key: str = Depends(verify_api_key)):
    """Execute autoscaling evaluation and action"""
    metrics = resource_monitor.collect_metrics()
    desired = autoscaler.evaluate_scaling(metrics)
    autoscaler.apply_scaling(desired)
    return {
        "action": "scaling",
        "from": autoscaler.current_replicas,
        "to": desired,
        "metrics": metrics
    }

@app.get("/system/metrics", tags=["Monitoring"])
async def get_system_metrics(hours: int = 1):
    """Get historical system metrics"""
    return resource_monitor.metrics_history.tail(
        int(hours * 60)  # Assuming 1 minute intervals
    ).to_dict(orient='records')

@app.get("/tracing/traces", tags=["Observability"])
async def get_recent_traces(limit: int = 100):
    """Get recent traces with basic info"""
    traces = tracing_collector.query_traces()
    return [{
        "trace_id": t['trace_id'],
        "root_span": t,
        "duration": t['duration'],
        "start_time": t['start_time']
    } for t in traces[-limit:]]

@app.get("/tracing/trace/{trace_id}", tags=["Observability"])
async def get_full_trace(trace_id: str):
    """Get complete trace hierarchy"""
    return tracing_collector.get_trace_tree(trace_id)

@app.get("/tracing/model/{version}", tags=["Analysis"])
async def analyze_model_traces(
    version: str,
    min_confidence: float = 0.7,
    days: int = 7
):
    """Analyze specific model traces"""
    traces = tracing_collector.query_traces({
        "tags": {"model_version": version},
        "min_duration": 0.5  # Analyze only requests longer than 500ms
    })
    
    analysis = {
        "performance_stats": calculate_performance_stats(traces),
        "common_errors": detect_error_patterns(traces),
        "feature_correlations": find_feature_impact(traces)
    }
    
    return analysis

def find_feature_impact(traces: list) -> dict:
    """Identify feature impact on predictions"""
    features = {}
    for trace in traces:
        if 'prediction_value' in trace['tags']:
            for key in trace['tags']:
                if key.startswith('feature_'):
                    feature = key[8:]
                    value = trace['tags'][key]
                    prediction = float(trace['tags']['prediction_value'])
                    
                    if feature not in features:
                        features[feature] = {
                            'values': [],
                            'predictions': []
                        }
                    features[feature]['values'].append(float(value))
                    features[feature]['predictions'].append(prediction)
    
    # Calculate correlation
    return {
        feat: np.corrcoef(data['values'], data['predictions'])[0,1]
        for feat, data in features.items()
    }

@app.middleware("http")
async def security_tracing(request: Request, call_next):
    """Record security-related events"""
    with tracer.start_span("security_check") as span:
        tracer.add_tag("endpoint", request.url.path)
        tracer.add_tag("user", request.state.user.id if hasattr(request.state, 'user') else 'anonymous')
        
        # Execute authentication
        try:
            auth_result = await authenticate_request(request)
            tracer.add_tag("auth_status", auth_result.status)
        except Exception as e:
            tracer.add_tag("auth_error", str(e))
            raise
        
        response = await call_next(request)
        
        # Record sensitive operations
        if request.url.path in SENSITIVE_ENDPOINTS:
            tracer.add_tag("sensitive_operation", True)
            tracer.add_tag("result_hash", hash_response(response.body))
            
    return response

@app.post("/auto-rollback", tags=["Maintenance"])
async def trigger_auto_rollback(api_key: str = Depends(verify_api_key)):
    """Perform automatic rollback check"""
    if auto_rollback.check_conditions():
        result = auto_rollback.execute()
        return {"action": "rollback", "success": result}
    return {"action": "none"}

@app.get("/feature-stats", tags=["Analysis"])
async def get_feature_statistics(feature: str = None):
    """Get feature statistics"""
    return {
        feature: feature_guard.feature_stats[feature]
        if feature else feature_guard.feature_stats
    }

trace_compressor = TraceCompressor()

@app.get("/tracing/storage/stats", tags=["Storage"])
async def get_storage_stats():
    """Get tracing storage statistics"""
    return {
        "memory_traces": len(trace_compressor.in_memory),
        "compressed_batches": len(trace_compressor.compressed_data),
        "estimated_size": sum(len(b) for b in trace_compressor.compressed_data)
    }

@app.get("/storage/cost", tags=["Storage"])
async def get_storage_cost_analysis():
    """Get storage cost analysis"""
    return cost_analyzer.calculate_daily_cost()

@app.post("/lifecycle/apply", tags=["Storage"])
async def apply_lifecycle_policies():
    """Apply data lifecycle policies"""
    lifecycle_manager.apply_policies()
    return {"status": "policies_applied"}

@app.post("/policies/optimize", tags=["Storage"])
async def optimize_policies():
    """Perform automatic policy optimization"""
    policy_engine.optimize_policies()
    return {"status": "optimization_completed"}

@app.get("/policies/current", tags=["Storage"])
async def get_current_policies():
    """Get current storage policies"""
    return {
        "hot_data_days": lifecycle_manager.policies['hot']['max_age'],
        "archive_frequency": trace_archiver.archive_frequency
    }

@app.get("/storage/hotspots", tags=["Analysis"])
async def get_data_hotspots(top_n: int = 10):
    """Get data hotspot rankings"""
    return access_analyzer.get_hot_data(top_n)

@app.post("/storage/optimize", tags=["Storage"])
async def trigger_optimization():
    """Execute storage optimization"""
    storage_optimizer.optimize_placement()
    return {"status": "optimization_completed"}

@app.get("/cache/metrics", tags=["Monitoring"])
async def get_cache_metrics():
    """Get cache performance metrics"""
    return {
        **cache_monitor.get_realtime_metrics(),
        "epsilon": cache.agent.epsilon,
        "memory_size": len(cache.agent.memory)
    }

@app.post("/cache/retrain", tags=["Maintenance"])
async def retrain_cache_model():
    """Manually trigger cache model retraining"""
    cache_trainer.train_batch()
    return {"status": "training_completed"}

@app.get("/storage/providers", tags=["Storage"])
async def get_storage_providers():
    """Get storage provider status"""
    return {
        "active": [p.name for p in cloud_storage.active_providers],
        "all": [p.config for p in cloud_storage.providers]
    }

@app.post("/storage/migrate/{data_key}", tags=["Storage"])
async def migrate_data(data_key: str, target_tier: str):
    """Manual data migration trigger"""
    optimizer = StorageTierOptimizer(cloud_storage)
    optimizer._migrate_data(data_key, 
                          data_registry[data_key]['tier'],
                          target_tier)
    return {"status": "migration_scheduled"}

@app.post("/verify/{data_key}", tags=["Storage"])
async def verify_data_integrity(data_key: str):
    """Manual data verification trigger"""
    result = verifier.verify_integrity(data_key)
    return {"data_key": data_key, "consistent": result}

@app.get("/quarantine", tags=["Storage"])
async def get_quarantined_data():
    """List quarantined data"""
    return {
        "quarantined": [
            k for k, v in data_registry.items() 
            if v.get('status') == 'quarantined'
        ]
    }

@app.get("/verification/queue", tags=["Storage"])
async def get_verification_queue():
    """Check verification queue status"""
    return {
        "pending": verification_queue.queue.qsize(),
        "recent_results": verification_queue.results
    }

@app.post("/verification/repair/{data_key}", tags=["Storage"])
async def trigger_repair(data_key: str, strategy: str):
    """Manual data repair trigger"""
    repair_engine.repair_data(data_key, strategy)
    return {"status": "repair_initiated"}

@app.post("/repair/auto/{data_key}", tags=["Storage"])
async def trigger_auto_repair(data_key: str):
    """Trigger fully automated repair"""
    repair_engine.auto_repair(data_key)
    return {"status": "auto_repair_initiated"}

@app.get("/repair/recommend/{data_key}", tags=["Storage"])
async def get_repair_recommendation(data_key: str):
    """Get repair strategy recommendations"""
    return repair_advisor.recommend_strategy(data_key)

@app.post("/repair/feedback", tags=["Storage"])
async def submit_repair_feedback(feedback: dict):
    """Submit repair result feedback"""
    repair_advisor.log_feedback(
        feedback['data_key'],
        feedback['strategy'],
        feedback['success']
    )
    return {"status": "feedback_logged"}

@app.post("/abtest/start", tags=["Experimentation"])
async def start_ab_test(test_config: ABTestConfig):
    """Start new A/B test"""
    ab_test_manager.start_test(
        test_config.name,
        test_config.variants,
        test_config.traffic_split
    )
    return {"status": "test_started"}

@app.get("/abtest/results/{test_name}", tags=["Experimentation"])
async def get_ab_test_results(test_name: str):
    """Get A/B test results"""
    return ab_test_manager.get_test_results(test_name)

@app.post("/abtest/conclude/{test_name}", tags=["Experimentation"])
async def conclude_ab_test(test_name: str):
    """Conclude test and determine winning strategy"""
    winner = ab_test_manager.detect_winner(test_name)
    return {
        "status": "test_concluded",
        "winner": winner[0] if winner else None,
        "analysis": winner
    }

@app.post("/abtest/adjust/{test_name}", tags=["Experimentation"])
async def adjust_ab_test(test_name: str):
    """Dynamically adjust test traffic distribution"""
    traffic_manager.adjust_traffic(test_name)
    return {"status": "traffic_adjusted"}

@app.get("/abtest/active", tags=["Experimentation"])
async def get_active_tests():
    """Get active A/B tests"""
    return [{
        "name": name,
        "variants": config['variants'],
        "traffic_split": config['traffic_split'],
        "duration": (datetime.now() - config['start_time']).total_seconds()
    } for name, config in ab_test_manager.active_tests.items()]

class ABTestConfig(BaseModel):
    name: str
    variants: List[str]
    traffic_split: Dict[str, float]