class StatisticalValidator:
    """A/B测试统计检验"""
    def calculate_p_value(self, control_success, control_total, 
                         variant_success, variant_total):
        """使用卡方检验计算p值"""
        control_fail = control_total - control_success
        variant_fail = variant_total - variant_success
        
        observed = np.array([[control_success, control_fail],
                            [variant_success, variant_fail]])
        chi2, p_value, _, _ = chi2_contingency(observed)
        return p_value 