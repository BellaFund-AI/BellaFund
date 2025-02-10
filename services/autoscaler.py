class AutoScaler:
    """Automatically scales prediction service based on load
    
    Attributes:
        min_replicas: Minimum number of service instances
        max_replicas: Maximum allowed instances
        scale_up_threshold: CPU% threshold for scaling up
        scale_down_threshold: CPU% threshold for scaling down
    """
    
    def __init__(self, 
                 min_replicas=2, 
                 max_replicas=10,
                 scale_up_threshold=80,
                 scale_down_threshold=30):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.current_replicas = min_replicas
        
    def evaluate_scaling(self, metrics: dict) -> int:
        """Determine required scaling based on metrics
        Args:
            metrics: Dictionary containing:
                - cpu_usage: Current CPU utilization %
                - memory_usage: Current memory usage %
                - request_rate: Requests per second
                - latency_p99: 99th percentile latency
        Returns:
            int: Number of replicas needed (-1 for scale down, 0 for no change)
        """
        # Scaling logic
        if metrics['cpu_usage'] > self.scale_up_threshold:
            return min(self.current_replicas * 2, self.max_replicas)
        elif metrics['cpu_usage'] < self.scale_down_threshold:
            return max(self.current_replicas // 2, self.min_replicas)
        return self.current_replicas
    
    def apply_scaling(self, desired_replicas: int) -> None:
        """Execute scaling operation through orchestrator API"""
        if desired_replicas != self.current_replicas:
            print(f"Scaling from {self.current_replicas} to {desired_replicas} replicas")
            # Implementation to call Kubernetes API or cloud provider
            self.current_replicas = desired_replicas 

    def calculate_desired_replicas_v2(self, metrics: dict) -> int:
        """Enhanced scaling algorithm considering multiple factors"""
        # Weighted combination of metrics
        cpu_weight = 0.4
        latency_weight = 0.3
        request_weight = 0.3
        
        # Normalize metrics
        cpu_factor = metrics['cpu_usage'] / 100
        latency_factor = min(metrics['latency_p95'] / 1000, 1)  # Assuming 1s max
        request_factor = metrics['request_rate'] / 1000  # Assuming 1000 RPS max
        
        # Calculate composite score
        score = (cpu_weight * cpu_factor + 
                latency_weight * latency_factor +
                request_weight * request_factor)
        
        # Determine scaling based on score
        if score > 0.8:
            return min(self.current_replicas * 2, self.max_replicas)
        elif score < 0.3:
            return max(self.current_replicas // 2, self.min_replicas)
        return self.current_replicas 