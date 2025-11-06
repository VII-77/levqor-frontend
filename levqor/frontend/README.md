# Levqor Frontend

Production-ready Next.js 14 frontend for the Levqor AI automation platform.

## Features

- 🚀 Next.js 14 with App Router
- 📊 Real-time system status monitoring
- 📱 Mobile-responsive design
- ⚡ TypeScript for type safety
- 🎨 Modern gradient UI
- 📄 Legal pages (Privacy, Terms)

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=https://7bcf7cfb-abac-4066-a19e-5fbe1b6c0854-00-msem1k2vhtji.kirk.replit.dev
```

## Local Development

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Deployment to Vercel

1. Push to GitHub
2. Import repository at https://vercel.com/new
3. Add environment variable: `NEXT_PUBLIC_API_URL`
4. Deploy

## Backend CORS

After deployment, update the backend CORS settings to allow your Vercel domain.

## Structure

```
src/
├── app/
│   ├── page.tsx          # Homepage
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
└── components/
    └── StatusCard.tsx    # Status display component
```

## License

Proprietary - All rights reserved
