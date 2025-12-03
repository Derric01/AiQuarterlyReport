import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { FileText, Copy, Download, RefreshCw } from 'lucide-react';
import { toast } from './ui/toast';
import { useMutation } from '@tanstack/react-query';
import { generateReport } from '@/lib/api';

export default function ReportCard({ report, loading, setReport, metrics }) {
  const regenerateReportMutation = useMutation({
    mutationFn: (metrics) => generateReport(metrics),
    onSuccess: (data) => {
      setReport(data.report);
      toast({ title: "Success", description: "Report regenerated successfully!" });
    },
    onError: (error) => {
      toast({ 
        title: "Error", 
        description: "Failed to regenerate report: " + error.message,
        variant: "destructive"
      });
    }
  });

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(report);
      toast({ title: "Copied!", description: "Report copied to clipboard" });
    } catch (err) {
      toast({ 
        title: "Error", 
        description: "Failed to copy to clipboard",
        variant: "destructive"
      });
    }
  };

  const handleDownload = () => {
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `quarterly-report-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast({ title: "Downloaded!", description: "Report saved to your downloads" });
  };

  const handleRegenerate = () => {
    if (!metrics) {
      toast({ 
        title: "Error", 
        description: "Metrics required to regenerate report",
        variant: "destructive"
      });
      return;
    }
    regenerateReportMutation.mutate(metrics);
  };

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card className="card-gradient">
          <CardHeader>
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-4 w-48" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-3/4 mb-4" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-2/3" />
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  if (!report) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card className="card-gradient border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-16 text-center">
            <FileText className="text-gray-500 mb-4" width={48} height={48} strokeWidth={1.5} />
            <h3 className="font-semibold text-gray-300 mb-2">No Report Generated</h3>
            <p className="text-sm text-gray-400">
              Click "Generate Report" to create an AI-powered quarterly market report
            </p>
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  // Split report into paragraphs
  const paragraphs = report.split('\n\n').filter(p => p.trim());

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
    >
      <Card className="card-gradient">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2 text-gray-100">
                <FileText className="text-blue-400" width={20} height={20} strokeWidth={2} />
                AI-Generated Report
              </CardTitle>
              <CardDescription className="text-gray-400">
                Quarterly equity market analysis with AI insights
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
                className="flex items-center gap-2"
              >
                <Copy width={16} height={16} strokeWidth={2} />
                Copy
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownload}
                className="flex items-center gap-2"
              >
                <Download width={16} height={16} strokeWidth={2} />
                Download
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleRegenerate}
                disabled={regenerateReportMutation.isPending}
                className="flex items-center gap-2"
              >
                <RefreshCw className={regenerateReportMutation.isPending ? 'animate-spin' : ''} width={16} height={16} strokeWidth={2} />
                Regenerate
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <div className="prose prose-gray max-w-none">
            {paragraphs.map((paragraph, index) => (
              <motion.p
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.2 }}
                className="text-gray-200 leading-relaxed mb-4 text-justify"
              >
                {paragraph}
              </motion.p>
            ))}
          </div>
          
          {paragraphs.length === 0 && (
            <p className="text-gray-400 italic">Report content is empty</p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}