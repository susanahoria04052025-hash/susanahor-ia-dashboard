'use server';

import { db } from '@/prisma/db';
import bcrypt from 'bcryptjs';
import { cookies } from 'next/headers';

// Acción de Registro de nuevo integrante del equipo
export async function registerUser(formData: FormData, patternSequence: string) {
  const id = formData.get('id') as string; // Cédula
  const name = formData.get('name') as string;

  if (!id || !name || !patternSequence) {
    return { success: false, error: 'Todos los campos son obligatorios.' };
  }

  try {
    // 1. En Prisma 8, buscamos usando .where().first() en el namespace public.User
    const existingUser = await db.orm.public.User.where({ id }).first();

    if (existingUser) {
      return { success: false, error: 'Esta cédula ya se encuentra registrada.' };
    }

    // 2. Encriptar la secuencia del patrón dibujado (ej. "0-1-4-7") con bcrypt
    const hashedPattern = await bcrypt.hash(patternSequence, 10);

    // 3. Primer usuario es ADMIN, el resto son USER
    const usersCount = await db.orm.public.User.all();
    const role = usersCount.length === 0 ? 'ADMIN' : 'USER';

    // 4. En Prisma 8 creamos pasando el objeto plano directamente (sin envoltorio "data")
    // Añadimos el createdAt en formato String ISO para evitar el conflicto de drivers
    await db.orm.public.User.create({
      id,
      name,
      pattern: hashedPattern,
      role,
      createdAt: new Date().toISOString(),
    });

    return { success: true };
  } catch (error) {
    console.error('Error en el registro:', error);
    return { success: false, error: 'Ocurrió un error en el servidor.' };
  }
}

// Acción de Login táctil
export async function loginUser(id: string, patternSequence: string) {
  if (!id || !patternSequence) {
    return { success: false, error: 'Por favor, ingresa tu cédula y patrón.' };
  }

  try {
    // 1. Buscar usuario en Neon usando la sintaxis de Prisma 8
    const user = await db.orm.public.User.where({ id }).first();

    if (!user) {
      return { success: false, error: 'La cédula no coincide con ningún miembro.' };
    }

    // 2. Validar que el patrón coincida con el hash
    const isValid = await bcrypt.compare(patternSequence, user.pattern);
    if (!isValid) {
      return { success: false, error: 'Patrón de desbloqueo incorrecto.' };
    }

    // 3. Crear una sesión básica en cookies
    (await cookies()).set('session_id', user.id, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      maxAge: 60 * 60 * 24 * 7, // 1 semana
      path: '/',
    });

    return { success: true, role: user.role, name: user.name };
  } catch (error) {
    console.error('Error en el login:', error);
    return { success: false, error: 'Ocurrió un error de inicio de sesión.' };
  }
}