/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // API routes configuration
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NODE_ENV === 'production' 
          ? '/api/:path*'  // Uses Vercel serverless functions in production
          : 'http://localhost:8000/api/:path*', // Local Python backend in dev
      },
    ]
  },
  // Environment variables
  env: {
    API_URL: process.env.API_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig
