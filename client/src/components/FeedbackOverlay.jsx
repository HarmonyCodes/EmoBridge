import React from 'react';
import { Sparkles, AlertCircle } from 'lucide-react';

const Confetti = () => (
  <div className="absolute inset-0 pointer-events-none overflow-hidden" aria-hidden="true">
    {[...Array(20)].map((_, i) => (
      <div
        key={i}
        className="absolute animate-bounce"
        style={{
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
          backgroundColor: ['#60A5FA', '#F472B6', '#FBBF24', '#34D399'][Math.floor(Math.random() * 4)],
          width: '10px',
          height: '10px',
          borderRadius: '50%',
          animationDuration: `${Math.random() * 2 + 1}s`,
          opacity: 0.6,
        }}
      />
    ))}
  </div>
);

const FeedbackOverlay = ({ message, isError, showConfetti }) => {
  if (!message) return null;

  return (
    <>
      <div
        role="alert"
        aria-live="assertive"
        className="absolute inset-0 flex items-center justify-center z-20 pointer-events-none px-4"
      >
        <div
          className={`
            ${isError
              ? 'bg-orange-100 border-orange-400 text-orange-700 dark:bg-orange-900 dark:border-orange-700 dark:text-orange-200'
              : 'bg-green-100 border-green-400 text-green-700 dark:bg-green-900 dark:border-green-700 dark:text-green-200'}
            px-10 py-5 rounded-3xl shadow-2xl border-4 animate-bounce text-center
          `}
        >
          <span className="text-4xl font-black flex items-center gap-3 justify-center">
            {isError
              ? <AlertCircle className="text-orange-500" aria-hidden="true" />
              : <Sparkles className="text-yellow-500" aria-hidden="true" />}
            {message}
          </span>
        </div>
      </div>
      {showConfetti && <Confetti />}
    </>
  );
};

export default FeedbackOverlay;
