const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['your-image-domain.com'], // Add your image domains here
  },
  env: {
    API_URL: process.env.API_URL, // Add your API URL environment variable
  },
};

module.exports = nextConfig;