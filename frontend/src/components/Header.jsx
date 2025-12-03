import { motion } from 'framer-motion';
import { TrendingUp, Zap, Shield } from 'lucide-react';

export default function Header() {
  return (
    <motion.header 
      className="w-full border-b border-gray-800 bg-gradient-to-r from-gray-900 via-gray-900 to-gray-900 shadow-lg"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="container mx-auto px-6 py-10">
        <div className="flex items-center justify-center mb-4">
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.1, type: "spring" }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 rounded-2xl blur-xl opacity-30 animate-pulse" />
            <div className="relative bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-700 p-4 rounded-2xl shadow-lg">
              <TrendingUp className="text-white" width={32} height={32} strokeWidth={2} />
            </div>
          </motion.div>
        </div>
        
        <motion.h1 
          className="text-4xl md:text-5xl lg:text-6xl font-black text-center bg-gradient-to-r from-indigo-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          AI Quarterly Report Studio
        </motion.h1>
        
        <motion.p 
          className="text-center text-gray-300 mt-4 text-base md:text-lg max-w-3xl mx-auto leading-relaxed"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          Enterprise-grade financial report generation powered by <span className="font-semibold text-indigo-400">Google Gemini 2.5</span>
          {' '}• Advanced validation • Style analysis
        </motion.p>
        
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="flex items-center justify-center gap-8 mt-6"
        >
          <div className="flex items-center gap-2 text-sm text-gray-300">
            <Zap className="text-purple-400" width={16} height={16} strokeWidth={2} />
            <span className="font-medium">AI-Powered</span>
          </div>
          <div className="h-4 w-px bg-gray-600" />
          <div className="flex items-center gap-2 text-sm text-gray-300">
            <Shield className="text-indigo-400" width={16} height={16} strokeWidth={2} />
            <span className="font-medium">Validated</span>
          </div>
          <div className="h-4 w-px bg-gray-600" />
          <div className="flex items-center gap-2 text-sm text-gray-300">
            <TrendingUp className="text-blue-400" width={16} height={16} strokeWidth={2} />
            <span className="font-medium">Market Reports</span>
          </div>
        </motion.div>
      </div>
    </motion.header>
  );
}