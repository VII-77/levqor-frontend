/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://7bcf7cfb-abac-4066-a19e-5fbe1b6c0854-00-msem1k2vhtji.kirk.replit.dev'
  }
}

module.exports = nextConfig
