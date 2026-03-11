import React from 'react';

const Header = () => (
  <header className="pt-16 pb-8 text-center">
    <h1 className="text-6xl md:text-7xl font-black tracking-tight mb-3 drop-shadow-md">
      <span className="text-blue-600 dark:text-blue-300">Emo</span>
      <span className="text-pink-500 dark:text-pink-400">Bridge</span>
    </h1>
    <div className="inline-block px-6 py-1 bg-white/50 dark:bg-slate-800/50 rounded-full">
      <p className="text-2xl font-bold text-slate-600 dark:text-white">
        הגשר לרגש
      </p>
    </div>
  </header>
);

export default Header;
