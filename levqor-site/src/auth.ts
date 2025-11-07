import NextAuth from 'next-auth'
import Resend from 'next-auth/providers/resend'

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Resend({
      apiKey: process.env.RESEND_API_KEY,
      from: 'no-reply@levqor.ai',
    }),
  ],
  pages: {
    signIn: '/signin',
    verifyRequest: '/signin/verify',
  },
})
