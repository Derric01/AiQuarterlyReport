import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Skeleton } from '@/components/ui/skeleton.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Progress } from '@/components/ui/progress.jsx';
import { BarChart3, Edit, PieChart, FileText, Sparkles, TrendingUp, Star, Trophy, CheckCircle } from 'lucide-react';

export default function StyleScoreCard({ styleScore, loading }) {
  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card className="card-gradient">
          <CardHeader>
            <Skeleton className="h-6 w-48" />
            <Skeleton className="h-4 w-64" />
          </CardHeader>
          <CardContent className="space-y-6">
            <Skeleton className="h-32 w-full" />
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-24 w-full" />
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  if (!styleScore) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card className="card-gradient border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-20 text-center">
            <div className="w-12 h-12 rounded-full bg-gray-700 flex items-center justify-center mb-4">
              <BarChart3 className="text-gray-400" width={24} height={24} strokeWidth={2} />
            </div>
            <h3 className="font-semibold text-gray-300 text-lg mb-2">No Style Analysis</h3>
            <p className="text-sm text-gray-400 max-w-md">
              Generate a report to receive quality style scoring
            </p>
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  const getGradeColor = (grade) => {
    if (grade.startsWith('A')) return { bg: 'bg-emerald-900/30', text: 'text-emerald-300', border: 'border-emerald-700' };
    if (grade.startsWith('B')) return { bg: 'bg-blue-900/30', text: 'text-blue-300', border: 'border-blue-700' };
    if (grade.startsWith('C')) return { bg: 'bg-amber-900/30', text: 'text-amber-300', border: 'border-amber-700' };
    return { bg: 'bg-red-900/30', text: 'text-red-300', border: 'border-red-700' };
  };

  const grade = styleScore.grade || 'B';
  const score = Math.round(styleScore.style_score || styleScore.percentage || 0);
  const gradeColors = getGradeColor(grade);
  const breakdown = styleScore.breakdown || {};

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
    >
      <Card className="card-gradient">
        <CardHeader className="pb-4 border-b border-gray-800">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="flex items-center gap-3 text-gray-100">
                <Edit width={20} height={20} strokeWidth={2} />
                Style Analysis
              </CardTitle>
              <CardDescription className="mt-1.5 text-gray-400">
                Quality assessment • Gemini 2.5
              </CardDescription>
            </div>
            <Badge variant="outline" className={`${gradeColors.bg} ${gradeColors.border} ${gradeColors.text} font-bold px-4 py-1.5 text-xl border-2`}>
              {grade}
            </Badge>
          </div>
        </CardHeader>
        
        <CardContent className="pt-6 space-y-5">
          {/* Overall Score Display */}
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
            className={`p-6 rounded-lg ${gradeColors.bg} border ${gradeColors.border}`}
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-baseline gap-2 mb-1">
                  <span className={`text-5xl font-bold ${gradeColors.text}`}>{score}</span>
                  <span className="text-2xl text-gray-400">/100</span>
                </div>
                <p className={`font-medium ${gradeColors.text} mb-1`}>
                  {styleScore.feedback || 'High quality analysis completed.'}
                </p>
                <div className="flex items-center gap-2 text-xs text-gray-400">
                  <CheckCircle width={14} height={14} strokeWidth={2} />
                  <span>Analyzed via Gemini 2.5</span>
                </div>
              </div>
              <div className="opacity-40">
                {grade.startsWith('A') ? <Trophy width={48} height={48} strokeWidth={1.5} /> : grade.startsWith('B') ? <Star width={48} height={48} strokeWidth={1.5} /> : <BarChart3 width={48} height={48} strokeWidth={1.5} />}
              </div>
            </div>
          </motion.div>

          {/* Score Breakdown */}
          {breakdown && Object.keys(breakdown).length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 pt-2">
                <PieChart width={18} height={18} strokeWidth={2} />
                <h4 className="font-semibold text-gray-200">Detailed Breakdown</h4>
              </div>

              {/* Structural Score */}
              {breakdown.structural && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: 0.1 }}
                  className="bg-gray-800/50 rounded-lg p-4 border border-gray-700"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <FileText width={14} height={14} strokeWidth={2} />
                      <span className="font-medium text-gray-200">Document Structure</span>
                    </div>
                    <Badge variant="secondary" className="bg-gray-700 text-gray-200 font-mono text-xs">
                      {Math.round(breakdown.structural.score)}/{breakdown.structural.max}
                    </Badge>
                  </div>
                  <Progress 
                    value={(breakdown.structural.score / breakdown.structural.max) * 100} 
                    className="h-1.5 mb-3"
                  />
                  {breakdown.structural.details && (
                    <div className="grid grid-cols-2 gap-3 text-xs">
                      <div className="flex justify-between text-gray-400">
                        <span>Words:</span>
                        <span className="font-medium text-gray-300">{breakdown.structural.details.word_count}</span>
                      </div>
                      <div className="flex justify-between text-gray-400">
                        <span>Paragraphs:</span>
                        <span className="font-medium text-gray-300">{breakdown.structural.details.paragraph_count}</span>
                      </div>
                    </div>
                  )}
                </motion.div>
              )}

              {/* Language Quality Score */}
              {breakdown.language_quality && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: 0.2 }}
                  className="bg-gray-800/50 rounded-lg p-4 border border-gray-700"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <Sparkles width={14} height={14} strokeWidth={2} />
                      <span className="font-medium text-gray-200">Language Quality</span>
                    </div>
                    <Badge variant="secondary" className="bg-gray-700 text-gray-200 font-mono text-xs">
                      {Math.round(breakdown.language_quality.score)}/{breakdown.language_quality.max}
                    </Badge>
                  </div>
                  <Progress 
                    value={(breakdown.language_quality.score / breakdown.language_quality.max) * 100} 
                    className="h-1.5 mb-3"
                  />
                  {breakdown.language_quality.details && (
                    <div className="grid grid-cols-2 gap-3 text-xs">
                      {Object.entries(breakdown.language_quality.details).map(([key, val]) => (
                        <div key={key} className="space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="text-gray-400 capitalize">{key}:</span>
                            <span className="font-semibold text-gray-200">{val.score}/10</span>
                          </div>
                          <p className="text-gray-500 text-[10px] leading-tight">{val.comment}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </motion.div>
              )}

              {/* Historical Similarity Score */}
              {breakdown.historical_similarity && (
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: 0.3 }}
                  className="bg-gray-800/50 rounded-lg p-4 border border-gray-700"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <TrendingUp width={14} height={14} strokeWidth={2} />
                      <span className="font-medium text-gray-200">Historical Consistency</span>
                    </div>
                    <Badge variant="secondary" className="bg-gray-700 text-gray-200 font-mono text-xs">
                      {Math.round(breakdown.historical_similarity.score)}/{breakdown.historical_similarity.max}
                    </Badge>
                  </div>
                  <Progress 
                    value={(breakdown.historical_similarity.score / breakdown.historical_similarity.max) * 100} 
                    className="h-1.5 mb-3"
                  />
                  {breakdown.historical_similarity.details && (
                    <div className="text-xs space-y-2">
                      {breakdown.historical_similarity.details.avg_similarity && (
                        <div className="flex justify-between">
                          <span className="text-gray-400">Similarity:</span>
                          <span className="font-medium text-gray-300">{breakdown.historical_similarity.details.avg_similarity}%</span>
                        </div>
                      )}
                      {breakdown.historical_similarity.details.consistency && (
                        <p className="text-gray-500 text-[10px] italic leading-tight">
                          {breakdown.historical_similarity.details.consistency}
                        </p>
                      )}
                    </div>
                  )}
                </motion.div>
              )}
            </div>
          )}

          {/* Methodology */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-gray-800/30 border border-gray-700 rounded-lg p-4"
          >
            <h4 className="font-medium text-gray-200 mb-2 flex items-center gap-2 text-sm">
              <Star width={14} height={14} strokeWidth={2} />
              Analysis Methodology
            </h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Powered by <span className="font-medium text-indigo-400">Google Gemini 2.5</span> for language quality assessment 
              and <span className="font-medium text-blue-400">SentenceTransformers</span> for historical similarity analysis.
            </p>
          </motion.div>
        </CardContent>
      </Card>
    </motion.div>
  );
}