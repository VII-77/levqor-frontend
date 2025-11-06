/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    domains: ['api.levqor.ai'],
  },
}

module.exports = nextConfig
