'use client';

import React, { useState, useRef, useEffect } from 'react';

interface PatternLockProps {
  onComplete: (pattern: string) => void;
  width?: number;
  height?: number;
}

const POINTS = [
  { id: 0, x: 50, y: 50 },
  { id: 1, x: 150, y: 50 },
  { id: 2, x: 250, y: 50 },
  { id: 3, x: 50, y: 150 },
  { id: 4, x: 150, y: 150 },
  { id: 5, x: 250, y: 150 },
  { id: 6, x: 50, y: 250 },
  { id: 7, x: 150, y: 250 },
  { id: 8, x: 250, y: 250 },
];

export default function PatternLock({ onComplete, width = 300, height = 300 }: PatternLockProps) {
  const [path, setPath] = useState<number[]>([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currPos, setCurrPos] = useState<{ x: number; y: number } | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);

  // Guardamos una referencia para leer la secuencia en tiempo real sin reiniciar el Effect
  const pathRef = useRef<number[]>([]);

  // Sincronizamos la referencia cada vez que el estado de 'path' cambia
  useEffect(() => {
    pathRef.current = path;
  }, [path]);

  // Iniciar el arrastre al presionar un punto
  const startDrawing = (pointId: number, e: React.MouseEvent | React.TouchEvent) => {
    e.preventDefault();
    setIsDrawing(true);
    setPath([pointId]);
    
    if (!svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    let clientX = 0;
    let clientY = 0;

    if ('touches' in e) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }

    const x = ((clientX - rect.left) / rect.width) * 300;
    const y = ((clientY - rect.top) / rect.height) * 300;
    setCurrPos({ x, y });
  };

  // Efecto global desacoplado (ya no depende de "path", evitando el bucle infinito)
  useEffect(() => {
    if (!isDrawing) return;

    const handleMove = (e: MouseEvent | TouchEvent) => {
      if (!svgRef.current) return;
      const rect = svgRef.current.getBoundingClientRect();
      
      let clientX = 0;
      let clientY = 0;

      if ('touches' in e) {
        if (e.touches.length === 0) return;
        clientX = e.touches[0].clientX;
        clientY = e.touches[0].clientY;
      } else {
        clientX = e.clientX;
        clientY = e.clientY;
      }

      const x = ((clientX - rect.left) / rect.width) * 300;
      const y = ((clientY - rect.top) / rect.height) * 300;
      setCurrPos({ x, y });

      // Verificamos proximidad con los 9 puntos usando la referencia "pathRef"
      const threshold = 25;
      for (const pt of POINTS) {
        const dist = Math.sqrt(Math.pow(x - pt.x, 2) + Math.pow(y - pt.y, 2));
        if (dist < threshold) {
          if (!pathRef.current.includes(pt.id)) {
            setPath((prev) => {
              if (prev.includes(pt.id)) return prev;
              return [...prev, pt.id];
            });
          }
        }
      }
    };

    const handleUp = () => {
      setIsDrawing(false);
      setCurrPos(null);
      
      // Verificamos la longitud utilizando la referencia actual
      if (pathRef.current.length >= 3) {
        onComplete(pathRef.current.join('-'));
      } else {
        setPath([]);
      }
    };

    // Añadimos escuchadores globales en window
    window.addEventListener('mousemove', handleMove);
    window.addEventListener('touchmove', handleMove, { passive: false });
    window.addEventListener('mouseup', handleUp);
    window.addEventListener('touchend', handleUp);

    return () => {
      window.removeEventListener('mousemove', handleMove);
      window.removeEventListener('touchmove', handleMove);
      window.removeEventListener('mouseup', handleUp);
      window.removeEventListener('touchend', handleUp);
    };
  }, [isDrawing, onComplete]); // Removido "path" de las dependencias

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <svg
        ref={svgRef}
        viewBox="0 0 300 300"
        className="touch-none select-none border border-zinc-200 dark:border-zinc-800 rounded-2xl bg-zinc-50 dark:bg-zinc-900 shadow-inner cursor-pointer"
        style={{ width, height }}
      >
        {/* Líneas estables que conectan los puntos seleccionados */}
        {path.map((pointId, idx) => {
          if (idx === 0) return null;
          const startPt = POINTS.find((p) => p.id === path[idx - 1])!;
          const endPt = POINTS.find((p) => p.id === pointId)!;
          return (
            <line
              key={`line-${idx}`}
              x1={startPt.x}
              y1={startPt.y}
              x2={endPt.x}
              y2={endPt.y}
              className="stroke-orange-500 stroke-[6]"
              strokeLinecap="round"
            />
          );
        })}

        {/* Línea flotante que sigue al cursor/dedo */}
        {isDrawing && currPos && path.length > 0 && (
          <line
            x1={POINTS.find((p) => p.id === path[path.length - 1])!.x}
            y1={POINTS.find((p) => p.id === path[path.length - 1])!.y}
            x2={currPos.x}
            y2={currPos.y}
            className="stroke-orange-400 stroke-[4]"
            strokeDasharray="4 4"
            strokeLinecap="round"
          />
        )}

        {/* Rejilla de 9 Nodos */}
        {POINTS.map((pt) => {
          const isSelected = path.includes(pt.id);
          const isLast = path[path.length - 1] === pt.id;

          return (
            <g key={pt.id}>
              {/* Círculo invisible de captura */}
              <circle
                cx={pt.x}
                cy={pt.y}
                r={25}
                fill="black"
                opacity={0}
                className="cursor-pointer"
                onMouseDown={(e) => startDrawing(pt.id, e)}
                onTouchStart={(e) => startDrawing(pt.id, e)}
              />
              
              {/* Anillo exterior visual */}
              <circle
                cx={pt.x}
                cy={pt.y}
                r={isSelected ? 16 : 8}
                pointerEvents="none"
                className={`transition-all duration-150 ${
                  isSelected
                    ? isLast
                      ? 'fill-orange-100 stroke-orange-600 stroke-[3] dark:fill-orange-950/40 dark:stroke-orange-500'
                      : 'fill-orange-50 stroke-orange-500 stroke-[2] dark:fill-orange-950/20 dark:stroke-orange-600'
                    : 'fill-zinc-300 dark:fill-zinc-700 hover:fill-zinc-400 dark:hover:fill-zinc-600'
                }`}
              />

              {/* Punto central */}
              <circle
                cx={pt.x}
                cy={pt.y}
                r={isSelected ? 6 : 0}
                pointerEvents="none"
                className="fill-orange-600 dark:fill-orange-500 transition-all duration-150"
              />
            </g>
          );
        })}
      </svg>
      <div className="mt-4 text-xs text-zinc-500 font-mono">
        Secuencia: {path.length > 0 ? path.join(' ➔ ') : 'Ninguna'}
      </div>
    </div>
  );
}