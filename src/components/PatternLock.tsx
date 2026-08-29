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

  const pathRef = useRef<number[]>([]);

  useEffect(() => {
    pathRef.current = path;
  }, [path]);

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
      
      if (pathRef.current.length >= 3) {
        onComplete(pathRef.current.join('-'));
      } else {
        setPath([]);
      }
    };

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
  }, [isDrawing, onComplete]);

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <svg
        ref={svgRef}
        viewBox="0 0 300 300"
        className="touch-none select-none border-2 border-orange-100 rounded-3xl bg-[#FFFBF5] shadow-inner cursor-pointer"
        style={{ width, height }}
      >
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
              className="stroke-[#FF5A1F] stroke-[6]"
              strokeLinecap="round"
            />
          );
        })}

        {isDrawing && currPos && path.length > 0 && (
          <line
            x1={POINTS.find((p) => p.id === path[path.length - 1])!.x}
            y1={POINTS.find((p) => p.id === path[path.length - 1])!.y}
            x2={currPos.x}
            y2={currPos.y}
            className="stroke-[#FF5A1F]/70 stroke-[4]"
            strokeDasharray="4 4"
            strokeLinecap="round"
          />
        )}

        {POINTS.map((pt) => {
          const isSelected = path.includes(pt.id);
          const isLast = path[path.length - 1] === pt.id;

          return (
            <g key={pt.id}>
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
              
              <circle
                cx={pt.x}
                cy={pt.y}
                r={isSelected ? 16 : 8}
                pointerEvents="none"
                className={`transition-all duration-150 ${
                  isSelected
                    ? isLast
                      ? 'fill-orange-100 stroke-[#FF5A1F] stroke-[3]'
                      : 'fill-orange-50 stroke-[#FF5A1F] stroke-[2]'
                    : 'fill-[#EADBC8] hover:fill-[#D8C4B6]'
                }`}
              />

              <circle
                cx={pt.x}
                cy={pt.y}
                r={isSelected ? 6 : 0}
                pointerEvents="none"
                className="fill-[#FF5A1F] transition-all duration-150"
              />
            </g>
          );
        })}
      </svg>
      <div className="mt-4 text-[10px] text-zinc-400 font-bold uppercase tracking-wider">
        Secuencia: {path.length > 0 ? path.join(' ➔ ') : 'Ninguna'}
      </div>
    </div>
  );
}