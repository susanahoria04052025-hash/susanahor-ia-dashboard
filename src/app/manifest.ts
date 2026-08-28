import { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Susanahoria CMS',
    short_name: 'Susanahoria',
    description: 'Sistema de gestión de guiones y organización de contenido para Susanahoria',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#ff7a00', // El naranja característico de la zanahoria
    icons: [
      {
        src: '/assets/icon.jpg',
        sizes: '512x512',
        type: 'image/jpeg',
      },
    ],
  }
}