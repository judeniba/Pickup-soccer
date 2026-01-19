"""
Master Test Runner - Executes all tests and generates comprehensive report
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))


class MasterTestRunner:
    """Executes all tests and generates comprehensive report"""
    
    def __init__(self):
        self.start_time = None
        self.results = {
            "integration": {"status": "pending", "duration": 0, "details": None},
            "performance": {"status": "pending", "duration": 0, "details": None},
            "end_to_end": {"status": "pending", "duration": 0, "details": None}
        }
    
    def print_header(self):
        """Print test suite header"""
        print("\n" + "="*80)
        print("PICKUP SOCCER - MASTER TEST SUITE")
        print("="*80)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("🧪 RUNNING INTEGRATION TESTS...")
        print("-" * 80)
        
        start = time.time()
        try:
            # Import and run integration tests
            from tests.test_integration import IntegrationTest
            
            test_suite = IntegrationTest()
            success = test_suite.run_all_tests()
            test_suite.cleanup()
            
            duration = time.time() - start
            self.results["integration"]["status"] = "passed" if success else "failed"
            self.results["integration"]["duration"] = duration
            self.results["integration"]["details"] = f"{test_suite.passed_tests}/{test_suite.total_tests} tests passed"
            
            return success
            
        except Exception as e:
            duration = time.time() - start
            self.results["integration"]["status"] = "error"
            self.results["integration"]["duration"] = duration
            self.results["integration"]["details"] = str(e)
            print(f"\n❌ Integration tests failed: {e}\n")
            return False
    
    def run_performance_tests(self):
        """Run performance benchmarks"""
        print("\n⚡ RUNNING PERFORMANCE BENCHMARKS...")
        print("-" * 80)
        
        start = time.time()
        try:
            # Import and run performance tests
            from tests.test_performance import PerformanceBenchmark
            
            benchmark = PerformanceBenchmark()
            benchmark.run_all_benchmarks()
            benchmark.cleanup()
            
            duration = time.time() - start
            self.results["performance"]["status"] = "passed"
            self.results["performance"]["duration"] = duration
            self.results["performance"]["details"] = f"{len(benchmark.benchmarks)} benchmarks completed"
            
            return True
            
        except Exception as e:
            duration = time.time() - start
            self.results["performance"]["status"] = "error"
            self.results["performance"]["duration"] = duration
            self.results["performance"]["details"] = str(e)
            print(f"\n❌ Performance tests failed: {e}\n")
            return False
    
    def run_end_to_end_tests(self):
        """Run end-to-end workflow"""
        print("\n🔄 RUNNING END-TO-END WORKFLOW...")
        print("-" * 80)
        
        start = time.time()
        try:
            # Import and run end-to-end workflow
            from run_integration import EndToEndWorkflow
            
            workflow = EndToEndWorkflow(use_sample_data=True)
            success = workflow.run_complete_workflow()
            
            duration = time.time() - start
            self.results["end_to_end"]["status"] = "passed" if success else "failed"
            self.results["end_to_end"]["duration"] = duration
            self.results["end_to_end"]["details"] = "7-step workflow completed"
            
            return success
            
        except Exception as e:
            duration = time.time() - start
            self.results["end_to_end"]["status"] = "error"
            self.results["end_to_end"]["duration"] = duration
            self.results["end_to_end"]["details"] = str(e)
            print(f"\n❌ End-to-end workflow failed: {e}\n")
            return False
    
    def generate_report(self):
        """Generate final test report"""
        total_duration = sum(r["duration"] for r in self.results.values())
        
        print("\n" + "="*80)
        print("MASTER TEST SUITE REPORT")
        print("="*80)
        
        # Test results table
        print("\n📊 Test Results:")
        print("-" * 80)
        print(f"{'Test Suite':<25} {'Status':<15} {'Duration':<15} {'Details':<25}")
        print("-" * 80)
        
        for suite_name, result in self.results.items():
            status_icon = {
                "passed": "✅",
                "failed": "❌",
                "error": "⚠️",
                "pending": "⏳"
            }.get(result["status"], "❓")
            
            print(f"{suite_name.replace('_', ' ').title():<25} "
                  f"{status_icon} {result['status']:<12} "
                  f"{result['duration']:.2f}s{'':<10} "
                  f"{result['details'] or 'N/A':<25}")
        
        print("-" * 80)
        print(f"{'TOTAL':<25} {'':<15} {total_duration:.2f}s")
        print("-" * 80)
        
        # Overall status
        all_passed = all(r["status"] == "passed" for r in self.results.values())
        any_error = any(r["status"] == "error" for r in self.results.values())
        
        print("\n" + "="*80)
        if all_passed:
            print("✅ ALL TESTS PASSED!")
            print("   System is ready for deployment.")
        elif any_error:
            print("⚠️  TESTS COMPLETED WITH ERRORS")
            print("   Review error messages above.")
        else:
            print("❌ SOME TESTS FAILED")
            print("   Review failed tests above.")
        print("="*80 + "\n")
        
        return all_passed
    
    def run_all_tests(self):
        """Run complete test suite"""
        self.start_time = time.time()
        self.print_header()
        
        # Check for sample data
        sample_dir = Path("data/sample/players")
        if not sample_dir.exists():
            print("⚠️  Sample data not found. Generating...")
            try:
                import subprocess
                subprocess.run([sys.executable, "scripts/generate_data.py"], check=True)
                print("✅ Sample data generated\n")
            except Exception as e:
                print(f"❌ Failed to generate sample data: {e}")
                print("💡 Run manually: python scripts/generate_data.py\n")
                return False
        
        # Run all test suites
        integration_ok = self.run_integration_tests()
        performance_ok = self.run_performance_tests()
        e2e_ok = self.run_end_to_end_tests()
        
        # Generate final report
        all_passed = self.generate_report()
        
        return all_passed


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run master test suite")
    parser.add_argument(
        "--suite",
        choices=["all", "integration", "performance", "e2e"],
        default="all",
        help="Test suite to run"
    )
    
    args = parser.parse_args()
    
    runner = MasterTestRunner()
    
    if args.suite == "all":
        success = runner.run_all_tests()
    elif args.suite == "integration":
        runner.print_header()
        success = runner.run_integration_tests()
        print(f"\n{'✅' if success else '❌'} Integration tests {'passed' if success else 'failed'}\n")
    elif args.suite == "performance":
        runner.print_header()
        success = runner.run_performance_tests()
        print(f"\n{'✅' if success else '❌'} Performance tests {'passed' if success else 'failed'}\n")
    elif args.suite == "e2e":
        runner.print_header()
        success = runner.run_end_to_end_tests()
        print(f"\n{'✅' if success else '❌'} End-to-end workflow {'passed' if success else 'failed'}\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
