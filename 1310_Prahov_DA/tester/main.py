import sys
from log_filter import log_filter
from tests import IntegrationTests
from tests import StaticAnalys
from tests import CodeStyle

if __name__ == "__main__":
    log_filter.info("Run tests")
    
    try:
        code_style = CodeStyle()
        code_style.run_test()
        static_analys = StaticAnalys()
        static_analys.run_test()
        integration = IntegrationTests()
        integration.run_all_tests()
        log_filter.info("Integration test complit")
        if not integration.isSuccessful:
            sys.exit(1)
            
    except Exception as e:
        log_filter.error(f"Error: {e}")
        sys.exit(1)