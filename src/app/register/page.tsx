'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import PatternLock from '@/components/PatternLock';
import { registerUser } from '@/app/actions/auth';

export default function RegisterPage() {
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [pattern, setPattern] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handlePatternComplete = (patternString: string) => {
    setPattern(patternString);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!pattern) {
      setError('Por favor dibuja tu patrón de bloqueo.');
      return;
    }

    setLoading(true);
    const formData = new FormData(e.currentTarget);

    const res = await registerUser(formData, pattern);

    if (res.success) {
      setSuccess('¡Registro exitoso! Redirigiendo al login...');
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } else {
      setError(res.error || 'Ocurrió un error inesperado.');
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-[#FFFDF9] p-6 selection:bg-orange-200 selection:text-orange-900 font-sans">
      <div className="w-full max-w-md bg-white border-4 border-orange-100 rounded-[2.5rem] p-8 shadow-xl relative overflow-hidden">
        {/* Círculos decorativos */}
        <div className="absolute -top-10 -right-10 w-24 h-24 bg-pink-100 rounded-full opacity-50 blur-xl"></div>
        <div className="absolute -bottom-10 -left-10 w-24 h-24 bg-orange-100 rounded-full opacity-50 blur-xl"></div>

        <div className="flex flex-col items-center mb-6 relative">
          <img src="/assets/icon.jpg" alt="Susanahoria" className="w-20 h-20 rounded-[1.5rem] shadow-md border-4 border-orange-200 mb-3" />
          <h1 className="text-2xl font-black text-[#FF5A1F] tracking-tight">Registro de Equipo</h1>
          <p className="text-xs text-pink-500 font-bold -mt-0.5">Únete al canal de Susanahoria</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 relative">
          <div>
            <label htmlFor="name" className="block text-xs font-black uppercase text-[#4E3F3F] mb-1.5 tracking-wider">
              Nombre Completo
            </label>
            <input
              type="text"
              name="name"
              id="name"
              required
              className="w-full px-4 py-3 rounded-2xl border-2 border-orange-100 bg-[#FFFBF5] text-[#2F1F1F] placeholder-zinc-400 focus:ring-2 focus:ring-[#FF5A1F] focus:border-[#FF5A1F] outline-none transition text-sm font-semibold"
              placeholder="Ej. Juan Pérez"
            />
          </div>

          <div>
            <label htmlFor="id" className="block text-xs font-black uppercase text-[#4E3F3F] mb-1.5 tracking-wider">
              Cédula (ID Único)
            </label>
            <input
              type="text"
              name="id"
              id="id"
              required
              className="w-full px-4 py-3 rounded-2xl border-2 border-orange-100 bg-[#FFFBF5] text-[#2F1F1F] placeholder-zinc-400 focus:ring-2 focus:ring-[#FF5A1F] focus:border-[#FF5A1F] outline-none transition text-sm font-semibold"
              placeholder="Ej. 104523456"
            />
          </div>

          <div className="flex flex-col items-center py-1">
            <span className="block text-xs font-black uppercase text-[#4E3F3F] mb-2 self-start tracking-wider">
              Dibuja tu patrón de acceso (mínimo 3 puntos)
            </span>
            <PatternLock onComplete={handlePatternComplete} />
          </div>

          {error && <p className="text-xs font-bold text-red-600 bg-red-50 border border-red-100 px-4 py-3 rounded-xl text-center">{error}</p>}
          {success && <p className="text-xs font-bold text-green-600 bg-green-50 border border-green-100 px-4 py-3 rounded-xl text-center">{success}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 rounded-2xl bg-[#FF5A1F] hover:bg-[#E04810] disabled:bg-orange-800 text-white font-black transition shadow-md shadow-orange-500/10 hover:scale-[1.01]"
          >
            {loading ? 'Registrando...' : 'Completar Registro 🥕'}
          </button>
        </form>

        <p className="text-center text-xs text-[#5E4F4F] mt-6 font-semibold relative">
          ¿Ya tienes cuenta?{' '}
          <a href="/login" className="text-[#FF5A1F] hover:underline font-bold">
            Inicia sesión aquí
          </a>
        </p>
      </div>
    </main>
  );
}