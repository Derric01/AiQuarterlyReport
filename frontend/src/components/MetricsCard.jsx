import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Button } from '@/components/ui/button.jsx';
import { Skeleton } from '@/components/ui/skeleton.jsx';
import { BarChart3, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

export default function MetricsCard({ metrics, loading }) {
  const [collapsed, setCollapsed] = useState(false);

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="card-gradient">
          <CardHeader>
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-4 w-48" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-64 w-full" />
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  if (!metrics) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="card-gradient border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-16 text-center">
            <BarChart3 className="text-gray-500 mb-4" width={48} height={48} strokeWidth={1.5} />
            <h3 className="font-semibold text-gray-300 mb-2">No Metrics Computed</h3>
            <p className="text-sm text-gray-400">
              Click "Fetch Data" then "Compute Metrics" to generate financial metrics
            </p>
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  const formatMetricValue = (value) => {
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
    return value;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="card-gradient">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2 text-gray-100">
                <BarChart3 className="text-blue-400" width={20} height={20} strokeWidth={2} />
                Financial Metrics
              </CardTitle>
              <CardDescription className="text-gray-400">
                Computed quarterly and YTD returns with market highs
              </CardDescription>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setCollapsed(!collapsed)}
              className="flex items-center gap-1"
            >
              {collapsed ? <ChevronDown width={16} height={16} strokeWidth={2} /> : <ChevronUp width={16} height={16} strokeWidth={2} />}
            </Button>
          </div>
        </CardHeader>
        
        {!collapsed && (
          <CardContent>
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                {Object.entries(metrics).map(([key, value], index) => (
                  <motion.div
                    key={key}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className="bg-gray-800 rounded-lg p-4 border border-gray-700"
                  >
                    <div className="text-sm font-medium text-gray-400 mb-1">
                      {key.replace(/_/g, ' ').toUpperCase()}
                    </div>
                    <div className="text-lg font-bold text-gray-100">
                      {typeof value === 'number' && key.includes('return') 
                        ? `${formatMetricValue(value)}%`
                        : formatMetricValue(value)
                      }
                    </div>
                  </motion.div>
                ))}
              </div>
              
              <div className="bg-gray-950 rounded-lg p-4 overflow-auto">
                <div className="text-green-400 text-xs mb-2 font-mono">
                  // Raw JSON Data
                </div>
                <pre className="text-green-300 text-sm font-mono whitespace-pre-wrap">
                  {JSON.stringify(metrics, null, 2)}
                </pre>
              </div>
            </motion.div>
          </CardContent>
        )}
      </Card>
    </motion.div>
  );
}