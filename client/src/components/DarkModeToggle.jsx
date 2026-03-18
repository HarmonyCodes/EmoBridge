import React from 'react';
import { Sun, Moon } from 'lucide-react';

const DarkModeToggle = React.memo(({ isDarkMode, onToggle, compact = false }) => (
  <button
    onClick={onToggle}
    aria-label={isDarkMode ? 'עבור למצב יום' : 'עבור למצב לילה'}
    className={
      compact
        ? 'bg-white/70 dark:bg-slate-800/70 px-6 py-3 rounded-2xl flex items-center gap-3 shadow border-2 border-blue-100 dark:border-blue-900/50 hover:border-blue-400 transition-all'
        : 'bg-white dark:bg-slate-800 px-8 py-4 rounded-3xl flex items-center gap-4 shadow-lg border-2 border-blue-100 dark:border-blue-900/50 hover:border-blue-400 transition-all min-w-[200px] justify-between'
    }
  >
    <span className={`font-bold text-slate-800 dark:text-slate-100 ${compact ? 'text-sm' : 'text-lg'}`}>
      {isDarkMode ? 'מצב יום' : 'מצב לילה'}
    </span>
    {isDarkMode
      ? <Sun className="text-yellow-400" size={compact ? 20 : 28} />
      : <Moon className="text-blue-400" size={compact ? 20 : 28} />}
  </button>
));

export default DarkModeToggle;
