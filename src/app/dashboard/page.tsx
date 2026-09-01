'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Fredoka, Inter } from 'next/font/google';
import { getCurrentUser, getScripts, createScript, approveScript, updateScriptContent, toggleMaterialStatus, logout } from '@/app/actions/scripts';

// Tipografía: Fredoka para titulares (redonda, juguetona — encaja con un canal de una
// creadora de 12 años) + Inter para texto de cuerpo, legible en paneles densos.
const fredoka = Fredoka({ subsets: ['latin'], weight: ['500', '600', '700'], variable: '--font-display' });
const inter = Inter({ subsets: ['latin'], weight: ['400', '500', '600', '700'], variable: '--font-body' });

interface User {
  id: string;
  name: string;
  role: string;
}

interface Script {
  id: string;
  title: string;
  scheduledDate: string; // 'YYYY-MM-DD'
  videoType: string;
  theme: string;
  materials: string;
  status: string; // 'PENDIENTE' | 'APROBADO'
  content?: string | null; // Texto completo del guion, redactado desde la Card de Guiones
  checkedMaterials?: string | null; // Materiales marcados como listos, separados por comas
}

const SEPT_YEAR = 2026;
const SEPT_MONTH = 8; // Septiembre (0-indexado)
const DAYS_IN_SEPT = new Date(SEPT_YEAR, SEPT_MONTH + 1, 0).getDate();
const WEEKDAY_LABELS = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];

