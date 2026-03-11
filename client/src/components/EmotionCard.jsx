import React from 'react';

const EmotionCard = ({ emoji, name, color, onClick }) => (
  <button
    onClick={onClick}
    className={`${color} aspect-square border-b-8 active:border-b-0 active:translate-y-2 transition-all rounded-[2rem] flex flex-col items-center justify-center gap-3 shadow-xl group`}
  >
    <span className="text-5xl md:text-6xl group-hover:scale-110 transition-transform duration-200">
      {emoji}
    </span>
    <span className="text-lg md:text-xl font-black text-slate-800">
      {name}
    </span>
  </button>
);

export default EmotionCard;
