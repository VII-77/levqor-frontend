import { withAuthMiddleware } from "next-auth/middleware";

export default withAuthMiddleware({
  pages: { signIn: "/signin" },
});

export const config = {
  matcher: ["/workflow"],
};
