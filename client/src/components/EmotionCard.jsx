import React, { useCallback } from 'react';

const EmotionCard = React.memo(({ emoji, name, color, onSelect }) => {
  const handleClick = useCallback(() => onSelect(name), [onSelect, name]);

  return (
    <button
      onClick={handleClick}
      aria-label={`בחר רגש: ${name}`}
      className={`${color} aspect-square border-b-8 active:border-b-0 active:translate-y-2 transition-all rounded-[2rem] flex flex-col items-center justify-center gap-3 shadow-xl group`}
    >
      <span className="text-5xl md:text-6xl group-hover:scale-110 transition-transform duration-200" aria-hidden="true">
        {emoji}
      </span>
      <span className="text-lg md:text-xl font-black text-slate-800 dark:text-slate-100">
        {name}
      </span>
    </button>
  );
});

EmotionCard.displayName = 'EmotionCard';

export default EmotionCard;
