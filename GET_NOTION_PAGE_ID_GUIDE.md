# 📋 How to Get Your Notion Parent Page ID

## Step-by-Step Instructions

### 1️⃣ Open Notion in Your Browser
- Go to your Notion workspace
- Navigate to any page where you want the databases created
- OR create a new empty page called "EchoPilot Databases"

### 2️⃣ Get the Page ID from the URL

The URL looks like this:
```
https://www.notion.so/workspace/Page-Name-abc123def456?v=...
                                        ↑
                                    This is your Page ID!
```

**Example:**
```
URL: https://www.notion.so/myworkspace/EchoPilot-Databases-1234567890abcdef1234567890abcdef

Page ID: 1234567890abcdef1234567890abcdef
```

**The Page ID is the 32-character string after your page name**

### 3️⃣ Format It Correctly

Notion page IDs can have hyphens or not. Both work:

✅ **With hyphens:**
```
12345678-90ab-cdef-1234-567890abcdef
```

✅ **Without hyphens:**
```
1234567890abcdef1234567890abcdef
```

### 4️⃣ Share It With Me

Just reply with:
```
NOTION_PARENT_PAGE_ID=<your_page_id_here>
```

**Or simply paste the page ID directly!**

---

## 🔍 Troubleshooting

### "I don't see a 32-character string"
- Make sure you're viewing the page in a **web browser**, not the app
- Click on the page name at the top to see the full URL
- Copy everything after the last `/` and before any `?` character

### "My URL looks different"
Common formats:
```
https://notion.so/workspace/<PAGE_ID>
https://www.notion.so/<PAGE_ID>
notion.so/<PAGE_ID>?v=...
```
The Page ID is always the 32-character hex string (0-9, a-f)

### "Can I use any page?"
Yes! It can be:
- ✅ An empty page you just created
- ✅ Your main workspace page
- ✅ A dedicated "Databases" page
- ✅ Any page where your Notion integration has access

### "Do I need special permissions?"
- ✅ The page must be shared with your Notion integration
- ✅ Your integration needs "Create database" permission
- ✅ Check in Notion Settings → Integrations

---

## ⚡ Quick Copy-Paste Template

Just fill in and send back:

```
NOTION_PARENT_PAGE_ID=YOUR_32_CHARACTER_PAGE_ID_HERE
```

Example:
```
NOTION_PARENT_PAGE_ID=1234567890abcdef1234567890abcdef
```

---

## 🎯 What Happens Next?

Once you provide the Page ID:

1. ✅ I'll add it to your environment
2. ✅ I'll run `python bot/database_setup.py`
3. ✅ 8 databases will be auto-created in ~10 seconds
4. ✅ I'll add all 8 database IDs to your environment
5. ✅ Readiness jumps from 38% → 63%! 🚀

**Total time:** 1 minute after you provide the ID

---

## 📸 Visual Guide

```
┌─────────────────────────────────────────┐
│ Notion Page URL                         │
├─────────────────────────────────────────┤
│ https://notion.so/workspace/            │
│ My-Database-Page-                       │
│ abc123def456789012345678abc123def       │
│                   └──────────┬──────────┘
│                        Copy this!        │
└─────────────────────────────────────────┘
```

---

Ready? Just paste your Page ID below! 👇
