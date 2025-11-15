# ESLint Fix Plan

## Issue
100+ ESLint errors due to unescaped quotes/apostrophes in JSX

## Solutions

### Option 1: Disable the Rule (Quick Fix)
Add to .eslintrc.json:
```json
{
  "extends": "next/core-web-vitals",
  "rules": {
    "react/no-unescaped-entities": "off"
  }
}
```

### Option 2: Auto-fix with ESLint
```bash
npm run lint -- --fix
```

### Option 3: Manual fixes needed for React Hooks warning
File: src/app/developer/keys/page.tsx:44:6
Add missing dependencies to useEffect

## Recommendation
Use Option 2 (auto-fix) first, then manually fix React Hooks warning
