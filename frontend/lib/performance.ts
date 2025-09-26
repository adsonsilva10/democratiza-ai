interface PerformanceThreshold {
  good: number;
  needsImprovement: number;
}

interface PerformanceAlert {
  id: string;
  type: 'warning' | 'error' | 'info';
  metric: string;
  message: string;
  value: number;
  threshold: number;
  timestamp: Date;
}

interface PerformanceConfig {
  thresholds: {
    pageLoadTime: PerformanceThreshold;
    firstContentfulPaint: PerformanceThreshold;
    cumulativeLayoutShift: PerformanceThreshold;
    largestContentfulPaint: PerformanceThreshold;
    firstInputDelay: PerformanceThreshold;
  };
  alertsEnabled: boolean;
  maxAlerts: number;
}

export class PerformanceAnalyzer {
  private config: PerformanceConfig;
  private alerts: PerformanceAlert[] = [];
  private observers: PerformanceObserver[] = [];

  constructor(config?: Partial<PerformanceConfig>) {
    this.config = {
      thresholds: {
        pageLoadTime: { good: 2000, needsImprovement: 4000 },
        firstContentfulPaint: { good: 1800, needsImprovement: 3000 },
        cumulativeLayoutShift: { good: 0.1, needsImprovement: 0.25 },
        largestContentfulPaint: { good: 2500, needsImprovement: 4000 },
        firstInputDelay: { good: 100, needsImprovement: 300 }
      },
      alertsEnabled: true,
      maxAlerts: 50,
      ...config
    };

    if (typeof window !== 'undefined' && 'PerformanceObserver' in window) {
      this.initializeObservers();
    }
  }

