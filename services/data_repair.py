class DataRepairEngine:
    """Intelligent data repair engine"""
    
    def __init__(self):
        self.repair_strategies = {
            'single_corruption': self._repair_from_replica,
            'multi_corruption': self._repair_from_source,
            'metadata_issue': self._rebuild_metadata
        }
        
    def repair_data(self, data_key: str, issue_type: str):
        """Execute repair process"""
        strategy = self.repair_strategies.get(issue_type)
        if not strategy:
            raise ValueError(f"Unknown issue type: {issue_type}")
            
        return strategy(data_key)
        
    def _repair_from_replica(self, data_key: str):
        """Repair data from healthy replica"""
        primary_uri = data_registry[data_key]['uri']
        provider = cloud_storage.get_provider(primary_uri)
        healthy_replica = self._find_healthy_replica(data_key)
        
        # Restore data from replica
        data = healthy_replica.retrieve(data_key)
        provider.store(data, data_registry[data_key]['tier'])
        
    def _repair_from_source(self, data_key: str):
        """Rebuild from original data source"""
        raw_data = data_ingester.fetch_raw_data(data_key)
        transformed = data_processor.process(raw_data)
        cloud_storage.store(transformed, data_registry[data_key]['tier'])
        
    def _rebuild_metadata(self, data_key: str):
        """Rebuild metadata index"""
        data = cloud_storage.retrieve(data_key)
        new_metadata = metadata_extractor.generate_metadata(data)
        metadata_registry.update(data_key, new_metadata)
        
    def auto_repair(self, data_key: str):
        """Fully automated repair process"""
        analysis = verification_analyzer.generate_report(data_key)
        strategy = repair_advisor.recommend_strategy(data_key)['strategy']
        
        logger.info(f"Auto-repairing {data_key} with {strategy} strategy")
        result = self.repair_data(data_key, strategy)
        
        # Log repair results
        repair_history.log_repair(
            data_key=data_key,
            strategy=strategy,
            success=result['status'] == 'repaired'
        )
        
        if not result['success']:
            alert_manager.trigger_alert({
                "type": "repair_failed",
                "data_key": data_key,
                "strategy": strategy
            }) 