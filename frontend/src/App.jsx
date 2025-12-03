import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import Header from './components/Header';
import ActionButtons from './components/ActionButtons';
import MetricsCard from './components/MetricsCard';
import ReportCard from './components/ReportCard';
import ValidationCard from './components/ValidationCard';
import StyleScoreCard from './components/StyleScoreCard';
import { Toaster } from './lib/toast';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 5 * 60 * 1000,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 1,
    },
  },
});

function App() {
  const [metrics, setMetrics] = useState(null);
  const [report, setReport] = useState('');
  const [validation, setValidation] = useState(null);
  const [styleScore, setStyleScore] = useState(null);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-slate-900">
        {/* Animated Background Pattern */}
        <div className="fixed inset-0 -z-10 overflow-hidden">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-gradient-to-br from-indigo-600/20 to-purple-600/20 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-gradient-to-br from-blue-600/20 to-cyan-600/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        </div>

        <Header />
        
        <main className="container mx-auto px-4 sm:px-6 py-8 space-y-8 max-w-[1600px]">
          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <ActionButtons
              setMetrics={setMetrics}
              setReport={setReport}
              setValidation={setValidation}
              setStyleScore={setStyleScore}
              metrics={metrics}
              report={report}
            />
          </motion.div>

          {/* Results Grid */}
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 lg:gap-8">
            {/* Left Column */}
            <div className="space-y-6 lg:space-y-8">
              <MetricsCard metrics={metrics} />
              <ValidationCard validation={validation} />
            </div>
            
            {/* Right Column */}
            <div className="space-y-6 lg:space-y-8">
              <ReportCard 
                report={report} 
                setReport={setReport}
                metrics={metrics}
              />
              <StyleScoreCard styleScore={styleScore} />
            </div>
          </div>
        </main>

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.8 }}
          className="border-t border-slate-200 bg-white/60 backdrop-blur-md mt-20"
        >
          <div className="container mx-auto px-6 py-8">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              <p className="text-slate-600 text-sm font-medium">
                AI Quarterly Report Studio
              </p>
              <div className="flex items-center gap-3 text-xs text-slate-500">
                <span>Powered by</span>
                <span className="px-3 py-1 bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700 font-semibold rounded-full">
                  Gemini 2.5
                </span>
              </div>
            </div>
          </div>
        </motion.footer>

        <Toaster />
      </div>
    </QueryClientProvider>
  );
}

export default App;