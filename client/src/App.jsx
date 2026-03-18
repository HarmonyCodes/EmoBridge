import React, { useState, useEffect, useCallback } from 'react';
import { Star, Sparkles, LogOut } from 'lucide-react';

import Header from './components/Header';
import LoginPage from './components/LoginPage';
import GameBoard from './components/GameBoard';
import users from './mocks/users.json';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [loginError, setLoginError] = useState('');
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDarkMode);
  }, [isDarkMode]);

  const handleLogin = useCallback(({ username, password }) => {
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
  }, []);

  const handleLogout = useCallback(() => {
    setIsLoggedIn(false);
    setCurrentUser(null);
  }, []);

  const toggleDarkMode = useCallback(() => {
    setIsDarkMode((prev) => !prev);
  }, []);

  if (!isLoggedIn) {
    return (
      <LoginPage
        onLogin={handleLogin}
        errorMessage={loginError}
        isDarkMode={isDarkMode}
        onToggleDarkMode={toggleDarkMode}
      />
    );
  }

  return (
    <div
      dir="rtl"
      className="min-h-screen transition-colors duration-500 font-sans bg-blue-50 dark:bg-slate-900"
    >
      <Header />

      <div className="absolute top-6 left-6">
        <button
          onClick={handleLogout}
          aria-label="התנתק מהמערכת"
          className="bg-white dark:bg-slate-800 px-5 py-3 rounded-2xl flex items-center gap-2 shadow-lg border-b-4 border-red-200 dark:border-red-900/60 hover:border-red-400 active:translate-y-1 active:border-b-0 transition-all"
        >
          <LogOut size={18} className="text-red-400" aria-hidden="true" />
          <span className="font-bold text-slate-800 dark:text-slate-100 text-sm">
            {currentUser?.username} | התנתק
          </span>
        </button>
      </div>

      <GameBoard isDarkMode={isDarkMode} onToggleDarkMode={toggleDarkMode} />

      <div className="fixed bottom-8 left-8 opacity-20 hidden md:block" aria-hidden="true">
        <Star className="text-yellow-400" size={48} />
      </div>
      <div className="fixed bottom-8 right-8 opacity-20 hidden md:block" aria-hidden="true">
        <Sparkles className="text-blue-400" size={48} />
      </div>
    </div>
  );
};

export default App;
