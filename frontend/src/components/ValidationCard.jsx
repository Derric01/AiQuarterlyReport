import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Shield, CheckCircle, X, AlertCircle } from 'lucide-react';

export default function ValidationCard({ validation, loading }) {
  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card className="card-gradient">
          <CardHeader>
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-4 w-48" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-16 w-full" />
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  if (!validation) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card className="card-gradient border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-16 text-center">
            <Shield className="text-gray-500 mb-4" width={48} height={48} strokeWidth={1.5} />
            <h3 className="font-semibold text-gray-300 mb-2">No Validation Results</h3>
            <p className="text-sm text-gray-400">
              Click "Validate Report" to check for accuracy and consistency
            </p>
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  const getStatusIcon = () => {
    if (validation.valid) {
      return <CheckCircle className="text-green-400" width={20} height={20} strokeWidth={2} />;
    }
    return <X className="text-red-400" width={20} height={20} strokeWidth={2} />;
  };

  const getStatusColor = () => {
    return validation.valid ? 'border-green-800 bg-green-950/30' : 'border-red-800 bg-red-950/30';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <Card className={`card-gradient ${getStatusColor()}`}>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-gray-100">
            <Shield className="text-blue-400" width={20} height={20} strokeWidth={2} />
            Validation Results
          </CardTitle>
          <CardDescription className="text-gray-400">
            Deterministic numeric validation and AI-powered semantic analysis
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <div className="space-y-4">
            {/* Overall Status */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              className={`p-4 rounded-lg border-2 ${
                validation.valid 
                  ? 'border-green-700 bg-green-950/30' 
                  : 'border-red-700 bg-red-950/30'
              }`}
            >
              <div className="flex items-center gap-3">
                {getStatusIcon()}
                <div>
                  <h3 className={`font-semibold ${
                    validation.valid ? 'text-green-300' : 'text-red-300'
                  }`}>
                    {validation.valid ? 'Validation Passed' : 'Validation Failed'}
                  </h3>
                  <p className={`text-sm ${
                    validation.valid ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {validation.valid 
                      ? 'Report meets all validation criteria' 
                      : 'Report contains errors that need attention'
                    }
                  </p>
                </div>
              </div>
            </motion.div>

            {/* Validation Types */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Deterministic Validation */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4, delay: 0.1 }}
                className="bg-gray-800 rounded-lg p-4 border border-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-200">Numeric Validation</h4>
                  <Badge variant={validation.deterministic_valid ? "default" : "destructive"}>
                    {validation.deterministic_valid ? "PASS" : "FAIL"}
                  </Badge>
                </div>
                <p className="text-sm text-gray-400">
                  Checks if all numbers match computed metrics
                </p>
              </motion.div>

              {/* Semantic Validation */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4, delay: 0.2 }}
                className="bg-gray-800 rounded-lg p-4 border border-gray-700"
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-200">Semantic Validation</h4>
                  <Badge variant={validation.semantic_valid ? "default" : "destructive"}>
                    {validation.semantic_valid ? "PASS" : "FAIL"}
                  </Badge>
                </div>
                <p className="text-sm text-gray-400">
                  AI checks for fabricated facts or inconsistencies
                </p>
              </motion.div>
            </div>

            {/* Errors List */}
            {validation.errors && validation.errors.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.3 }}
                className="space-y-2"
              >
                <h4 className="font-medium text-gray-200 flex items-center gap-2">
                  <AlertCircle className="text-orange-400" width={16} height={16} strokeWidth={2} />
                  Issues Found ({validation.errors.length})
                </h4>
                <div className="space-y-2 max-h-32 overflow-y-auto">
                  {validation.errors.map((error, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: 0.1 * index }}
                      className="bg-orange-950/30 border border-orange-800 rounded p-3"
                    >
                      <p className="text-sm text-orange-300">{error}</p>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Summary Stats */}
            {validation.valid && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.4 }}
                className="bg-blue-950/30 border border-blue-800 rounded-lg p-4"
              >
                <p className="text-sm text-blue-300 font-medium">
                  ✅ All validation checks passed successfully
                </p>
                <p className="text-xs text-blue-400 mt-1">
                  Report is ready for publication and distribution
                </p>
              </motion.div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}