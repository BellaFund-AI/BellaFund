from scipy.stats import chi2_contingency
from collections import defaultdict
from services.data_backup import AsyncBackupClient
import asyncio
from cryptography.fernet import Fernet
from prometheus_client import Counter, Gauge

class RepairABTestManager:
    """修复策略A/B测试框架"""
    
    def __init__(self, strategies: list):
        self.active_tests = {}
        self.strategy_pool = strategies
        self.metrics_collector = ABTestMetricsCollector()
        
    def start_test(self, test_name: str, variants: list, traffic_split: dict):
        """启动新的A/B测试"""
        if sum(traffic_split.values()) != 1.0:
            raise ValueError("Traffic split must sum to 1.0")
            
        self.active_tests[test_name] = {
            'variants': variants,
            'traffic_split': traffic_split,
            'assignments': {},
            'start_time': datetime.now()
        }
        
    def assign_strategy(self, data_key: str) -> str:
        """为数据分配修复策略"""
        for test_name, config in self.active_tests.items():
            if data_key not in config['assignments']:
                # 根据流量分配策略
                rand = np.random.random()
                cumulative = 0
                for variant, ratio in config['traffic_split'].items():
                    cumulative += ratio
                    if rand <= cumulative:
                        config['assignments'][data_key] = variant
                        return variant
        return 'default'
    
    def log_result(self, data_key: str, strategy: str, success: bool):
        """记录A/B测试结果"""
        for test in self.active_tests.values():
            if data_key in test['assignments']:
                self.metrics_collector.log_metric(
                    test_id=test['test_name'],
                    variant=strategy,
                    success=success
                )
                
    def get_test_results(self, test_name: str) -> dict:
        """获取测试结果报告"""
        return self.metrics_collector.analyze_results(test_name)

    def detect_winner(self, test_name: str, confidence_level: float=0.95) -> dict:
        """使用统计检验确定优胜策略"""
        test_data = self.metrics_collector.get_test_data(test_name)
        baseline = test_data['control']
        variants = [k for k in test_data.keys() if k != 'control']
        
        results = {}
        for variant in variants:
            p_value = self._calculate_p_value(
                baseline['successes'], baseline['trials'],
                test_data[variant]['successes'], test_data[variant]['trials']
            )
            results[variant] = {
                'lift': (test_data[variant]['rate'] - baseline['rate']) / baseline['rate'],
                'p_value': p_value,
                'significant': p_value < (1 - confidence_level)
            }
        
        return sorted(results.items(), key=lambda x: -x[1]['lift'])

    def _calculate_p_value(self, control_success, control_total, variant_success, variant_total):
        validator = StatisticalValidator()
        return validator.calculate_p_value(
            control_success, control_total,
            variant_success, variant_total
        )

class AdaptiveTrafficManager:
    """Dynamic traffic allocation based on real-time performance"""
    def adjust_traffic(self, test_name: str):
        current_split = self.active_tests[test_name]['traffic_split']
        performance = self.metrics_collector.get_performance(test_name)
        
        # Adjust traffic using multi-armed bandit algorithm
        total_trials = sum(v['trials'] for v in performance.values())
        new_split = {
            variant: (v['successes'] + 1) / (total_trials + len(performance))
            for variant, v in performance.items()
        }
        
        # 归一化分配比例
        total = sum(new_split.values())
        self.active_tests[test_name]['traffic_split'] = {
            k: v/total for k, v in new_split.items()
        } 

class ABTestMetricsCollector:
    """A/B测试指标收集器"""
    def __init__(self):
        self.test_metrics = defaultdict(lambda: defaultdict(
            lambda: {'successes': 0, 'trials': 0}
        ))
        self.backup_client = AsyncBackupClient()
        self.cipher = Fernet(config.ENCRYPTION_KEY)
        self.metrics = {
            'log_errors': Counter('abtest_log_errors', 'Metric logging errors'),
            'active_tests': Gauge('abtest_active_tests', 'Number of active tests')
        }
    
    def log_metric(self, test_id: str, variant: str, success: bool):
        try:
            # 加密敏感字段
            encrypted_test_id = self.cipher.encrypt(test_id.encode())
            encrypted_variant = self.cipher.encrypt(variant.encode())
            # 存储加密后的数据...
            self.test_metrics[test_id][variant]['trials'] += 1
            if success:
                self.test_metrics[test_id][variant]['successes'] += 1
            # 异步备份数据
            asyncio.create_task(
                self.backup_client.backup_metric(
                    test_id, variant, success
                )
            )
        except Exception as e:
            self.metrics['log_errors'].inc()
            logger.error(f"Metric logging failed: {str(e)}")
    
    def analyze_results(self, test_id: str) -> dict:
        results = {}
        for variant, metrics in self.test_metrics[test_id].items():
            results[variant] = {
                'success_rate': metrics['successes'] / metrics['trials'],
                'total_trials': metrics['trials']
            }
        return results 