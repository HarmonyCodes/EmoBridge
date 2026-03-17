import React from 'react';
import { Heart, User } from 'lucide-react';

import EmotionCard from './EmotionCard';
import FeedbackOverlay from './FeedbackOverlay';
import DarkModeToggle from './DarkModeToggle';
import useGameRound from '../hooks/useGameRound';

const GameBoard = ({ isDarkMode, onToggleDarkMode }) => {
  const { roundEmotions, feedback, isError, showConfetti, handleEmotionClick } = useGameRound();

  return (
    <main className="max-w-4xl mx-auto px-4 py-8 flex flex-col items-center">

      {/* Visual Target Area */}
      <div className="relative mb-12">
        <div className="w-64 h-64 md:w-80 md:h-80 bg-white dark:bg-slate-800 rounded-[3rem] shadow-2xl border-8 border-white dark:border-slate-700 flex items-center justify-center overflow-hidden transition-transform hover:scale-105">
          <div className="flex flex-col items-center">
            <User size={140} className="text-blue-100 dark:text-slate-600" aria-hidden="true" />
            <p className="mt-4 text-slate-500 dark:text-white text-xl font-bold">כיצד אני מרגיש?</p>
          </div>
        </div>

        <FeedbackOverlay
          message={feedback}
          isError={isError}
          showConfetti={showConfetti}
        />
      </div>

      {/* Emotion Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 w-full max-w-2xl px-2" role="group" aria-label="בחירת רגש">
        {roundEmotions.map((emotion) => (
          <EmotionCard
            key={emotion.id}
            emoji={emotion.emoji}
            name={emotion.name}
            color={emotion.color}
            onSelect={handleEmotionClick}
          />
        ))}
      </div>

      {/* Footer Controls */}
      <div className="mt-16 flex flex-wrap justify-center gap-6">
        <div className="bg-white dark:bg-slate-800 px-8 py-4 rounded-3xl flex items-center gap-4 shadow-lg border-2 border-pink-100 dark:border-pink-900/50 min-w-[200px] justify-between">
          <span className="font-bold text-lg text-slate-800 dark:text-slate-100">בחר את הרגש</span>
          <Heart className="text-pink-400 fill-pink-400" size={28} aria-hidden="true" />
        </div>

        <DarkModeToggle isDarkMode={isDarkMode} onToggle={onToggleDarkMode} />
      </div>
    </main>
  );
};

export default GameBoard;
