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
    <main className="min-h-screen flex flex-col items-center justify-center bg-[#FFFDF9] p-6 selection:bg-orange-200 selection:text-orange-900 font-sans">
      <div className="w-full max-w-md bg-white border-4 border-orange-100 rounded-[2.5rem] p-8 shadow-xl relative overflow-hidden">
        {/* Círculos decorativos de fondo en colores pastel */}
        <div className="absolute -top-10 -right-10 w-24 h-24 bg-pink-100 rounded-full opacity-50 blur-xl"></div>
        <div className="absolute -bottom-10 -left-10 w-24 h-24 bg-orange-100 rounded-full opacity-50 blur-xl"></div>

        <div className="flex flex-col items-center mb-6 relative">
          <img src="/assets/icon.jpg" alt="Susanahoria" className="w-20 h-20 rounded-[1.5rem] shadow-md border-4 border-orange-200 mb-3" />
          <h1 className="text-2xl font-black text-[#FF5A1F] tracking-tight">Acceso Privado</h1>
          <p className="text-xs text-pink-500 font-bold -mt-0.5">Equipo de Susanahoria</p>
        </div>

        <div className="space-y-4 relative">
          <div>
            <label htmlFor="id" className="block text-xs font-black uppercase text-[#4E3F3F] mb-1.5 tracking-wider">
              Cédula de Identidad
            </label>
            <input
              type="text"
              name="id"
              id="id"
              value={id}
              onChange={(e) => setId(e.target.value)}
              required
              className="w-full px-4 py-3 rounded-2xl border-2 border-orange-100 bg-[#FFFBF5] text-[#2F1F1F] placeholder-zinc-400 focus:ring-2 focus:ring-[#FF5A1F] focus:border-[#FF5A1F] outline-none transition text-sm font-semibold"
              placeholder="Ingresa tu número de cédula"
            />
          </div>

          <div className="flex flex-col items-center py-1">
            <span className="block text-xs font-black uppercase text-[#4E3F3F] mb-2 self-start tracking-wider">
              Dibuja tu patrón para ingresar
            </span>
            <PatternLock onComplete={handlePatternComplete} />
          </div>

          {error && <p className="text-xs font-bold text-red-600 bg-red-50 border border-red-100 px-4 py-3 rounded-xl text-center">{error}</p>}
          {success && <p className="text-xs font-bold text-green-600 bg-green-50 border border-green-100 px-4 py-3 rounded-xl text-center">{success}</p>}
        </div>

        <p className="text-center text-xs text-[#5E4F4F] mt-6 font-semibold relative">
          ¿No tienes una cuenta?{' '}
          <a href="/register" className="text-[#FF5A1F] hover:underline font-bold">
            Regístrate aquí
          </a>
        </p>
      </div>
    </main>
  );
}