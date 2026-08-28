'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getCurrentUser, getScripts, createScript, logout } from '@/app/actions/scripts';

interface User {
  id: string;
  name: string;
  role: string;
}

interface Script {
  id: string;
  title: string;
  scheduledDate: string;
  videoType: string;
  theme: string;
  materials: string;
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [scripts, setScripts] = useState<Script[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formLoading, setFormLoading] = useState(false);
  const router = useRouter();

  // Carga inicial de datos de sesión y guiones
  const loadData = async () => {
    setLoading(true);
    const currentUser = await getCurrentUser();
    if (!currentUser) {
      router.push('/login');
      return;
    }
    setUser(currentUser as User);

    const allScripts = await getScripts();
    setScripts(allScripts as Script[]);
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setFormLoading(true);

    const form = e.currentTarget;
    const formData = new FormData(form);

    const res = await createScript(formData);

    if (res.success) {
      form.reset();
      // Recargar la agenda de guiones desde la base de datos
      const updatedScripts = await getScripts();
      setScripts(updatedScripts as Script[]);
    } else {
      setError(res.error || 'Error al añadir guion.');
    }
    setFormLoading(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-zinc-950 text-orange-500">
        <div className="text-center font-semibold">Cargando panel de Susanahoria...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col">
      {/* Cabecera / Navbar */}
      <header className="border-b border-zinc-800 bg-zinc-900/50 backdrop-blur sticky top-0 z-40 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <img src="/assets/icon.jpg" alt="Susanahoria" className="w-10 h-10 rounded-xl" />
          <div>
            <h1 className="text-md font-bold tracking-tight text-white">Susanahoria CMS</h1>
            <p className="text-xs text-zinc-500">Agenda & Logística de Contenido</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden sm:flex flex-col items-end">
            <span className="text-sm font-semibold text-white">{user?.name}</span>
            <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full ${
              user?.role === 'ADMIN' ? 'bg-orange-500/10 text-orange-500 border border-orange-500/20' : 'bg-zinc-800 text-zinc-400'
            }`}>
              {user?.role}
            </span>
          </div>
          <button
            onClick={handleLogout}
            className="text-xs font-semibold px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-xl transition"
          >
            Salir
          </button>
        </div>
      </header>

      {/* Contenedor Principal */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Lado Izquierdo: Formulario de adición de guion (Solo para ADMIN) */}
        {user?.role === 'ADMIN' && (
          <section className="lg:col-span-4 bg-zinc-900 border border-zinc-800 rounded-3xl p-6 self-start shadow-xl">
            <h2 className="text-lg font-bold text-white mb-1">Añadir Nuevo Guion</h2>
            <p className="text-xs text-zinc-500 mb-6">Planifica los temas y requerimientos para el equipo</p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold uppercase text-zinc-400 mb-1">Título del Video</label>
                <input
                  type="text"
                  name="title"
                  required
                  placeholder="Ej. Receta de Zanahoria Crujiente"
                  className="w-full px-4 py-2.5 rounded-xl border border-zinc-800 bg-zinc-950 text-white placeholder-zinc-600 focus:ring-2 focus:ring-orange-500 outline-none transition text-sm"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold uppercase text-zinc-400 mb-1">Fecha</label>
                  <input
                    type="date"
                    name="scheduledDate"
                    required
                    className="w-full px-4 py-2.5 rounded-xl border border-zinc-800 bg-zinc-950 text-white focus:ring-2 focus:ring-orange-500 outline-none transition text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase text-zinc-400 mb-1">Tipo</label>
                  <select
                    name="videoType"
                    required
                    className="w-full px-4 py-2.5 rounded-xl border border-zinc-800 bg-zinc-950 text-white focus:ring-2 focus:ring-orange-500 outline-none transition text-sm"
                  >
                    <option value="SHORT">Short (Vertical)</option>
                    <option value="HORIZONTAL">Horizontal</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase text-zinc-400 mb-1">Tema / Idea Central</label>
                <input
                  type="text"
                  name="theme"
                  required
                  placeholder="Ej. Cocina rápida saludable"
                  className="w-full px-4 py-2.5 rounded-xl border border-zinc-800 bg-zinc-950 text-white placeholder-zinc-600 focus:ring-2 focus:ring-orange-500 outline-none transition text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase text-zinc-400 mb-1">Materiales Necesarios</label>
                <textarea
                  name="materials"
                  required
                  rows={3}
                  placeholder="Ej. 3 zanahorias, licuadora, aro de luz, guantes verdes"
                  className="w-full px-4 py-2.5 rounded-xl border border-zinc-800 bg-zinc-950 text-white placeholder-zinc-600 focus:ring-2 focus:ring-orange-500 outline-none transition text-sm resize-none"
                />
              </div>

              {error && <p className="text-xs text-red-500 bg-red-950/20 px-3 py-2 rounded-lg text-center border border-red-950">{error}</p>}

              <button
                type="submit"
                disabled={formLoading}
                className="w-full py-3 bg-orange-600 hover:bg-orange-500 disabled:bg-orange-800 text-white font-semibold rounded-xl text-sm transition shadow-lg shadow-orange-950/20"
              >
                {formLoading ? 'Registrando...' : 'Programar Guion'}
              </button>
            </form>
          </section>
        )}

        {/* Lado Derecho: Listado de Guiones Programados */}
        <section className={`${user?.role === 'ADMIN' ? 'lg:col-span-8' : 'lg:col-span-12'} space-y-6`}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h2 className="text-lg font-bold text-white">Cronograma de Contenido</h2>
              <p className="text-xs text-zinc-500">Visualiza los guiones programados y prepara el equipo</p>
            </div>
            <span className="text-xs text-zinc-400 font-medium self-start bg-zinc-900 border border-zinc-800 px-3 py-1.5 rounded-xl">
              Total programados: {scripts.length}
            </span>
          </div>

          {scripts.length === 0 ? (
            <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-12 text-center text-zinc-500">
              No hay guiones programados en este momento.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {scripts.map((script) => (
                <article
                  key={script.id}
                  className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 flex flex-col justify-between hover:border-zinc-700 transition shadow-md"
                >
                  <div className="space-y-3">
                    {/* Fecha y Badge de Tipo */}
                    <div className="flex items-center justify-between">
                      <time className="text-xs text-orange-500 font-semibold uppercase tracking-wider">
                        {new Date(script.scheduledDate + 'T00:00:00').toLocaleDateString('es-ES', {
                          weekday: 'short',
                          day: 'numeric',
                          month: 'short',
                        })}
                      </time>
                      <span className={`text-[9px] font-bold tracking-wider px-2.5 py-1 rounded-full ${
                        script.videoType === 'SHORT'
                          ? 'bg-green-500/10 text-green-400 border border-green-500/10'
                          : 'bg-blue-500/10 text-blue-400 border border-blue-500/10'
                      }`}>
                        {script.videoType === 'SHORT' ? 'Vertical (Short)' : 'Horizontal'}
                      </span>
                    </div>

                    {/* Título y Tema */}
                    <div>
                      <h3 className="text-md font-bold text-white line-clamp-1">{script.title}</h3>
                      <p className="text-xs text-zinc-400 mt-0.5"><span className="text-zinc-600 font-semibold uppercase text-[10px]">Idea:</span> {script.theme}</p>
                    </div>

                    {/* Lista de materiales requeridos */}
                    <div className="pt-3 border-t border-zinc-800/60">
                      <h4 className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider mb-1.5">Materiales Requeridos:</h4>
                      <p className="text-xs text-zinc-300 bg-zinc-950/40 border border-zinc-800/40 p-3 rounded-xl leading-relaxed whitespace-pre-wrap">
                        {script.materials}
                      </p>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}