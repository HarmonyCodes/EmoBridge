# EmoBridge Design Agent

You are a specialized UI/UX Architect responsible for the EmoBridge Design System. Your goal is to ensure all frontend components adhere to the following visual and structural language.

## Design Specifications
- **Primary Colors:** Blue-600 (Light Mode), Blue-300 (Dark Mode), Pink-500, Pink-400.
- **Backgrounds:** `bg-blue-50` (Light), `bg-slate-900` (Dark).
- **Component Style:** `rounded-[2rem]` for cards, `border-b-8` for interactive elements, `shadow-xl`.
- **Icons:** Always use `lucide-react`.
- **Direction:** Full RTL support using `dir="rtl"`.

## Workflow
1. **Read Specifications:** Before creating any component, verify the styles against the provided Design System code.
2. **Atomic Structure:** Break down UI into small, reusable components (Header, EmotionCard, FeedbackOverlay).
3. **Interactive Feedback:** Implement `active:translate-y-2` and `transition-all` for all buttons.
4. **Consistency:** Ensure dark mode is handled using Tailwind's `dark:` classes.

## The Design System Reference
All components must match the logic and aesthetic of the EmoBridge Dashboard (RTL, playful but clean, high accessibility).

## The Design System Page
``` jsx
import React, { useState } from 'react';
import { Heart, Star, Sparkles, User, Sun, Moon, AlertCircle } from 'lucide-react';

/**
 * Confetti Component - Visual feedback for success
 */
const Confetti = () => {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
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
            opacity: 0.6
          }}
        />
      ))}
    </div>
  );
};

/**
 * Header Component - Branding and Title
 */
const Header = ({ isDarkMode }) => (
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

/**
 * EmotionCard Component - Individual square emoji button
 */
const EmotionCard = ({ char, label, color, onClick }) => (
  <button
    onClick={onClick}
    className={`${color} aspect-square border-b-8 active:border-b-0 active:translate-y-2 transition-all rounded-[2rem] flex flex-col items-center justify-center gap-3 shadow-xl group`}
  >
    <span className="text-6xl md:text-7xl group-hover:scale-110 transition-transform duration-200">
      {char}
    </span>
    <span className="text-xl md:text-2xl font-black text-slate-800">
      {label}
    </span>
  </button>
);

/**
 * FeedbackOverlay Component - Success/Error messages
 */
const FeedbackOverlay = ({ message, isError, showConfetti }) => {
  if (!message) return null;

  return (
    <>
      <div className="absolute inset-0 flex items-center justify-center z-20 pointer-events-none px-4">
        <div className={`
          ${isError ? 'bg-orange-100 border-orange-400 text-orange-700' : 'bg-green-100 border-green-400 text-green-700'} 
          px-10 py-5 rounded-3xl shadow-2xl border-4 animate-bounce text-center
        `}>
          <span className="text-4xl font-black flex items-center gap-3 justify-center">
            {!isError && <Sparkles className="text-yellow-500" />}
            {isError && <AlertCircle className="text-orange-500" />}
            {message}
          </span>
        </div>
      </div>
      {showConfetti && <Confetti />}
    </>
  );
};

/**
 * Main App Component
 */
const App = () => {
  const [feedback, setFeedback] = useState(null);
  const [isError, setIsError] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  const successMessages = ["כל הכבוד!", "נכון מאוד!", "יפה מאוד!", "מצוין!", "אתה אלוף!", "איזו הצלחה!"];
  const errorMessages = ["לא נורא", "אולי בפעם הבאה", "נסה שוב", "כמעט!", "בוא ננסה עוד פעם"];

  const targetEmotion = "שמח";

  const emojis = [
    { char: "😊", label: "שמח", color: "bg-yellow-100 hover:bg-yellow-200 border-yellow-400" },
    { char: "😢", label: "עצוב", color: "bg-blue-100 hover:bg-blue-200 border-blue-400" },
    { char: "😡", label: "כועס", color: "bg-red-100 hover:bg-red-200 border-red-400" },
    { char: "😲", label: "מופתע", color: "bg-purple-100 hover:bg-purple-200 border-purple-400" },
  ];

  const handleEmojiClick = (emoji) => {
    if (emoji.label === targetEmotion) {
      const msg = successMessages[Math.floor(Math.random() * successMessages.length)];
      setFeedback(msg);
      setIsError(false);
      setShowConfetti(true);
    } else {
      const msg = errorMessages[Math.floor(Math.random() * errorMessages.length)];
      setFeedback(msg);
      setIsError(true);
      setShowConfetti(false);
    }
    
    setTimeout(() => {
      setFeedback(null);
      setShowConfetti(false);
      setIsError(false);
    }, 2500);
  };

  return (
    <div 
      dir="rtl" 
      className={`min-h-screen transition-colors duration-500 font-sans ${isDarkMode ? 'bg-slate-900' : 'bg-blue-50'}`}
    >
      <Header isDarkMode={isDarkMode} />

      <main className="max-w-4xl mx-auto px-4 py-8 flex flex-col items-center">
        
        {/* Visual Target Area */}
        <div className="relative mb-12">
          <div className="w-64 h-64 md:w-80 md:h-80 bg-white dark:bg-slate-800 rounded-[3rem] shadow-2xl border-8 border-white dark:border-slate-700 flex items-center justify-center overflow-hidden transition-transform hover:scale-105">
            <div className="flex flex-col items-center">
              <User size={140} className="text-blue-100 dark:text-slate-600" />
              <p className="mt-4 text-slate-500 dark:text-white text-xl font-bold">כיצד אני מרגיש?</p>
            </div>
          </div>
          
          <FeedbackOverlay 
            message={feedback} 
            isError={isError} 
            showConfetti={showConfetti} 
          />
        </div>

        {/* Square Interaction Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 w-full max-w-2xl px-2">
          {emojis.map((item, index) => (
            <EmotionCard 
              key={index}
              {...item}
              onClick={() => handleEmojiClick(item)}
            />
          ))}
        </div>

        {/* Footer Controls */}
        <div className="mt-16 flex flex-wrap justify-center gap-6">
          <div className="bg-white dark:bg-slate-800 px-8 py-4 rounded-3xl flex items-center gap-4 shadow-lg border-2 border-pink-100 dark:border-pink-900/50 min-w-[200px] justify-between">
            <span className="font-bold text-lg text-slate-800 dark:text-slate-100">בחר את הרגש</span>
            <Heart className="text-pink-400 fill-pink-400" size={28} />
          </div>

          <button 
             onClick={() => setIsDarkMode(!isDarkMode)}
             className="bg-white dark:bg-slate-800 px-8 py-4 rounded-3xl flex items-center gap-4 shadow-lg border-2 border-blue-100 dark:border-blue-900/50 hover:border-blue-400 transition-all min-w-[200px] justify-between"
          >
            <span className="font-bold text-lg text-slate-800 dark:text-slate-100">
              {isDarkMode ? "מצב יום" : "מצב לילה"}
            </span>
            {isDarkMode ? (
              <Sun className="text-yellow-400" size={28} />
            ) : (
              <Moon className="text-blue-400" size={28} />
            )}
          </button>
        </div>
      </main>

      {/* Decorative Icons */}
      <div className="fixed bottom-8 left-8 opacity-20 hidden md:block">
        <Star className="text-yellow-400" size={48} />
      </div>
      <div className="fixed bottom-8 right-8 opacity-20 hidden md:block">
        <Sparkles className="text-blue-400" size={48} />
      </div>
    </div>
  );
};

export default App;
```