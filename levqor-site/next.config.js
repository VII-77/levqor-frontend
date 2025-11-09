/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  experimental: { scrollRestoration: true },
  images: { formats: ['image/avif','image/webp'] },
  headers: async () => ([
    {
      source: '/:all*(svg|jpg|jpeg|png|gif|webp|avif|ico|css|js|woff|woff2)',
      headers: [
        { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }
      ],
    },
    {
      source: '/(pricing|docs|privacy|terms|contact)',
      headers: [
        { key: 'Cache-Control', value: 'public, s-maxage=86400, stale-while-revalidate=604800' }
      ],
    }
  ]),
};
module.exports = nextConfig;
