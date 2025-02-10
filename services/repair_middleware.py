async def ab_test_middleware(data_key: str, repair_func):
    """A/B测试策略分配中间件"""
    assigned_strategy = ab_test_manager.assign_strategy(data_key)
    
    # 执行分配的修复策略
    result = repair_func(data_key, assigned_strategy)
    
    # 记录测试结果
    ab_test_manager.log_result(
        data_key=data_key,
        strategy=assigned_strategy,
        success=result['success']
    )
    
    return result 