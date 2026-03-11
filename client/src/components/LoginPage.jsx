import React, { useState } from 'react';
import { User, Lock, LogIn, Eye, EyeOff, Sun, Moon } from 'lucide-react';

const LoginPage = ({ onLogin, errorMessage, isDarkMode, onToggleDarkMode }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onLogin) onLogin({ username, password });
  };

  return (
    <div
      dir="rtl"
      className="min-h-screen bg-blue-50 dark:bg-slate-900 flex items-center justify-center px-4 transition-colors duration-500"
    >
      <div className="w-full max-w-md">

        {/* Logo */}
        <div className="text-center mb-10">
          <h1 className="text-6xl font-black tracking-tight mb-3 drop-shadow-md">
            <span className="text-blue-600 dark:text-blue-300">Emo</span>
            <span className="text-pink-500 dark:text-pink-400">Bridge</span>
          </h1>
          <div className="inline-block px-6 py-1 bg-white/50 dark:bg-slate-800/50 rounded-full">
            <p className="text-xl font-bold text-slate-600 dark:text-white">
              הגשר לרגש
            </p>
          </div>
        </div>

        {/* Card */}
        <div className="bg-white dark:bg-slate-800 rounded-[2rem] shadow-xl border-b-8 border-blue-200 dark:border-blue-900 px-8 py-10">
          <h2 className="text-2xl font-black text-slate-800 dark:text-white text-center mb-8">
            כניסה למערכת
          </h2>

          <form onSubmit={handleSubmit} className="flex flex-col gap-5">

            {/* Username */}
            <div className="flex flex-col gap-2">
              <label className="text-sm font-bold text-slate-600 dark:text-slate-300">
                שם משתמש
              </label>
              <div className="relative">
                <User
                  size={18}
                  className="absolute top-1/2 right-4 -translate-y-1/2 text-slate-400 dark:text-slate-500"
                />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="הכנס שם משתמש"
                  required
                  className="w-full pr-11 pl-4 py-3 rounded-2xl border-2 border-slate-200 dark:border-slate-600 bg-blue-50 dark:bg-slate-700 text-slate-800 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none focus:border-blue-400 dark:focus:border-blue-400 transition-colors"
                />
              </div>
            </div>

            {/* Password */}
            <div className="flex flex-col gap-2">
              <label className="text-sm font-bold text-slate-600 dark:text-slate-300">
                סיסמה
              </label>
              <div className="relative">
                <Lock
                  size={18}
                  className="absolute top-1/2 right-4 -translate-y-1/2 text-slate-400 dark:text-slate-500"
                />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="הכנס סיסמה"
                  required
                  className="w-full pr-11 pl-11 py-3 rounded-2xl border-2 border-slate-200 dark:border-slate-600 bg-blue-50 dark:bg-slate-700 text-slate-800 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none focus:border-blue-400 dark:focus:border-blue-400 transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute top-1/2 left-4 -translate-y-1/2 text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* Error message */}
            {errorMessage && (
              <p className="text-center text-sm font-bold text-red-500 dark:text-red-400 bg-red-50 dark:bg-red-900/20 rounded-xl py-2 px-4">
                {errorMessage}
              </p>
            )}

            {/* Submit */}
            <button
              type="submit"
              className="mt-2 w-full bg-blue-500 hover:bg-blue-600 active:translate-y-1 border-b-4 border-blue-700 active:border-b-0 text-white font-black text-lg py-3 rounded-2xl shadow-lg flex items-center justify-center gap-3 transition-all"
            >
              <LogIn size={22} />
              כניסה
            </button>

          </form>
        </div>

        {/* Dark mode toggle */}
        <div className="flex justify-center mt-6">
          <button
            onClick={onToggleDarkMode}
            className="bg-white/70 dark:bg-slate-800/70 px-6 py-3 rounded-2xl flex items-center gap-3 shadow border-2 border-blue-100 dark:border-blue-900/50 hover:border-blue-400 transition-all"
          >
            <span className="font-bold text-slate-800 dark:text-slate-100 text-sm">
              {isDarkMode ? 'מצב יום' : 'מצב לילה'}
            </span>
            {isDarkMode
              ? <Sun className="text-yellow-400" size={20} />
              : <Moon className="text-blue-400" size={20} />}
          </button>
        </div>

      </div>
    </div>
  );
};

export default LoginPage;
