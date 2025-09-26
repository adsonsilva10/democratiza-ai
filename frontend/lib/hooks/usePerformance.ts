import { useState, useEffect } from 'react';

interface PerformanceMetric {
  name: string;
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
}

interface PerformanceData {
  good: number;
  needsImprovement: number;
  poor: number;
  average: number;
}

interface PageLoadMetrics {
  loadTime: number;
  domContentLoaded: number;
  firstContentfulPaint: number;
}

interface ApiPerformanceMetrics {
  avgResponseTime: number;
  successRate: number;
  errorCount: number;
}

export const usePerformance = () => {
  const [metrics, setMetrics] = useState<PerformanceMetric[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const collectMetrics = () => {
      if ('performance' in window) {
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        const paint = performance.getEntriesByType('paint');
        
        const newMetrics: PerformanceMetric[] = [
          {
            name: 'Page Load Time',
            value: navigation.loadEventEnd - navigation.loadEventStart,
            rating: navigation.loadEventEnd - navigation.loadEventStart < 2000 ? 'good' : 
                   navigation.loadEventEnd - navigation.loadEventStart < 4000 ? 'needs-improvement' : 'poor'
          },
          {
            name: 'DOM Content Loaded',
            value: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
            rating: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart < 1500 ? 'good' :
                   navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart < 3000 ? 'needs-improvement' : 'poor'
          }
        ];

        if (paint.length > 0) {
          const fcp = paint.find(entry => entry.name === 'first-contentful-paint');
          if (fcp) {
            newMetrics.push({
              name: 'First Contentful Paint',
              value: fcp.startTime,
              rating: fcp.startTime < 1800 ? 'good' : fcp.startTime < 3000 ? 'needs-improvement' : 'poor'
            });
          }
        }

        setMetrics(newMetrics);
      }
      setIsLoading(false);
    };

    // Collect metrics after page load
    if (document.readyState === 'complete') {
      setTimeout(collectMetrics, 100);
    } else {
      window.addEventListener('load', () => setTimeout(collectMetrics, 100));
    }
  }, []);

  const data: PerformanceData = {
    good: metrics.filter(m => m.rating === 'good').length,
    needsImprovement: metrics.filter(m => m.rating === 'needs-improvement').length,
    poor: metrics.filter(m => m.rating === 'poor').length,
    average: metrics.length > 0 ? Math.round(metrics.reduce((acc, m) => acc + m.value, 0) / metrics.length) : 0
  };

  const getMetricsSummary = () => {
    const summary = {
      total: metrics.length,
      byMetric: {} as Record<string, { good: number; needsImprovement: number; poor: number; average: number }>,
      byPage: {} as Record<string, number>
    };

    metrics.forEach(metric => {
      if (!summary.byMetric[metric.name]) {
        summary.byMetric[metric.name] = { good: 0, needsImprovement: 0, poor: 0, average: 0 };
      }
      
      summary.byMetric[metric.name][metric.rating === 'needs-improvement' ? 'needsImprovement' : metric.rating]++;
    });

    // Calculate averages
    Object.keys(summary.byMetric).forEach(metricName => {
      const metricData = metrics.filter(m => m.name === metricName);
      const avg = metricData.length > 0 ? 
        metricData.reduce((sum, m) => sum + m.value, 0) / metricData.length : 0;
      summary.byMetric[metricName].average = Math.round(avg);
    });

    return summary;
  };

  return { data, metrics, isLoading, getMetricsSummary };
};

export const usePageLoad = () => {
  const [metrics, setMetrics] = useState<PageLoadMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const collectPageLoadMetrics = () => {
      if ('performance' in window) {
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        const paint = performance.getEntriesByType('paint');
        
        const fcp = paint.find(entry => entry.name === 'first-contentful-paint');
        
        setMetrics({
          loadTime: navigation.loadEventEnd - navigation.loadEventStart,
          domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
          firstContentfulPaint: fcp ? fcp.startTime : 0
        });
      }
      setIsLoading(false);
    };

    if (document.readyState === 'complete') {
      setTimeout(collectPageLoadMetrics, 100);
    } else {
      window.addEventListener('load', () => setTimeout(collectPageLoadMetrics, 100));
    }
  }, []);

  return { metrics, isLoading };
};

export const useApiPerformance = () => {
  const [metrics, setMetrics] = useState<ApiPerformanceMetrics>({
    avgResponseTime: 0,
    successRate: 100,
    errorCount: 0
  });
  const [isLoading, setIsLoading] = useState(false);

  // This would typically track actual API calls
  // For now, returning mock data
  useEffect(() => {
    setMetrics({
      avgResponseTime: Math.floor(Math.random() * 500) + 200, // 200-700ms
      successRate: Math.floor(Math.random() * 10) + 90, // 90-100%
      errorCount: Math.floor(Math.random() * 5) // 0-5 errors
    });
  }, []);

  return { metrics, isLoading };
};