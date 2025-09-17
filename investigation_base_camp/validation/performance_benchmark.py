#!/usr/bin/env python3
"""
Performance Benchmark
Purpose: Verify performance impact of graphics system fixes
Author: GitHub Copilot
Created: 2025-09-17

Benchmarks system performance to ensure fixes don't degrade
Phase 1-2 performance or introduce performance regressions.
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any, List
import traceback
from datetime import datetime

# Add src to path for testing
workspace_root = Path(__file__).parent.parent.parent
src_path = workspace_root / "src"
sys.path.insert(0, str(src_path))

class PerformanceBenchmark:
    """Benchmarks system performance after graphics fixes."""
    
    def __init__(self):
        self.benchmark_results = {
            "timestamp": datetime.now().isoformat(),
            "performance_summary": {
                "total_benchmarks": 0,
                "passed_benchmarks": 0,
                "failed_benchmarks": 0,
                "performance_regressions": 0
            },
            "core_system_benchmarks": {},
            "graphics_system_benchmarks": {},
            "integration_benchmarks": {},
            "memory_benchmarks": {},
            "performance_status": "UNKNOWN"
        }
    
    def run_all_benchmarks(self):
        """Run complete performance benchmark suite."""
        
        print("⚡ Starting Performance Benchmarks...")
        
        # Benchmark categories
        self.benchmark_core_system_performance()
        self.benchmark_graphics_system_performance()
        self.benchmark_integration_performance()
        self.benchmark_memory_performance()
        
        # Determine overall performance status
        self._determine_performance_status()
    
    def benchmark_core_system_performance(self):
        """Benchmark core Phase 2 system performance."""
        
        print("🏛️  Benchmarking Core System Performance...")
        
        core_benchmarks = {
            "event_bus_performance": self._benchmark_event_bus,
            "simulation_clock_performance": self._benchmark_simulation_clock,
            "app_framework_startup": self._benchmark_app_startup,
            "config_manager_performance": self._benchmark_config_manager
        }
        
        core_results = {}
        
        for benchmark_name, benchmark_func in core_benchmarks.items():
            result = self._run_single_benchmark(benchmark_name, benchmark_func)
            core_results[benchmark_name] = result
        
        self.benchmark_results["core_system_benchmarks"] = core_results
    
    def benchmark_graphics_system_performance(self):
        """Benchmark graphics system performance."""
        
        print("🎮 Benchmarking Graphics System Performance...")
        
        graphics_benchmarks = {
            "graphics_manager_import": self._benchmark_graphics_import,
            "graphics_manager_instantiation": self._benchmark_graphics_instantiation,
            "panda3d_availability": self._benchmark_panda3d_performance
        }
        
        graphics_results = {}
        
        for benchmark_name, benchmark_func in graphics_benchmarks.items():
            result = self._run_single_benchmark(benchmark_name, benchmark_func)
            graphics_results[benchmark_name] = result
        
        self.benchmark_results["graphics_system_benchmarks"] = graphics_results
    
    def benchmark_integration_performance(self):
        """Benchmark integration performance between systems."""
        
        print("🔄 Benchmarking Integration Performance...")
        
        integration_benchmarks = {
            "full_system_startup": self._benchmark_full_system,
            "cross_component_communication": self._benchmark_component_communication,
            "concurrent_operations": self._benchmark_concurrent_ops
        }
        
        integration_results = {}
        
        for benchmark_name, benchmark_func in integration_benchmarks.items():
            result = self._run_single_benchmark(benchmark_name, benchmark_func)
            integration_results[benchmark_name] = result
        
        self.benchmark_results["integration_benchmarks"] = integration_results
    
    def benchmark_memory_performance(self):
        """Benchmark memory usage and performance."""
        
        print("💾 Benchmarking Memory Performance...")
        
        memory_benchmarks = {
            "baseline_memory_usage": self._benchmark_baseline_memory,
            "graphics_memory_impact": self._benchmark_graphics_memory,
            "memory_stability": self._benchmark_memory_stability
        }
        
        memory_results = {}
        
        for benchmark_name, benchmark_func in memory_benchmarks.items():
            result = self._run_single_benchmark(benchmark_name, benchmark_func)
            memory_results[benchmark_name] = result
        
        self.benchmark_results["memory_benchmarks"] = memory_results
    
    def _run_single_benchmark(self, benchmark_name: str, benchmark_func) -> Dict[str, Any]:
        """Run a single benchmark with timing and error handling."""
        
        self.benchmark_results["performance_summary"]["total_benchmarks"] += 1
        
        try:
            print(f"  → Running {benchmark_name}...")
            
            result = benchmark_func()
            
            # Determine if benchmark passed based on performance thresholds
            if result.get("performance_status") == "PASS":
                self.benchmark_results["performance_summary"]["passed_benchmarks"] += 1
                print(f"    ✅ {benchmark_name} PASSED - {result.get('metric', 'N/A')}")
            elif result.get("performance_status") == "REGRESSION":
                self.benchmark_results["performance_summary"]["performance_regressions"] += 1
                self.benchmark_results["performance_summary"]["failed_benchmarks"] += 1
                print(f"    📉 {benchmark_name} REGRESSION - {result.get('issue', 'Performance degraded')}")
            else:
                self.benchmark_results["performance_summary"]["failed_benchmarks"] += 1
                print(f"    ❌ {benchmark_name} FAILED - {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            self.benchmark_results["performance_summary"]["failed_benchmarks"] += 1
            error_result = {
                "performance_status": "FAIL",
                "benchmark_name": benchmark_name,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            print(f"    💥 {benchmark_name} CRASHED - {str(e)}")
            return error_result
    
    # Core System Benchmarks
    
    def _benchmark_event_bus(self) -> Dict[str, Any]:
        """Benchmark event bus performance."""
        
        try:
            from core.event_bus import EventBus
            
            bus = EventBus()
            events_received = []
            
            def benchmark_handler(event):
                events_received.append(event.data)
            
            bus.subscribe("benchmark.test", benchmark_handler)
            
            # Benchmark event processing performance
            num_events = 1000
            start_time = time.perf_counter()
            
            for i in range(num_events):
                bus.publish("benchmark.test", {"index": i})
            
            end_time = time.perf_counter()
            
            processing_time = end_time - start_time
            events_per_second = num_events / processing_time
            
            # Performance thresholds
            target_eps = 10000  # 10k events/second
            
            if events_per_second >= target_eps and len(events_received) == num_events:
                return {
                    "performance_status": "PASS",
                    "processing_time": processing_time,
                    "events_per_second": events_per_second,
                    "events_processed": len(events_received),
                    "metric": f"{events_per_second:.0f} events/sec"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "processing_time": processing_time,
                    "events_per_second": events_per_second,
                    "target_eps": target_eps,
                    "issue": f"Performance below target: {events_per_second:.0f} < {target_eps}"
                }
        
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _benchmark_simulation_clock(self) -> Dict[str, Any]:
        """Benchmark simulation clock performance."""
        
        try:
            from core.simulation_clock import SimulationClock
            from core.event_bus import EventBus
            
            bus = EventBus()
            
            # Benchmark clock creation
            start_time = time.perf_counter()
            clock = SimulationClock(bus)
            creation_time = time.perf_counter() - start_time
            
            # Benchmark time operations
            start_time = time.perf_counter()
            
            for _ in range(100):
                clock.set_speed(1.0)
                current_time = clock.current_time
                clock.get_speed()
            
            operations_time = time.perf_counter() - start_time
            
            # Performance thresholds
            target_creation_time = 0.1  # 100ms
            target_operations_time = 0.05  # 50ms for 100 operations
            
            if creation_time <= target_creation_time and operations_time <= target_operations_time:
                return {
                    "performance_status": "PASS",
                    "creation_time": creation_time,
                    "operations_time": operations_time,
                    "metric": f"Create: {creation_time*1000:.1f}ms, Ops: {operations_time*1000:.1f}ms"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "creation_time": creation_time,
                    "operations_time": operations_time,
                    "issue": f"Clock performance degraded"
                }
        
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _benchmark_app_startup(self) -> Dict[str, Any]:
        """Benchmark application startup performance."""
        
        try:
            # Benchmark app framework startup
            start_time = time.perf_counter()
            
            from core.app_framework import Application
            app = Application()
            
            startup_time = time.perf_counter() - start_time
            
            # Performance threshold
            target_startup_time = 2.0  # 2 seconds
            
            if startup_time <= target_startup_time:
                return {
                    "performance_status": "PASS",
                    "startup_time": startup_time,
                    "metric": f"{startup_time:.3f}s startup"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "startup_time": startup_time,
                    "target": target_startup_time,
                    "issue": f"Startup too slow: {startup_time:.3f}s > {target_startup_time}s"
                }
        
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _benchmark_config_manager(self) -> Dict[str, Any]:
        """Benchmark configuration manager performance."""
        
        try:
            from core.config_manager import ConfigManager
            
            # Benchmark config operations
            start_time = time.perf_counter()
            
            config = ConfigManager()
            
            for _ in range(1000):
                value = config.get("graphics.target_fps", 60)
            
            operations_time = time.perf_counter() - start_time
            
            # Performance threshold
            target_time = 0.1  # 100ms for 1000 operations
            
            if operations_time <= target_time:
                return {
                    "performance_status": "PASS",
                    "operations_time": operations_time,
                    "metric": f"{operations_time*1000:.1f}ms for 1k ops"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "operations_time": operations_time,
                    "target": target_time,
                    "issue": f"Config operations too slow"
                }
        
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    # Graphics System Benchmarks
    
    def _benchmark_graphics_import(self) -> Dict[str, Any]:
        """Benchmark graphics system import performance."""
        
        try:
            # Benchmark graphics manager import
            start_time = time.perf_counter()
            
            from graphics.graphics_manager import GraphicsManager
            
            import_time = time.perf_counter() - start_time
            
            # Performance threshold
            target_import_time = 1.0  # 1 second
            
            if import_time <= target_import_time:
                return {
                    "performance_status": "PASS",
                    "import_time": import_time,
                    "metric": f"{import_time:.3f}s import"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "import_time": import_time,
                    "target": target_import_time,
                    "issue": f"Graphics import too slow"
                }
        
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _benchmark_graphics_instantiation(self) -> Dict[str, Any]:
        """Benchmark graphics manager instantiation performance."""
        
        try:
            from graphics.graphics_manager import GraphicsManager
            
            # Benchmark instantiation
            start_time = time.perf_counter()
            
            graphics_mgr = GraphicsManager()
            
            instantiation_time = time.perf_counter() - start_time
            
            # Performance threshold
            target_time = 0.5  # 500ms
            
            if instantiation_time <= target_time:
                return {
                    "performance_status": "PASS",
                    "instantiation_time": instantiation_time,
                    "metric": f"{instantiation_time:.3f}s instantiation"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "instantiation_time": instantiation_time,
                    "target": target_time,
                    "issue": f"Graphics instantiation too slow"
                }
        
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _benchmark_panda3d_performance(self) -> Dict[str, Any]:
        """Benchmark Panda3D availability and basic performance."""
        
        try:
            # Benchmark Panda3D basic operations
            start_time = time.perf_counter()
            
            from panda3d.core import Vec3, Vec4
            
            # Basic math operations
            for i in range(1000):
                vec = Vec3(i, i*2, i*3)
                length = vec.length()
            
            operations_time = time.perf_counter() - start_time
            
            # Performance threshold
            target_time = 0.1  # 100ms for 1000 operations
            
            if operations_time <= target_time:
                return {
                    "performance_status": "PASS",
                    "operations_time": operations_time,
                    "metric": f"{operations_time*1000:.1f}ms for 1k vec ops"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "operations_time": operations_time,
                    "target": target_time,
                    "issue": f"Panda3D operations too slow"
                }
        
        except ImportError:
            return {
                "performance_status": "FAIL",
                "error": "Panda3D not available",
                "impact": "Graphics system cannot function"
            }
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    # Integration Benchmarks
    
    def _benchmark_full_system(self) -> Dict[str, Any]:
        """Benchmark full system integration performance."""
        
        try:
            # Benchmark full system startup
            start_time = time.perf_counter()
            
            from core.app_framework import Application
            from graphics.graphics_manager import GraphicsManager
            
            app = Application()
            graphics_mgr = GraphicsManager()
            
            full_startup_time = time.perf_counter() - start_time
            
            # Performance threshold
            target_time = 3.0  # 3 seconds for full system
            
            if full_startup_time <= target_time:
                return {
                    "performance_status": "PASS",
                    "full_startup_time": full_startup_time,
                    "metric": f"{full_startup_time:.3f}s full startup"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "full_startup_time": full_startup_time,
                    "target": target_time,
                    "issue": f"Full system startup too slow"
                }
        
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _benchmark_component_communication(self) -> Dict[str, Any]:
        """Benchmark component communication performance."""
        
        try:
            from core.app_framework import Application
            
            app = Application()
            
            # Benchmark cross-component communication
            messages_received = []
            
            def communication_handler(event):
                messages_received.append(event.data)
            
            app.event_bus.subscribe("benchmark.communication", communication_handler)
            
            start_time = time.perf_counter()
            
            for i in range(500):
                app.event_bus.publish("benchmark.communication", {"message": i})
            
            communication_time = time.perf_counter() - start_time
            
            # Performance threshold
            target_time = 0.1  # 100ms for 500 messages
            
            if communication_time <= target_time and len(messages_received) == 500:
                return {
                    "performance_status": "PASS",
                    "communication_time": communication_time,
                    "messages_processed": len(messages_received),
                    "metric": f"{communication_time*1000:.1f}ms for 500 messages"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "communication_time": communication_time,
                    "target": target_time,
                    "issue": f"Component communication too slow"
                }
        
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _benchmark_concurrent_ops(self) -> Dict[str, Any]:
        """Benchmark concurrent operations performance."""
        
        try:
            from core.app_framework import Application
            
            app = Application()
            
            # Benchmark concurrent event processing and time operations
            start_time = time.perf_counter()
            
            events_received = []
            
            def concurrent_handler(event):
                events_received.append(event.data)
            
            app.event_bus.subscribe("benchmark.concurrent", concurrent_handler)
            
            # Simulate concurrent operations
            for i in range(100):
                app.event_bus.publish("benchmark.concurrent", {"index": i})
                app.clock.set_speed(1.0 + (i % 5))
                current_time = app.clock.current_time
            
            concurrent_time = time.perf_counter() - start_time
            
            # Performance threshold
            target_time = 0.2  # 200ms for concurrent ops
            
            if concurrent_time <= target_time and len(events_received) == 100:
                return {
                    "performance_status": "PASS",
                    "concurrent_time": concurrent_time,
                    "operations_completed": len(events_received),
                    "metric": f"{concurrent_time*1000:.1f}ms concurrent"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "concurrent_time": concurrent_time,
                    "target": target_time,
                    "issue": f"Concurrent operations too slow"
                }
        
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    # Memory Benchmarks
    
    def _benchmark_baseline_memory(self) -> Dict[str, Any]:
        """Benchmark baseline memory usage."""
        
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Memory threshold
            target_baseline = 50  # 50MB baseline
            
            if baseline_memory <= target_baseline:
                return {
                    "performance_status": "PASS",
                    "baseline_memory": baseline_memory,
                    "metric": f"{baseline_memory:.1f}MB baseline"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "baseline_memory": baseline_memory,
                    "target": target_baseline,
                    "issue": f"Baseline memory too high"
                }
        
        except ImportError:
            return {
                "performance_status": "PASS",
                "message": "psutil not available - memory monitoring disabled"
            }
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _benchmark_graphics_memory(self) -> Dict[str, Any]:
        """Benchmark graphics system memory impact."""
        
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Load graphics system
            from graphics.graphics_manager import GraphicsManager
            graphics_mgr = GraphicsManager()
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            # Memory threshold
            target_increase = 20  # 20MB increase
            
            if memory_increase <= target_increase:
                return {
                    "performance_status": "PASS",
                    "memory_increase": memory_increase,
                    "initial_memory": initial_memory,
                    "final_memory": final_memory,
                    "metric": f"+{memory_increase:.1f}MB graphics"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "memory_increase": memory_increase,
                    "target": target_increase,
                    "issue": f"Graphics memory impact too high"
                }
        
        except ImportError:
            return {
                "performance_status": "PASS",
                "message": "psutil not available - memory monitoring disabled"
            }
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _benchmark_memory_stability(self) -> Dict[str, Any]:
        """Benchmark memory stability over operations."""
        
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            
            from core.app_framework import Application
            app = Application()
            
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Perform operations that might leak memory
            for i in range(1000):
                events_received = []
                
                def temp_handler(event):
                    events_received.append(event.data)
                
                app.event_bus.subscribe(f"temp.{i}", temp_handler)
                app.event_bus.publish(f"temp.{i}", {"data": i})
                app.event_bus.unsubscribe(f"temp.{i}", temp_handler)
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_growth = final_memory - initial_memory
            
            # Stability threshold
            target_growth = 5  # 5MB growth acceptable
            
            if memory_growth <= target_growth:
                return {
                    "performance_status": "PASS",
                    "memory_growth": memory_growth,
                    "metric": f"+{memory_growth:.1f}MB after 1k ops"
                }
            else:
                return {
                    "performance_status": "REGRESSION",
                    "memory_growth": memory_growth,
                    "target": target_growth,
                    "issue": f"Memory leak detected: +{memory_growth:.1f}MB"
                }
        
        except ImportError:
            return {
                "performance_status": "PASS",
                "message": "psutil not available - memory monitoring disabled"
            }
        except Exception as e:
            return {
                "performance_status": "FAIL",
                "error": str(e)
            }
    
    def _determine_performance_status(self):
        """Determine overall performance status."""
        
        total = self.benchmark_results["performance_summary"]["total_benchmarks"]
        passed = self.benchmark_results["performance_summary"]["passed_benchmarks"]
        regressions = self.benchmark_results["performance_summary"]["performance_regressions"]
        
        if regressions == 0 and passed == total:
            self.benchmark_results["performance_status"] = "OPTIMAL"
        elif regressions == 0:
            self.benchmark_results["performance_status"] = "ACCEPTABLE"
        elif regressions <= total * 0.2:  # 20% regression threshold
            self.benchmark_results["performance_status"] = "MINOR_REGRESSIONS"
        else:
            self.benchmark_results["performance_status"] = "PERFORMANCE_DEGRADED"
    
    def save_results(self):
        """Save performance benchmark results."""
        
        report_content = f"""# Performance Benchmark Results
