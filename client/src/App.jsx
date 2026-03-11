import React, { useState, useEffect } from 'react';
import { Heart, Star, Sparkles, User, Sun, Moon, LogOut } from 'lucide-react';

import Header from './components/Header';
import EmotionCard from './components/EmotionCard';
import FeedbackOverlay from './components/FeedbackOverlay';
import LoginPage from './components/LoginPage';
import emotions from './mocks/emotions.json';
import users from './mocks/users.json';

const successMessages = ['כל הכבוד!', 'נכון מאוד!', 'יפה מאוד!', 'מצוין!', 'אתה אלוף!', 'איזו הצלחה!'];
const errorMessages = ['לא נורא', 'אולי בפעם הבאה', 'נסה שוב', 'כמעט!', 'בוא ננסה עוד פעם'];

const TARGET_EMOTION = 'שמח';

const pickRoundEmotions = () => {
  const target = emotions.find((e) => e.name === TARGET_EMOTION);
  const distractors = emotions
    .filter((e) => e.name !== TARGET_EMOTION)
    .sort(() => Math.random() - 0.5)
    .slice(0, 3);
  return [...distractors, target].sort(() => Math.random() - 0.5);
};

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [loginError, setLoginError] = useState('');

  const [feedback, setFeedback] = useState(null);
  const [isError, setIsError] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [roundEmotions, setRoundEmotions] = useState(() => pickRoundEmotions());

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDarkMode);
  }, [isDarkMode]);

  const handleLogin = ({ username, password }) => {
    const match = users.find(
      (u) => u.username === username && u.password === password
    );
    if (match) {
      setCurrentUser(match);
      setIsLoggedIn(true);
      setLoginError('');
    } else {
      setLoginError('שם משתמש או סיסמה שגויים');
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentUser(null);
    setFeedback(null);
    setShowConfetti(false);
    setIsError(false);
    setRoundEmotions(pickRoundEmotions());
  };

  const handleEmotionClick = (emotion) => {
    if (emotion.name === TARGET_EMOTION) {
      setFeedback(successMessages[Math.floor(Math.random() * successMessages.length)]);
      setIsError(false);
      setShowConfetti(true);
    } else {
      setFeedback(errorMessages[Math.floor(Math.random() * errorMessages.length)]);
      setIsError(true);
      setShowConfetti(false);
    }

    setTimeout(() => {
      setFeedback(null);
      setShowConfetti(false);
      setIsError(false);
      setRoundEmotions(pickRoundEmotions());
    }, 2500);
  };

  if (!isLoggedIn) {
    return (
      <LoginPage
        onLogin={handleLogin}
        errorMessage={loginError}
        isDarkMode={isDarkMode}
        onToggleDarkMode={() => setIsDarkMode(!isDarkMode)}
      />
    );
  }

  return (
    <div
      dir="rtl"
      className="min-h-screen transition-colors duration-500 font-sans bg-blue-50 dark:bg-slate-900"
    >
      <Header />

      {/* Logout button */}
      <div className="absolute top-6 left-6">
        <button
          onClick={handleLogout}
          className="bg-white dark:bg-slate-800 px-5 py-3 rounded-2xl flex items-center gap-2 shadow-lg border-b-4 border-red-200 dark:border-red-900/60 hover:border-red-400 active:translate-y-1 active:border-b-0 transition-all"
        >
          <LogOut size={18} className="text-red-400" />
          <span className="font-bold text-slate-800 dark:text-slate-100 text-sm">
            {currentUser?.username} | התנתק
          </span>
        </button>
      </div>

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

        {/* Emotion Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 w-full max-w-2xl px-2">
          {roundEmotions.map((emotion) => (
            <EmotionCard
              key={emotion.id}
              emoji={emotion.emoji}
              name={emotion.name}
              color={emotion.color}
              onClick={() => handleEmotionClick(emotion)}
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
              {isDarkMode ? 'מצב יום' : 'מצב לילה'}
            </span>
            {isDarkMode
              ? <Sun className="text-yellow-400" size={28} />
              : <Moon className="text-blue-400" size={28} />}
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
