'use client';

import React from 'react';
import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#FFFDF9] text-[#2F1F1F] selection:bg-orange-200 selection:text-orange-900 font-sans">
      
      {/* HEADER / NAVBAR */}
      <header className="sticky top-0 z-50 backdrop-blur-md bg-[#FFFDF9]/85 border-b border-orange-100/60 px-6 py-4 max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <img src="/assets/icon.jpg" alt="Susanahoria" className="w-10 h-10 rounded-2xl shadow-md border-2 border-orange-200" />
          <div>
            <span className="text-lg font-black tracking-tight text-[#FF5A1F] font-mono">SUSANAHORIA</span>
            <span className="text-xs block text-pink-500 font-bold -mt-1">Creadora Digital</span>
          </div>
        </div>

        {/* Navegación del Portafolio */}
        <nav className="hidden md:flex items-center gap-8 font-bold text-sm text-[#5E4F4F]">
          <a href="#about" className="hover:text-[#FF5A1F] transition">Sobre Mí</a>
          <a href="#works" className="hover:text-[#FF5A1F] transition">Mi Contenido</a>
          <a href="#philosophy" className="hover:text-[#FF5A1F] transition">Filosofía</a>
        </nav>

        {/* Botón de Acceso Privado */}
        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="text-xs md:text-sm font-bold bg-[#FF5A1F] hover:bg-[#E04810] text-white px-5 py-2.5 rounded-2xl transition shadow-md shadow-orange-500/15 hover:scale-[1.02]"
          >
            Acceso Equipo 🥕
          </Link>
        </div>
      </header>

      {/* HERO SECTION - Presentación Alegre */}
      <section id="about" className="max-w-7xl mx-auto px-6 py-12 md:py-20 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
          <div className="inline-block bg-pink-100 text-pink-600 text-xs font-black px-4 py-1.5 rounded-full uppercase tracking-wider">
            ✨ Diseñadora & Creadora de 12 Años
          </div>
          <h1 className="text-4xl md:text-6xl font-black text-[#2F1F1F] leading-tight">
            Diseño de Marca que <span className="text-[#FF5A1F] italic underline decoration-wavy decoration-pink-300">Brilla</span> y Divierte
          </h1>
          <p className="text-lg text-[#5E4F4F] max-w-xl mx-auto lg:mx-0 leading-relaxed">
            ¡Hola! Soy Susana. Me encanta crear contenido alegre, divertido y saludable para niños y familias. Diseño experiencias visuales llenas de color, chispa y, por supuesto, ¡muchas zanahorias!
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-4">
            <a
              href="#works"
              className="w-full sm:w-auto text-center font-bold bg-[#FF5A1F] text-white px-8 py-4 rounded-2xl shadow-lg shadow-orange-500/20 hover:bg-[#E04810] transition hover:scale-[1.01]"
            >
              Ver Mi Portafolio
            </a>
            <a
              href="https://www.youtube.com/@SUSANAAHORIA"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto text-center font-bold bg-white text-[#2F1F1F] border-2 border-orange-100 px-8 py-4 rounded-2xl hover:bg-orange-50/50 transition"
            >
              Ir a Mi Canal 🎥
            </a>
          </div>
        </div>

        {/* Tarjeta del Perfil de Susanahoria (Estilo Maquetado Solar Pop) */}
        <div className="lg:col-span-5 relative flex justify-center">
          <div className="relative w-full max-w-sm aspect-square bg-gradient-to-tr from-pink-400 to-orange-400 rounded-[3rem] p-4 shadow-2xl rotate-2 hover:rotate-0 transition duration-300">
            <div className="w-full h-full bg-white rounded-[2.5rem] overflow-hidden flex flex-col items-center justify-center p-6 border-4 border-orange-100">
              <img src="/assets/icon.jpg" alt="Susanahoria" className="w-32 h-32 rounded-[2rem] shadow-md border-4 border-orange-200 mb-4" />
              <h2 className="text-2xl font-black text-[#FF5A1F]">SUSANAHORIA</h2>
              <p className="text-xs text-[#5E4F4F] text-center font-semibold mt-1">
                "¡Comida sana, videos felices y mucha diversión digital!"
              </p>
              <div className="flex gap-2 mt-4">
                <span className="bg-orange-100 text-[#FF5A1F] font-bold text-[10px] px-3 py-1 rounded-full uppercase">Saludable</span>
                <span className="bg-pink-100 text-pink-600 font-bold text-[10px] px-3 py-1 rounded-full uppercase">Creativo</span>
                <span className="bg-yellow-100 text-yellow-700 font-bold text-[10px] px-3 py-1 rounded-full uppercase">Kids</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECCIÓN DE CONTENIDO SELECCIONADO */}
      <section id="works" className="bg-[#FFFDF9] py-16 border-t border-orange-100/40">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-xl mx-auto space-y-3 mb-12">
            <h2 className="text-3xl font-black text-[#2F1F1F]">Mi Contenido Seleccionado</h2>
            <p className="text-sm text-[#5E4F4F]">
              Un vistazo rápido a las ideas que cocinamos, grabamos y compartimos con el mundo entero en YouTube.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            {/* Card 1 */}
            <div className="bg-[#FFFDF9] border border-orange-100 rounded-3xl p-6 shadow-sm hover:shadow-lg transition group">
              <div className="aspect-video w-full bg-orange-100 rounded-2xl overflow-hidden mb-4 relative">
                <div className="absolute inset-0 bg-gradient-to-t from-[#FF5A1F]/80 to-transparent flex items-end p-3">
                  <span className="text-white text-xs font-bold uppercase">Cocina Divertida</span>
                </div>
                <img src="/assets/icon.jpg" className="w-full h-full object-cover group-hover:scale-105 transition" alt="Recetas" />
              </div>
              <h3 className="font-black text-[#2F1F1F] text-md">Recetas de Zanahorias</h3>
              <p className="text-xs text-[#5E4F4F] mt-1 leading-relaxed">
                Postres, snacks crujientes y batidos llenos de vitaminas explicados de forma súper fácil para niños.
              </p>
            </div>

            {/* Card 2 */}
            <div className="bg-[#FFFDF9] border border-orange-100 rounded-3xl p-6 shadow-sm hover:shadow-lg transition group">
              <div className="aspect-video w-full bg-pink-100 rounded-2xl overflow-hidden mb-4 relative">
                <div className="absolute inset-0 bg-gradient-to-t from-pink-500/80 to-transparent flex items-end p-3">
                  <span className="text-white text-xs font-bold uppercase">Manualidades</span>
                </div>
                <img src="/assets/icon.jpg" className="w-full h-full object-cover group-hover:scale-105 transition" alt="Manualidades" />
              </div>
              <h3 className="font-black text-[#2F1F1F] text-md">Origami y Colores</h3>
              <p className="text-xs text-[#5E4F4F] mt-1 leading-relaxed">
                Tardes creativas de pintura, cortes de papel y plastilina para despertar la imaginación.
              </p>
            </div>

            {/* Card 3 */}
            <div className="bg-[#FFFDF9] border border-orange-100 rounded-3xl p-6 shadow-sm hover:shadow-lg transition group">
              <div className="aspect-video w-full bg-yellow-100 rounded-2xl overflow-hidden mb-4 relative">
                <div className="absolute inset-0 bg-gradient-to-t from-yellow-600/80 to-transparent flex items-end p-3">
                  <span className="text-white text-xs font-bold uppercase">Videos Educativos</span>
                </div>
                <img src="/assets/icon.jpg" className="w-full h-full object-cover group-hover:scale-105 transition" alt="Educativos" />
              </div>
              <h3 className="font-black text-[#2F1F1F] text-md">Aventuras y Ciencia</h3>
              <p className="text-xs text-[#5E4F4F] mt-1 leading-relaxed">
                Datos curiosos de animales, experimentos caseros seguros y retos aptos para toda la familia.
              </p>
            </div>

            {/* Card 4 */}
            <div className="bg-[#FFFDF9] border border-orange-100 rounded-3xl p-6 shadow-sm hover:shadow-lg transition group">
              <div className="aspect-video w-full bg-emerald-100 rounded-2xl overflow-hidden mb-4 relative">
                <div className="absolute inset-0 bg-gradient-to-t from-emerald-600/80 to-transparent flex items-end p-3">
                  <span className="text-white text-xs font-bold uppercase">Detrás de Cámaras</span>
                </div>
                <img src="/assets/icon.jpg" className="w-full h-full object-cover group-hover:scale-105 transition" alt="Vlogs" />
              </div>
              <h3 className="font-black text-[#2F1F1F] text-md">Detrás de Cámaras</h3>
              <p className="text-xs text-[#5E4F4F] mt-1 leading-relaxed">
                Cómo organizamos nuestro set de grabación, tomas graciosas y la preparación de cada video.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* SECCIÓN DE FILOSOFÍA Y VALORES */}
      <section id="philosophy" className="bg-[#FFFBF5] py-16 border-t border-orange-100/30">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          <div className="lg:col-span-5 space-y-4">
            <span className="text-xs font-bold text-pink-500 uppercase tracking-widest">Nuestra Filosofía</span>
            <h2 className="text-3xl font-black text-[#2F1F1F]">¿Por qué Susanahoria es Diferente?</h2>
            <p className="text-sm text-[#5E4F4F] leading-relaxed">
              Creemos que la alimentación sana y el entretenimiento pueden ir de la mano. A través de colores vibrantes y mensajes educativos de autocuidado, inspiramos a una nueva generación a divertirse comiendo sano y creando de forma positiva.
            </p>
            
            {/* Estadísticas de Impacto */}
            <div className="grid grid-cols-2 gap-4 pt-4">
              <div className="bg-white border border-orange-100 p-4 rounded-2xl text-center">
                <span className="block text-2xl font-black text-[#FF5A1F]">120K+</span>
                <span className="text-[10px] font-bold text-zinc-500 uppercase">Amigos Felices</span>
              </div>
              <div className="bg-white border border-orange-100 p-4 rounded-2xl text-center">
                <span className="block text-2xl font-black text-[#FF5A1F]">15+</span>
                <span className="text-[10px] font-bold text-zinc-500 uppercase">Temas Divertidos</span>
              </div>
            </div>
          </div>

          <div className="lg:col-span-7 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white border border-orange-50/60 p-6 rounded-3xl space-y-2">
              <span className="text-2xl">🌱</span>
              <h3 className="font-black text-[#2F1F1F] text-sm">Alimentación Colorida</h3>
              <p className="text-xs text-[#5E4F4F] leading-relaxed">
                Incentivamos el consumo de vegetales de forma amigable, lúdica y sin presiones.
              </p>
            </div>
            
            <div className="bg-white border border-orange-50/60 p-6 rounded-3xl space-y-2">
              <span className="text-2xl">🎨</span>
              <h3 className="font-black text-[#2F1F1F] text-sm">Identidad Visual</h3>
              <p className="text-xs text-[#5E4F4F] leading-relaxed">
                Paletas de colores diseñadas para conectar emocionalmente con familias y niños.
              </p>
            </div>

            <div className="bg-white border border-orange-50/60 p-6 rounded-3xl space-y-2">
              <span className="text-2xl">⚡</span>
              <h3 className="font-black text-[#2F1F1F] text-sm">Edición Dinámica</h3>
              <p className="text-xs text-[#5E4F4F] leading-relaxed">
                Estructuras de guiones dinámicas para retener la atención de la audiencia infantil de forma sana.
              </p>
            </div>

            <div className="bg-white border border-orange-50/60 p-6 rounded-3xl space-y-2">
              <span className="text-2xl">🧠</span>
              <h3 className="font-black text-[#2F1F1F] text-sm">Diseño de Impacto</h3>
              <p className="text-xs text-[#5E4F4F] leading-relaxed">
                Mensajes con propósito que promueven la empatía, el cuidado y los hábitos positivos.
              </p>
            </div>
          </div>

        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-orange-100/50 py-12 bg-white text-center text-xs text-zinc-500 space-y-4">
        <div className="flex items-center justify-center gap-3">
          <img src="/assets/icon.jpg" alt="Susanahoria" className="w-8 h-8 rounded-xl shadow-inner" />
          <span className="font-black text-[#FF5A1F] tracking-tight">SUSANAHORIA IA</span>
        </div>
        <p className="max-w-md mx-auto">
          © {new Date().getFullYear()} Susanahoria. Creado con ❤️ y mucha creatividad digital para inspirar a niños y familias.
        </p>
        <div className="flex justify-center gap-6 text-[#FF5A1F] font-bold">
          <Link href="/login" className="hover:underline">Acceso Privado para el Equipo</Link>
        </div>
      </footer>

    </div>
  );
}