function dateKey(day: number) {
  return `${SEPT_YEAR}-${String(SEPT_MONTH + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
}

// Offset (0 = Lunes) del primer día del mes, para alinear la grilla del calendario
function firstDayOffset() {
  const jsDay = new Date(SEPT_YEAR, SEPT_MONTH, 1).getDay(); // 0=Dom ... 6=Sáb
  return (jsDay + 6) % 7;
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [scripts, setScripts] = useState<Script[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formLoading, setFormLoading] = useState(false);
  const [formDate, setFormDate] = useState('');
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [approvingId, setApprovingId] = useState<string | null>(null);
  const [savingMaterial, setSavingMaterial] = useState<string | null>(null);
  const [draftContent, setDraftContent] = useState('');
  const [savingContent, setSavingContent] = useState(false);
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

  // Mapa rápido fecha -> guion, para pintar el calendario y resolver el día seleccionado
  const scriptsByDate = useMemo(() => {
    const map: Record<string, Script> = {};
    scripts.forEach((s) => {
      map[s.scheduledDate] = s;
    });
    return map;
  }, [scripts]);

  const selectedScript = selectedDate ? scriptsByDate[selectedDate] ?? null : null;

  // Si un ADMIN selecciona un día libre, precargamos la fecha en el formulario de Logística
  useEffect(() => {
    if (user?.role === 'ADMIN' && selectedDate && !scriptsByDate[selectedDate]) {
      setFormDate(selectedDate);
    }
  }, [selectedDate, scriptsByDate, user]);

  // Al cambiar de guion seleccionado, cargamos su contenido guardado en el borrador.
  // Dependemos solo del id: así no pisamos lo que el ADMIN está escribiendo si
  // `scripts` se refresca por otro motivo (ej. otro usuario aprobando otra fecha).
  useEffect(() => {
    setDraftContent(selectedScript?.content ?? '');
  }, [selectedScript?.id]);

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (user?.role !== 'ADMIN') return; // Protección por código, además de la visual
    setError('');
    setFormLoading(true);

    const form = e.currentTarget;
    const formData = new FormData(form);

    const res = await createScript(formData);

    if (res.success) {
      form.reset();
      setFormDate('');
      const updatedScripts = await getScripts();
      setScripts(updatedScripts as Script[]);
    } else {
      setError(res.error || 'Error al añadir guion.');
    }
    setFormLoading(false);
  };

  // Aprobación reactiva: actualizamos el estado local al instante (optimista) y
  // revertimos si el servidor responde con error. Como selectedScript se deriva de
  // `scripts`, el calendario y la tarjeta de detalle se sincronizan solos.
  const handleApprove = async (scriptId: string) => {
    setApprovingId(scriptId);
    setError('');
    setScripts((prev) => prev.map((s) => (s.id === scriptId ? { ...s, status: 'APROBADO' } : s)));

    const res = await approveScript(scriptId);

    if (!res.success) {
      setScripts((prev) => prev.map((s) => (s.id === scriptId ? { ...s, status: 'PENDIENTE' } : s)));
      setError(res.error || 'Error al aprobar la fecha.');
    }
    setApprovingId(null);
  };

  // Guardado reactivo del texto del guion: igual patrón optimista que la aprobación.
  const handleSaveContent = async () => {
    if (!selectedScript) return;
    const scriptId = selectedScript.id;
    const prevContent = selectedScript.content ?? '';

    setSavingContent(true);
    setError('');
    setScripts((prev) => prev.map((s) => (s.id === scriptId ? { ...s, content: draftContent } : s)));

    const res = await updateScriptContent(scriptId, draftContent);

    if (!res.success) {
      setScripts((prev) => prev.map((s) => (s.id === scriptId ? { ...s, content: prevContent } : s)));
      setError(res.error || 'Error al guardar el guion.');
    }
    setSavingContent(false);
  };

  // Checklist colaborativo: el estado "marcado" vive en `checkedMaterials` del guion en
  // Neon, no en el cliente — así ADMIN y USER ven exactamente lo mismo. Actualización
  // optimista igual que approve/save, revertida si el servidor falla.
  const handleToggleMaterial = async (scriptId: string, materialName: string) => {
    const script = scripts.find((s) => s.id === scriptId);
    if (!script) return;

    const currentChecked = script.checkedMaterials
      ? script.checkedMaterials.split(',').map((m) => m.trim()).filter(Boolean)
      : [];
    const isChecked = currentChecked.includes(materialName);
    const nextChecked = isChecked
      ? currentChecked.filter((m) => m !== materialName)
      : [...currentChecked, materialName];
    const nextString = nextChecked.join(', ');

    setSavingMaterial(materialName);
    setError('');
    setScripts((prev) => prev.map((s) => (s.id === scriptId ? { ...s, checkedMaterials: nextString } : s)));

    const res = await toggleMaterialStatus(scriptId, materialName);

    if (!res.success) {
      setScripts((prev) => prev.map((s) => (s.id === scriptId ? { ...s, checkedMaterials: script.checkedMaterials } : s)));
      setError(res.error || 'Error al actualizar el checklist.');
    }
    setSavingMaterial(null);
  };

  if (loading) {
    return (
      <div
        className={`${fredoka.variable} ${inter.variable} min-h-screen flex items-center justify-center`}
        style={{ background: '#FBF3E7', fontFamily: 'var(--font-body)' }}
      >
        <div className="text-center font-semibold" style={{ color: '#E2600B' }}>
          Cargando panel de Susanahoria...
        </div>
      </div>
    );
  }

  const isAdmin = user?.role === 'ADMIN';
  const materialsList = selectedScript ? selectedScript.materials.split(',').map((m) => m.trim()).filter(Boolean) : [];
  const checkedMaterialsList = selectedScript?.checkedMaterials
    ? selectedScript.checkedMaterials.split(',').map((m) => m.trim()).filter(Boolean)
    : [];

  // Un ADMIN puede crear guion cuando eligió un día y ese día todavía está libre.
  // (No existe hoy un estado de "día de descanso" en el modelo — todos los días de
  // Septiembre son laborables salvo que ya tengan guion programado.)
  const canAdminCreate = isAdmin && !!selectedDate && !selectedScript;
  const shouldShowDetails = !!selectedScript || canAdminCreate;

  // Card del calendario, reutilizada tanto en la vista detallada (dentro de la rejilla)
  // como en la vista centrada (cuando no hay nada que mostrar aún).
  const calendarCard = (
    <section
      className="rounded-3xl p-5 sm:p-6"
      style={{ background: '#FFFDF8', border: '1px solid #F0E2C7', boxShadow: '0 10px 30px -18px rgba(178,101,20,0.35)' }}
    >
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 600 }} className="text-xl">
            Agenda
          </h2>
          <p className="text-xs mt-0.5" style={{ color: '#A0865F' }}>
            Naranja: día libre · Verde: guion programado
          </p>
        </div>
        <div className="flex gap-2 text-[10px] font-semibold">
          <span className="flex items-center gap-1"><i className="w-2.5 h-2.5 rounded-full inline-block" style={{ background: '#F6A24A' }} />Libre</span>
          <span className="flex items-center gap-1"><i className="w-2.5 h-2.5 rounded-full inline-block" style={{ background: '#7FB876' }} />Programado</span>
        </div>
      </div>

      <div className="grid grid-cols-7 gap-1.5 sm:gap-2 mb-1.5 text-center">
        {WEEKDAY_LABELS.map((w) => (
          <span key={w} className="text-[10px] font-bold" style={{ color: '#BDA987' }}>
            {w}
          </span>
        ))}
      </div>

      <div className="grid grid-cols-7 gap-1.5 sm:gap-2">
        {Array.from({ length: firstDayOffset() }).map((_, i) => (
          <div key={`empty-${i}`} />
        ))}
        {Array.from({ length: DAYS_IN_SEPT }).map((_, i) => {
          const day = i + 1;
          const key = dateKey(day);
          const script = scriptsByDate[key];
          const isSelected = selectedDate === key;
          const isApproved = script?.status === 'APROBADO';

          return (
            <button
              key={key}
              onClick={() => setSelectedDate(key)}
              className="aspect-square rounded-xl flex flex-col items-center justify-center text-sm font-semibold transition"
              style={
                isSelected
                  ? { background: '#2B2118', color: '#FBF3E7' }
                  : script
                  ? { background: isApproved ? '#DCEEDB' : '#E9F3E4', color: '#3E7A34', border: '1px solid #BCDDB0' }
                  : { background: '#FCEBD3', color: '#B5540A', border: '1px solid #F6D9AD' }
              }
            >
              <span>{day}</span>
              {script && <span className="text-[9px] mt-0.5">{isApproved ? '✔' : '●'}</span>}
            </button>
          );
        })}
      </div>
    </section>
  );

  return (
    <div
      className={`${fredoka.variable} ${inter.variable} min-h-screen`}
      style={{ background: '#FBF3E7', fontFamily: 'var(--font-body)', color: '#2B2118' }}
    >
      {/* ===== Cabecera ===== */}
      <header
        className="print:hidden sticky top-0 z-40 px-5 sm:px-8 py-4 flex items-center justify-between border-b"
        style={{ background: 'rgba(251,243,231,0.9)', backdropFilter: 'blur(8px)', borderColor: '#EFE1CB' }}
      >
        <div className="flex items-center gap-3">
          <img src="/assets/icon.jpg" alt="Susanahoria" className="w-11 h-11 rounded-2xl shadow-sm" style={{ border: '2px solid #F6A24A' }} />
          <div>
            <h1 style={{ fontFamily: 'var(--font-display)', fontWeight: 600 }} className="text-lg leading-tight" >
              Susanahoria
            </h1>
            <p className="text-xs" style={{ color: '#A0865F' }}>
              Agenda de grabación · Septiembre 2026
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 sm:gap-4">
          <div className="hidden sm:flex flex-col items-end">
            <span className="text-sm font-semibold">{user?.name}</span>
            <span
              className="text-[10px] font-bold px-2 py-0.5 rounded-full"
              style={
                isAdmin
                  ? { background: '#FCE3C6', color: '#B5540A', border: '1px solid #F6A24A' }
                  : { background: '#F1E7D4', color: '#8A7B68', border: '1px solid #E4D5B6' }
              }
            >
              {isAdmin ? 'Manager' : 'Producción'}
            </span>
          </div>
          <button
            onClick={handleLogout}
            className="text-xs font-semibold px-4 py-2 rounded-xl transition"
            style={{ background: '#F1E7D4', color: '#6B5A3E' }}
          >
            Salir
          </button>
        </div>
      </header>

      {error && (
        <div className="print:hidden max-w-7xl mx-auto px-5 sm:px-8 pt-4">
          <p className="text-xs px-4 py-2.5 rounded-xl" style={{ background: '#FBE4DC', color: '#B0431F', border: '1px solid #F3B9A4' }}>
            {error}
          </p>
        </div>
      )}

      {/* ===== Contenedor principal ===== */}
      <main className="print:hidden px-5 sm:px-8 py-6 max-w-7xl mx-auto">
        {shouldShowDetails ? (
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        {/* ---------- Card 1: Agenda (calendario interactivo) ---------- */}
        <div className="xl:col-span-7">{calendarCard}</div>


        {/* ---------- Card 2: Guiones (detalle del día + próximos) ---------- */}
        <section
          className="xl:col-span-5 rounded-3xl p-5 sm:p-6 flex flex-col"
          style={{ background: '#FFFDF8', border: '1px solid #F0E2C7', boxShadow: '0 10px 30px -18px rgba(178,101,20,0.35)' }}
        >
          <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 600 }} className="text-xl mb-4">
            Guiones
          </h2>

          {!selectedDate && (
            <p className="text-sm" style={{ color: '#A0865F' }}>
              Selecciona un día en el calendario para ver los detalles.
            </p>
          )}

          {selectedDate && !selectedScript && (
            <div className="rounded-2xl p-4 text-sm" style={{ background: '#FCEBD3', color: '#8A5A1E' }}>
              {isAdmin
                ? 'Día libre. Usa la tarjeta de Logística para programar un guion aquí.'
                : 'No hay guion programado para este día todavía.'}
            </div>
          )}

          {selectedScript && (
            <div className="rounded-2xl p-4 space-y-3" style={{ background: '#F5F0E1' }}>
              <div className="flex items-center justify-between">
                <span
                  className="text-[9px] font-bold px-2.5 py-1 rounded-full"
                  style={
                    selectedScript.videoType === 'SHORT'
                      ? { background: '#DCEEDB', color: '#3E7A34' }
                      : { background: '#DCE7F3', color: '#2E5E8C' }
                  }
                >
                  {selectedScript.videoType === 'SHORT' ? 'Vertical (Short)' : 'Horizontal'}
                </span>
                <span
                  className="text-[9px] font-bold px-2.5 py-1 rounded-full"
                  style={
                    selectedScript.status === 'APROBADO'
                      ? { background: '#DCEEDB', color: '#3E7A34' }
                      : { background: '#FCE3C6', color: '#B5540A' }
                  }
                >
                  {selectedScript.status === 'APROBADO' ? 'Aprobado' : 'Pendiente'}
                </span>
              </div>
              <h3 className="text-md font-bold">{selectedScript.title}</h3>
              <p className="text-xs" style={{ color: '#6B5A3E' }}>
                <span className="font-semibold">Enfoque:</span> {selectedScript.theme}
              </p>

              {/* ---- Redacción del guion + impresión ---- */}
              <div className="pt-3 border-t" style={{ borderColor: '#E4D5B6' }}>
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <h4 className="text-[10px] font-bold uppercase tracking-wide" style={{ color: '#8A7B68' }}>
                    Redactar Guion del Video
                  </h4>
                  <button
                    type="button"
                    onClick={() => window.print()}
                    className="shrink-0 text-[10px] font-semibold px-3 py-1.5 rounded-lg transition"
                    style={{ background: '#2B2118', color: '#FBF3E7' }}
                  >
                    Descargar PDF / Imprimir 🖨
                  </button>
                </div>

                <textarea
                  value={isAdmin ? draftContent : selectedScript.content ?? ''}
                  onChange={isAdmin ? (e) => setDraftContent(e.target.value) : undefined}
                  readOnly={!isAdmin}
                  rows={8}
                  placeholder={isAdmin ? 'Escribe o pega aquí el guion completo...' : 'El guion aún no ha sido redactado.'}
                  className="w-full px-3 py-2.5 rounded-xl text-xs leading-relaxed outline-none resize-y"
                  style={{
                    border: '1px solid #EAD9B4',
                    background: isAdmin ? '#FFFDF8' : '#EFE6D2',
                    color: '#3A2E1E',
                  }}
                />

                {isAdmin && (
                  <button
                    type="button"
                    onClick={handleSaveContent}
                    disabled={savingContent}
                    className="mt-2 w-full py-2.5 font-semibold rounded-xl text-xs transition"
                    style={{ background: savingContent ? '#F6C08A' : '#F27B1C', color: '#FFFDF8' }}
                  >
                    {savingContent ? 'Guardando...' : 'Guardar Cambios del Guion'}
                  </button>
                )}
              </div>
            </div>
          )}

        </section>

        {/* ---------- Card 3: Logística (formulario de creación — SOLO ADMIN) ---------- */}
        {isAdmin && (
          <section
            className="xl:col-span-7 rounded-3xl p-5 sm:p-6"
            style={{ background: '#FFFDF8', border: '1px solid #F0E2C7', boxShadow: '0 10px 30px -18px rgba(178,101,20,0.35)' }}
          >
            <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 600 }} className="text-xl mb-1">
              Logística
            </h2>
            <p className="text-xs mb-5" style={{ color: '#A0865F' }}>
              Programa un guion en un día libre del calendario.
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold mb-1" style={{ color: '#8A7B68' }}>
                  Título del video
                </label>
                <input
                  type="text"
                  name="title"
                  required
                  placeholder="Ej. Receta de Zanahoria Crujiente"
                  className="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition"
                  style={{ border: '1px solid #EAD9B4', background: '#FFFDF8' }}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold mb-1" style={{ color: '#8A7B68' }}>
                    Fecha
                  </label>
                  <input
                    type="date"
                    name="scheduledDate"
                    required
                    min={`${SEPT_YEAR}-${String(SEPT_MONTH + 1).padStart(2, '0')}-01`}
                    max={dateKey(DAYS_IN_SEPT)}
                    value={formDate}
                    onChange={(e) => setFormDate(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition"
                    style={{ border: '1px solid #EAD9B4', background: '#FFFDF8' }}
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold mb-1" style={{ color: '#8A7B68' }}>
                    Tipo
                  </label>
                  <select
                    name="videoType"
                    required
                    className="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition"
                    style={{ border: '1px solid #EAD9B4', background: '#FFFDF8' }}
                  >
                    <option value="SHORT">Short (Vertical)</option>
                    <option value="HORIZONTAL">Horizontal</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold mb-1" style={{ color: '#8A7B68' }}>
                  Tema / idea central
                </label>
                <input
                  type="text"
                  name="theme"
                  required
                  placeholder="Ej. Cocina rápida saludable"
                  className="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition"
                  style={{ border: '1px solid #EAD9B4', background: '#FFFDF8' }}
                />
              </div>

              <div>
                <label className="block text-xs font-semibold mb-1" style={{ color: '#8A7B68' }}>
                  Materiales necesarios
                </label>
                <textarea
                  name="materials"
                  required
                  rows={3}
                  placeholder="Ej. 3 zanahorias, licuadora, aro de luz, guantes verdes"
                  className="w-full px-4 py-2.5 rounded-xl text-sm outline-none transition resize-none"
                  style={{ border: '1px solid #EAD9B4', background: '#FFFDF8' }}
                />
              </div>

              <button
                type="submit"
                disabled={formLoading}
                className="w-full py-3 font-semibold rounded-xl text-sm transition"
                style={{ background: formLoading ? '#F6C08A' : '#F27B1C', color: '#FFFDF8' }}
              >
                {formLoading ? 'Programando...' : 'Programar guion'}
              </button>
            </form>
          </section>
        )}

        {/* ---------- Card 4: Checklist (materiales + aprobación del equipo) ---------- */}
        <section
          className={`${isAdmin ? 'xl:col-span-5' : 'xl:col-span-12'} rounded-3xl p-5 sm:p-6`}
          style={{ background: '#FFFDF8', border: '1px solid #F0E2C7', boxShadow: '0 10px 30px -18px rgba(178,101,20,0.35)' }}
        >
          <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 600 }} className="text-xl mb-1">
            Checklist
          </h2>
          <p className="text-xs mb-5" style={{ color: '#A0865F' }}>
            Materiales para el día seleccionado
          </p>

          {!selectedScript && (
            <p className="text-sm" style={{ color: '#A0865F' }}>
              Elige un día con guion programado para ver su checklist.
            </p>
          )}

          {selectedScript && (
            <div className="space-y-4">
              <div className="space-y-2">
                {materialsList.map((item, idx) => {
                  const checked = checkedMaterialsList.includes(item);
                  const isSaving = savingMaterial === item;
                  return (
                    <label
                      key={`${selectedScript.id}-${idx}`}
                      className="flex items-center gap-3 text-sm px-3 py-2.5 rounded-xl cursor-pointer"
                      style={{ background: '#F5F0E1', opacity: isSaving ? 0.6 : 1 }}
                    >
                      <input
                        type="checkbox"
                        checked={checked}
                        disabled={isSaving}
                        onChange={() => handleToggleMaterial(selectedScript.id, item)}
                        className="w-4 h-4 rounded"
                        style={{ accentColor: '#F27B1C' }}
                      />
                      <span style={checked ? { textDecoration: 'line-through', color: '#A0865F' } : {}}>{item}</span>
                    </label>
                  );
                })}
              </div>

              {/* Estado / acción de aprobación — visible solo para el rol correspondiente */}
              <div className="pt-2">
                {!isAdmin &&
                  (selectedScript.status === 'APROBADO' ? (
                    <div
                      className="text-center text-sm font-semibold px-4 py-3 rounded-xl"
                      style={{ background: '#DCEEDB', color: '#3E7A34' }}
                    >
                      Fecha Confirmada por el Equipo 🥕✔
                    </div>
                  ) : (
                    <button
                      onClick={() => handleApprove(selectedScript.id)}
                      disabled={approvingId === selectedScript.id}
                      className="w-full py-3 font-semibold rounded-xl text-sm transition"
                      style={{
                        background: approvingId === selectedScript.id ? '#F6C08A' : '#F27B1C',
                        color: '#FFFDF8',
                      }}
                    >
                      {approvingId === selectedScript.id ? 'Confirmando...' : 'Aprobar Fecha para Grabación'}
                    </button>
                  ))}

                {isAdmin && (
                  <div
                    className="text-center text-xs font-semibold px-4 py-2.5 rounded-xl"
                    style={
                      selectedScript.status === 'APROBADO'
                        ? { background: '#DCEEDB', color: '#3E7A34' }
                        : { background: '#FCE3C6', color: '#B5540A' }
                    }
                  >
                    {selectedScript.status === 'APROBADO'
                      ? 'Equipo confirmó esta fecha ✔'
                      : 'Esperando confirmación del equipo'}
                  </div>
                )}
              </div>
            </div>
          )}
        </section>
        </div>
        ) : (
        <div className="max-w-md w-full mx-auto space-y-4">
          {calendarCard}
          <div
            className="rounded-2xl px-4 py-3.5 text-sm text-center leading-relaxed bg-white"
            style={{ border: '1px solid #F6D9AD', color: '#6B5A3E' }}
          >
            💡 Haz clic en los días de color verde en el calendario para ver el guion y los materiales
            programados por el manager 🥕.
          </div>
        </div>
        )}
      </main>

      {/* ===== Hoja de producción — visible ÚNICAMENTE al imprimir / exportar PDF ===== */}
      {selectedScript && (
        <div className="hidden print:block bg-white text-[#1A1410] px-2">
          <div className="flex items-start justify-between border-b-2 pb-4 mb-6" style={{ borderColor: '#1A1410' }}>
            <div className="flex items-center gap-3">
              <img src="/assets/icon.jpg" alt="Susanahoria" className="w-14 h-14 rounded-xl" />
              <div>
                <p className="text-[10px] font-bold tracking-widest" style={{ color: '#B5540A' }}>
                  SUSANAHORIA CMS — HOJA DE PRODUCCIÓN
                </p>
                <h1 className="text-2xl font-bold">{selectedScript.title}</h1>
              </div>
            </div>
            <div className="text-right text-xs leading-relaxed">
              <p>
                <span className="font-semibold">Fecha:</span>{' '}
                {new Date(selectedScript.scheduledDate + 'T00:00:00').toLocaleDateString('es-ES', {
                  weekday: 'long',
                  day: 'numeric',
                  month: 'long',
                  year: 'numeric',
                })}
              </p>
              <p>
                <span className="font-semibold">Formato:</span>{' '}
                {selectedScript.videoType === 'SHORT' ? 'Vertical (Short)' : 'Horizontal'}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="rounded-lg p-4" style={{ border: '1px solid #1A1410' }}>
              <h2 className="text-[10px] font-bold uppercase tracking-wide mb-1.5">Idea Central</h2>
              <p className="text-sm">{selectedScript.theme}</p>
            </div>
            <div className="rounded-lg p-4" style={{ border: '1px solid #1A1410' }}>
              <h2 className="text-[10px] font-bold uppercase tracking-wide mb-1.5">Lista de Materiales</h2>
              <ul className="text-sm list-disc list-inside space-y-0.5">
                {materialsList.map((m, idx) => (
                  <li key={idx}>{m}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="mb-10">
            <h2 className="text-[10px] font-bold uppercase tracking-wide mb-2 border-b pb-1" style={{ borderColor: '#1A1410' }}>
              Guion Completo
            </h2>
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {selectedScript.content?.trim() ? selectedScript.content : 'Este guion aún no ha sido redactado.'}
            </p>
          </div>

          <div className="text-center text-[10px] pt-4 border-t" style={{ borderColor: '#1A1410', color: '#8A7B68' }}>
            Susanahoria — Creatividad Digital
          </div>
        </div>
      )}

      {/* Ajustes de página al imprimir: márgenes y colores exactos de marca */}
      <style jsx global>{`
        @media print {
          @page {
            margin: 1.4cm;
          }
          html,
          body {
            background: #ffffff !important;
          }
          * {
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
          }
        }
      `}</style>
    </div>
  );
}