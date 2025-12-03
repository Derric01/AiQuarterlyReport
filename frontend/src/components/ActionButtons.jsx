import { useMutation, useQueryClient } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Database, Calculator, Brain, CheckCircle, Star } from 'lucide-react';
import { fetchData, computeMetrics, generateReport, validateReport, getStyleScore } from '@/lib/api.js';
import { toast } from '@/hooks/use-toast.js';

export default function ActionButtons({ 
  setMetrics, 
  setReport, 
  setValidation, 
  setStyleScore,
  metrics,
  report 
}) {
  const queryClient = useQueryClient();

  const fetchDataMutation = useMutation({
    mutationFn: fetchData,
    onSuccess: (data) => {
      toast({ title: "Success", description: "Market data fetched successfully!" });
    },
    onError: (error) => {
      toast({ 
        title: "Error", 
        description: "Failed to fetch data: " + error.message,
        variant: "destructive"
      });
    }
  });

  const computeMetricsMutation = useMutation({
    mutationFn: computeMetrics,
    onSuccess: (data) => {
      setMetrics(data);
      toast({ title: "Success", description: "Metrics computed successfully!" });
    },
    onError: (error) => {
      toast({ 
        title: "Error", 
        description: "Failed to compute metrics: " + error.message,
        variant: "destructive"
      });
    }
  });

  const generateReportMutation = useMutation({
    mutationFn: (metrics) => generateReport(metrics),
    onSuccess: (data) => {
      setReport(data.report);
      toast({ title: "Success", description: "AI report generated successfully!" });
    },
    onError: (error) => {
      toast({ 
        title: "Error", 
        description: "Failed to generate report: " + error.message,
        variant: "destructive"
      });
    }
  });

  const validateReportMutation = useMutation({
    mutationFn: ({ report, metrics }) => validateReport(report, metrics),
    onSuccess: (data) => {
      setValidation(data);
      toast({ 
        title: data.valid ? "Validation Passed" : "Validation Failed", 
        description: data.valid ? "Report is valid!" : "Report contains errors",
        variant: data.valid ? "default" : "destructive"
      });
    },
    onError: (error) => {
      toast({ 
        title: "Error", 
        description: "Failed to validate report: " + error.message,
        variant: "destructive"
      });
    }
  });

  const styleScoreMutation = useMutation({
    mutationFn: (report) => getStyleScore(report),
    onSuccess: (data) => {
      setStyleScore(data);
      toast({ 
        title: "Style Analysis Complete", 
        description: `Style match: ${data.score}%` 
      });
    },
    onError: (error) => {
      toast({ 
        title: "Error", 
        description: "Failed to analyze style: " + error.message,
        variant: "destructive"
      });
    }
  });

  const buttons = [
    {
      label: "Fetch Data",
      icon: Database,
      action: () => fetchDataMutation.mutate(),
      loading: fetchDataMutation.isPending,
      disabled: false,
      description: "Download ACWI & S&P 500 data"
    },
    {
      label: "Compute Metrics",
      icon: Calculator,
      action: () => computeMetricsMutation.mutate(),
      loading: computeMetricsMutation.isPending,
      disabled: false,
      description: "Calculate quarterly returns & highs"
    },
    {
      label: "Generate Report",
      icon: Brain,
      action: () => generateReportMutation.mutate(metrics),
      loading: generateReportMutation.isPending,
      disabled: !metrics,
      description: "AI-powered report generation"
    },
    {
      label: "Validate Report",
      icon: CheckCircle,
      action: () => validateReportMutation.mutate({ report, metrics }),
      loading: validateReportMutation.isPending,
      disabled: !report || !metrics,
      description: "Deterministic & semantic validation"
    },
    {
      label: "Style Score",
      icon: Star,
      action: () => styleScoreMutation.mutate(report),
      loading: styleScoreMutation.isPending,
      disabled: !report,
      description: "RAG-based style matching"
    }
  ];

  return (
    <Card className="card-gradient">
      <CardContent className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {buttons.map((button, index) => (
            <motion.div
              key={button.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
            >
              <div className="text-center space-y-3">
                <Button
                  onClick={button.action}
                  disabled={button.disabled || button.loading}
                  className="w-full h-20 flex flex-col items-center justify-center space-y-2 bg-gradient-to-br from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 shadow-lg hover:shadow-xl transition-all duration-200"
                  size="lg"
                >
                  {button.loading ? (
                    <div className="animate-spin">
                      <button.icon width={24} height={24} strokeWidth={2} />
                    </div>
                  ) : (
                    <button.icon width={24} height={24} strokeWidth={2} />
                  )}
                  <span className="text-sm font-medium">{button.label}</span>
                </Button>
                <p className="text-xs text-gray-600">{button.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}