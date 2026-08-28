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
    <main className="min-h-screen flex flex-col items-center justify-center bg-zinc-50 dark:bg-zinc-950 p-6">
      <div className="w-full max-w-md bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl p-8 shadow-sm">
        <div className="flex flex-col items-center mb-6">
          <img src="/assets/icon.jpg" alt="Susanahoria" className="w-20 h-20 rounded-2xl shadow-sm border border-orange-200 mb-3" />
          <h1 className="text-2xl font-bold text-zinc-950 dark:text-zinc-50">Registro de Equipo</h1>
          <p className="text-sm text-zinc-500 mt-1">Únete al panel de Susanahoria</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">
              Nombre Completo
            </label>
            <input
              type="text"
              name="name"
              id="name"
              required
              className="w-full px-4 py-3 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 text-zinc-950 dark:text-zinc-50 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none transition"
              placeholder="Ej. Juan Pérez"
            />
          </div>

          <div>
            <label htmlFor="id" className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">
              Cédula (ID Único)
            </label>
            <input
              type="text"
              name="id"
              id="id"
              required
              className="w-full px-4 py-3 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 text-zinc-950 dark:text-zinc-50 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none transition"
              placeholder="Ej. 104523456"
            />
          </div>

          <div className="flex flex-col items-center py-2">
            <span className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2 self-start">
              Dibuja tu patrón de acceso (mínimo 3 puntos)
            </span>
            <PatternLock onComplete={handlePatternComplete} />
          </div>

          {error && <p className="text-sm text-red-500 bg-red-50 dark:bg-red-950/20 px-4 py-2 rounded-xl text-center">{error}</p>}
          {success && <p className="text-sm text-green-500 bg-green-50 dark:bg-green-950/20 px-4 py-2 rounded-xl text-center">{success}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 rounded-2xl bg-orange-600 hover:bg-orange-500 disabled:bg-orange-800 text-white font-semibold transition shadow-md"
          >
            {loading ? 'Registrando...' : 'Completar Registro'}
          </button>
        </form>

        <p className="text-center text-sm text-zinc-500 mt-6">
          ¿Ya tienes cuenta?{' '}
          <a href="/login" className="text-orange-600 hover:underline font-medium">
            Inicia sesión aquí
          </a>
        </p>
      </div>
    </main>
  );
}