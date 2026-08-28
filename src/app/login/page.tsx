'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import PatternLock from '@/components/PatternLock';
import { loginUser } from '@/app/actions/auth';

export default function LoginPage() {
  const [id, setId] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handlePatternComplete = async (patternString: string) => {
    setError('');
    setSuccess('');

    if (!id) {
      setError('Por favor, ingresa tu cédula primero.');
      return;
    }

    setLoading(true);
    const res = await loginUser(id, patternString);

    if (res.success) {
      setSuccess(`¡Hola ${res.name}! Redirigiendo al panel...`);
      setTimeout(() => {
        router.push('/dashboard');
      }, 1500);
    } else {
      setError(res.error || 'Credenciales incorrectas.');
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-zinc-50 dark:bg-zinc-950 p-6">
      <div className="w-full max-w-md bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl p-8 shadow-sm">
        <div className="flex flex-col items-center mb-6">
          <img src="/assets/icon.jpg" alt="Susanahoria" className="w-20 h-20 rounded-2xl shadow-sm border border-orange-200 mb-3" />
          <h1 className="text-2xl font-bold text-zinc-950 dark:text-zinc-50">Susanahoria</h1>
          <p className="text-sm text-zinc-500 mt-1">Panel de control táctil</p>
        </div>

        <div className="space-y-4">
          <div>
            <label htmlFor="id" className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">
              Cédula
            </label>
            <input
              type="text"
              name="id"
              id="id"
              value={id}
              onChange={(e) => setId(e.target.value)}
              required
              className="w-full px-4 py-3 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 text-zinc-950 dark:text-zinc-50 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none transition"
              placeholder="Ingresa tu cédula"
            />
          </div>

          <div className="flex flex-col items-center py-2">
            <span className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2 self-start">
              Dibuja tu patrón para ingresar
            </span>
            <PatternLock onComplete={handlePatternComplete} />
          </div>

          {error && <p className="text-sm text-red-500 bg-red-50 dark:bg-red-950/20 px-4 py-2 rounded-xl text-center">{error}</p>}
          {success && <p className="text-sm text-green-500 bg-green-50 dark:bg-green-950/20 px-4 py-2 rounded-xl text-center">{success}</p>}
        </div>

        <p className="text-center text-sm text-zinc-500 mt-6">
          ¿Eres nuevo?{' '}
          <a href="/register" className="text-orange-600 hover:underline font-medium">
            Regístrate aquí
          </a>
        </p>
      </div>
    </main>
  );
}