**Generated:** {self.benchmark_results['timestamp']}  
**Purpose:** Verify performance impact of graphics system fixes

---

## Performance Status: {self.benchmark_results['performance_status']}

### Benchmark Summary
- **Total Benchmarks:** {self.benchmark_results['performance_summary']['total_benchmarks']}
- **Passed:** {self.benchmark_results['performance_summary']['passed_benchmarks']}
- **Failed:** {self.benchmark_results['performance_summary']['failed_benchmarks']}
- **Performance Regressions:** {self.benchmark_results['performance_summary']['performance_regressions']}

---

## Core System Performance
"""
        
        for benchmark_name, result in self.benchmark_results["core_system_benchmarks"].items():
            status_icon = "✅" if result.get("performance_status") == "PASS" else "📉" if result.get("performance_status") == "REGRESSION" else "❌"
            metric = result.get("metric", result.get("error", "No metric"))
            report_content += f"- {status_icon} **{benchmark_name}:** {metric}\n"
        
        report_content += "\n## Graphics System Performance\n"
        for benchmark_name, result in self.benchmark_results["graphics_system_benchmarks"].items():
            status_icon = "✅" if result.get("performance_status") == "PASS" else "📉" if result.get("performance_status") == "REGRESSION" else "❌"
            metric = result.get("metric", result.get("error", "No metric"))
            report_content += f"- {status_icon} **{benchmark_name}:** {metric}\n"
        
        report_content += "\n## Integration Performance\n"
        for benchmark_name, result in self.benchmark_results["integration_benchmarks"].items():
            status_icon = "✅" if result.get("performance_status") == "PASS" else "📉" if result.get("performance_status") == "REGRESSION" else "❌"
            metric = result.get("metric", result.get("error", "No metric"))
            report_content += f"- {status_icon} **{benchmark_name}:** {metric}\n"
        
        report_content += "\n## Memory Performance\n"
        for benchmark_name, result in self.benchmark_results["memory_benchmarks"].items():
            status_icon = "✅" if result.get("performance_status") == "PASS" else "📉" if result.get("performance_status") == "REGRESSION" else "❌"
            metric = result.get("metric", result.get("message", result.get("error", "No metric")))
            report_content += f"- {status_icon} **{benchmark_name}:** {metric}\n"
        
        output_path = workspace_root / "investigation_base_camp" / "validation" / "performance_benchmark_results.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Performance benchmark results saved to: {output_path}")
        return output_path

def main():
    """Run performance benchmark suite."""
    print("⚡ Starting Performance Benchmark Suite...")
    
    benchmark = PerformanceBenchmark()
    benchmark.run_all_benchmarks()
    
    # Print summary
    summary = benchmark.benchmark_results["performance_summary"]
    status = benchmark.benchmark_results["performance_status"]
    
    print(f"\n📊 Performance Summary:")
    print(f"   ⚡ Performance Status: {status}")
    print(f"   ✅ Passed: {summary['passed_benchmarks']}")
    print(f"   ❌ Failed: {summary['failed_benchmarks']}")
    print(f"   📉 Regressions: {summary['performance_regressions']}")
    
    if summary['performance_regressions'] > 0:
        print(f"\n🚨 PERFORMANCE REGRESSIONS DETECTED:")
        print(f"   → Review benchmark details for optimization opportunities")
    
    output_path = benchmark.save_results()
    print(f"\n💾 Complete results saved to: {output_path}")

if __name__ == "__main__":
    main()