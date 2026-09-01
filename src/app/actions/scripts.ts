'use server';

import { db } from '@/prisma/db';
import { cookies } from 'next/headers';

// Recuperar los datos del usuario logueado usando la cookie de sesión
export async function getCurrentUser() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get('session_id')?.value;

  if (!sessionId) return null;

  try {
    const user = await db.orm.public.User.where({ id: sessionId }).first();
    return user;
  } catch (error) {
    console.error('Error al obtener usuario actual:', error);
    return null;
  }
}

// Obtener todos los guiones ordenados por fecha
export async function getScripts() {
  try {
    const scripts = await db.orm.public.Script.all();
    // Ordenamos cronológicamente en memoria por fecha programada
    return scripts.sort((a, b) => new Date(a.scheduledDate).getTime() - new Date(b.scheduledDate).getTime());
  } catch (error) {
    console.error('Error al obtener guiones:', error);
    return [];
  }
}

// Crear un nuevo guion (solo permitido para ADMINs)
export async function createScript(formData: FormData) {
  const user = await getCurrentUser();

  // Protección por código: aunque el formulario esté oculto en la UI para USER,
  // esta verificación en el servidor es la que realmente impide la escritura.
  if (!user || user.role !== 'ADMIN') {
    return { success: false, error: 'No tienes privilegios de Administrador para añadir guiones.' };
  }

  const title = formData.get('title') as string;
  const scheduledDate = formData.get('scheduledDate') as string;
  const videoType = formData.get('videoType') as string;
  const theme = formData.get('theme') as string;
  const materials = formData.get('materials') as string;

  if (!title || !scheduledDate || !videoType || !theme || !materials) {
    return { success: false, error: 'Todos los campos son obligatorios.' };
  }

  try {
    // Prisma 8: Creación directa con objeto plano
    await db.orm.public.Script.create({
      id: crypto.randomUUID(), // Generamos ID único en servidor
      title,
      scheduledDate,
      videoType,
      theme,
      materials,
      status: 'PENDIENTE', // Todo guion nuevo nace pendiente de aprobación del equipo
      createdById: user.id,
      createdAt: new Date().toISOString(),
    });

    return { success: true };
  } catch (error) {
    console.error('Error al crear guion:', error);
    return { success: false, error: 'Error al registrar el guion en el servidor.' };
  }
}

// Aprobar la fecha de grabación de un guion (flujo del equipo de producción, ej. USER)
export async function approveScript(scriptId: string) {
  const user = await getCurrentUser();

  // Solo un usuario autenticado puede confirmar que puede grabar ese día.
  // Si más adelante quieres restringirlo únicamente a role === 'USER'
  // (dejando fuera incluso al ADMIN), agrega esa condición aquí.
  if (!user) {
    return { success: false, error: 'Debes iniciar sesión para aprobar una fecha.' };
  }

  if (!scriptId) {
    return { success: false, error: 'Guion no válido.' };
  }

  try {
    await db.orm.public.Script.where({ id: scriptId }).update({ status: 'APROBADO' });
    return { success: true };
  } catch (error) {
    console.error('Error al aprobar guion:', error);
    return { success: false, error: 'Error al confirmar la fecha en el servidor.' };
  }
}

// Cerrar sesión
export async function logout() {
  const cookieStore = await cookies();
  cookieStore.delete('session_id');
}