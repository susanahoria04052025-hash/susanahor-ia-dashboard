'use client';

import React, { useState, useEffect } from 'react';

export default function SplashScreen() {
  const [show, setShow] = useState(true);

  useEffect(() => {
    // Mantenemos el splash activo por 2.4 segundos y luego lo desmontamos del DOM
    const timer = setTimeout(() => {
      setShow(false);
    }, 2400);
    return () => clearTimeout(timer);
  }, []);

  if (!show) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-white pointer-events-none">
      <style>{`
        @keyframes squishAndFade {
          0% {
            transform: scale(0.2);
            opacity: 0;
          }
          15% {
            transform: scale(1.15, 0.85); /* Achatar puntas */
            opacity: 1;
          }
          30% {
            transform: scale(0.85, 1.15); /* Estirar hacia arriba */
          }
          45% {
            transform: scale(1.05, 0.95); /* Rebote pequeño */
          }
          60% {
            transform: scale(1);
            opacity: 1;
          }
          80% {
            transform: scale(1);
            opacity: 1;
          }
          100% {
            transform: scale(1.25); /* Escala de salida */
            opacity: 0; /* Desvanecido suave */
          }
        }
        @keyframes bgFade {
          0%, 80% { background-color: #ffffff; }
          100% { background-color: rgba(255, 255, 255, 0); }
        }
        .animate-squish {
          animation: squishAndFade 2.4s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }
        .animate-bg-fade {
          animation: bgFade 2.4s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }
      `}</style>
      <div className="absolute inset-0 bg-white animate-bg-fade" />
      <div className="relative animate-squish flex flex-col items-center">
        <img
          src="/assets/icon.jpg"
          alt="Susanahoria"
          className="w-36 h-36 rounded-[2.5rem] shadow-xl border-4 border-orange-200"
        />
        <h1 className="text-3xl font-black text-[#FF5A1F] mt-5 tracking-wider font-mono">
          SUSANAHORIA
        </h1>
        <span className="text-xs font-black text-pink-500 uppercase tracking-widest mt-1">
          Cargando creatividad...
        </span>
      </div>
    </div>
  );
}