  private initializeObservers(): void {
    // Observe Core Web Vitals
    try {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          this.analyzeEntry(entry);
        }
      });

      observer.observe({ 
        type: 'navigation', 
        buffered: true 
      });

      observer.observe({ 
        type: 'paint', 
        buffered: true 
      });

      observer.observe({ 
        type: 'largest-contentful-paint', 
        buffered: true 
      });

      observer.observe({ 
        type: 'layout-shift', 
        buffered: true 
      });

      this.observers.push(observer);
    } catch (error) {
      console.warn('PerformanceObserver not fully supported:', error);
    }
  }

  private analyzeEntry(entry: PerformanceEntry): void {
    if (!this.config.alertsEnabled) return;

    switch (entry.entryType) {
      case 'navigation':
        this.analyzeNavigationTiming(entry as PerformanceNavigationTiming);
        break;
      case 'paint':
        this.analyzePaintTiming(entry);
        break;
      case 'largest-contentful-paint':
        this.analyzeLCP(entry);
        break;
      case 'layout-shift':
        this.analyzeCLS(entry);
        break;
    }
  }

  private analyzeNavigationTiming(entry: PerformanceNavigationTiming): void {
    const loadTime = entry.loadEventEnd - entry.loadEventStart;
    const threshold = this.config.thresholds.pageLoadTime;

    if (loadTime > threshold.needsImprovement) {
      this.addAlert({
        type: 'error',
        metric: 'Page Load Time',
        message: `Page load time (${loadTime}ms) exceeds threshold`,
        value: loadTime,
        threshold: threshold.needsImprovement
      });
    } else if (loadTime > threshold.good) {
      this.addAlert({
        type: 'warning',
        metric: 'Page Load Time',
        message: `Page load time (${loadTime}ms) needs improvement`,
        value: loadTime,
        threshold: threshold.good
      });
    }
  }

  private analyzePaintTiming(entry: PerformanceEntry): void {
    if (entry.name === 'first-contentful-paint') {
      const fcp = entry.startTime;
      const threshold = this.config.thresholds.firstContentfulPaint;

      if (fcp > threshold.needsImprovement) {
        this.addAlert({
          type: 'error',
          metric: 'First Contentful Paint',
          message: `FCP (${fcp.toFixed(0)}ms) is too slow`,
          value: fcp,
          threshold: threshold.needsImprovement
        });
      } else if (fcp > threshold.good) {
        this.addAlert({
          type: 'warning',
          metric: 'First Contentful Paint',
          message: `FCP (${fcp.toFixed(0)}ms) could be faster`,
          value: fcp,
          threshold: threshold.good
        });
      }
    }
  }

  private analyzeLCP(entry: PerformanceEntry): void {
    const lcp = entry.startTime;
    const threshold = this.config.thresholds.largestContentfulPaint;

    if (lcp > threshold.needsImprovement) {
      this.addAlert({
        type: 'error',
        metric: 'Largest Contentful Paint',
        message: `LCP (${lcp.toFixed(0)}ms) is too slow`,
        value: lcp,
        threshold: threshold.needsImprovement
      });
    } else if (lcp > threshold.good) {
      this.addAlert({
        type: 'warning',
        metric: 'Largest Contentful Paint',
        message: `LCP (${lcp.toFixed(0)}ms) needs improvement`,
        value: lcp,
        threshold: threshold.good
      });
    }
  }

  private analyzeCLS(entry: any): void {
    if (!entry.hadRecentInput) {
      const cls = entry.value;
      const threshold = this.config.thresholds.cumulativeLayoutShift;

      if (cls > threshold.needsImprovement) {
        this.addAlert({
          type: 'error',
          metric: 'Cumulative Layout Shift',
          message: `CLS (${cls.toFixed(3)}) indicates poor visual stability`,
          value: cls,
          threshold: threshold.needsImprovement
        });
      } else if (cls > threshold.good) {
        this.addAlert({
          type: 'warning',
          metric: 'Cumulative Layout Shift',
          message: `CLS (${cls.toFixed(3)}) could be improved`,
          value: cls,
          threshold: threshold.good
        });
      }
    }
  }

  private addAlert(alertData: Omit<PerformanceAlert, 'id' | 'timestamp'>): void {
    const alert: PerformanceAlert = {
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      timestamp: new Date(),
      ...alertData
    };

    this.alerts.unshift(alert);

    // Keep only the most recent alerts
    if (this.alerts.length > this.config.maxAlerts) {
      this.alerts = this.alerts.slice(0, this.config.maxAlerts);
    }

    // Log to console for debugging
    console.warn(`Performance Alert: ${alert.message}`);
  }

  public getAlerts(): PerformanceAlert[] {
    return [...this.alerts];
  }

  public clearAlerts(): void {
    this.alerts = [];
  }

  public getConfig(): PerformanceConfig {
    return { ...this.config };
  }

  public updateConfig(newConfig: Partial<PerformanceConfig>): void {
    this.config = { ...this.config, ...newConfig };
  }

  public destroy(): void {
    this.observers.forEach(observer => observer.disconnect());
    this.observers = [];
    this.alerts = [];
  }

  // Utility methods
  public static formatMetric(value: number, metric: string): string {
    switch (metric) {
      case 'Cumulative Layout Shift':
        return value.toFixed(3);
      case 'First Input Delay':
      case 'Page Load Time':
      case 'First Contentful Paint':
      case 'Largest Contentful Paint':
        return `${Math.round(value)}ms`;
      default:
        return value.toString();
    }
  }

  public static getRating(value: number, threshold: PerformanceThreshold): 'good' | 'needs-improvement' | 'poor' {
    if (value <= threshold.good) return 'good';
    if (value <= threshold.needsImprovement) return 'needs-improvement';
    return 'poor';
  }
}

// Default instance for easy use
export const performanceAnalyzer = new PerformanceAnalyzer();

// Hook for React components
export const usePerformanceAnalyzer = () => {
  return {
    analyzer: performanceAnalyzer,
    getAlerts: () => performanceAnalyzer.getAlerts(),
    clearAlerts: () => performanceAnalyzer.clearAlerts()
  };
};