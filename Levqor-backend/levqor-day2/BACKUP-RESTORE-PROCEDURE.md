# 🗄️ Backup + Restore Test Procedure

**Target:** Day 2 Burn-In  
**Frequency:** Manual (once during burn-in, then weekly)  
**Database:** PostgreSQL (Neon)  

---

## 📋 **BACKUP PROCEDURE**

### **1. Manual Database Dump**

```bash
# Set environment variables (already available in Replit)
export PGHOST="${PGHOST}"
export PGPORT="${PGPORT}"
export PGUSER="${PGUSER}"
export PGDATABASE="${PGDATABASE}"
export PGPASSWORD="${PGPASSWORD}"

# Create backup directory
mkdir -p backups/$(date +%Y-%m)

# Generate backup with timestamp
BACKUP_FILE="backups/$(date +%Y-%m)/levqor-db-$(date +%Y%m%d-%H%M%S).sql"

# Create dump (schema + data)
pg_dump \
  --host="$PGHOST" \
  --port="$PGPORT" \
  --username="$PGUSER" \
  --dbname="$PGDATABASE" \
  --no-password \
  --format=plain \
  --no-owner \
  --no-acl \
  > "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"

echo "✅ Backup created: ${BACKUP_FILE}.gz"
ls -lh "${BACKUP_FILE}.gz"
```

### **2. Verify Backup Integrity**

```bash
BACKUP_GZ="${BACKUP_FILE}.gz"

# Decompress and validate
echo "Validating backup..."
gunzip -c "$BACKUP_GZ" | head -20

# Check for key indicators
gunzip -c "$BACKUP_GZ" | grep -E "PostgreSQL database dump|CREATE TABLE|COPY" | head -5

# Calculate checksum
CHECKSUM=$(sha256sum "$BACKUP_GZ" | awk '{print $1}')
echo "Checksum (SHA256): $CHECKSUM"

# Save checksum
echo "$CHECKSUM  $(basename $BACKUP_GZ)" > "${BACKUP_GZ}.sha256"
```

### **3. Log Backup Metadata**

```bash
# Append to backup log
cat >> backups/backup-log.txt << EOF
---
Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
File: $(basename $BACKUP_GZ)
Size: $(ls -lh $BACKUP_GZ | awk '{print $5}')
Checksum: $CHECKSUM
Tables: $(gunzip -c $BACKUP_GZ | grep -c "CREATE TABLE")
Status: Success
---
EOF

echo "✅ Backup logged"
```

---

## 🔄 **RESTORE TEST PROCEDURE**

### **IMPORTANT: Use Staging/Test Database**
**Never test restore on production database!**

### **1. Create Test Database**

```bash
# Option A: Local test database (if available)
createdb levqor_restore_test

# Option B: Use Neon branch (recommended)
# In Neon dashboard: Create branch "restore-test"
# Use branch connection string for restore
```

### **2. Perform Restore**

```bash
BACKUP_GZ="backups/2025-11/levqor-db-20251111-170000.sql.gz"
TEST_DB="levqor_restore_test"

# Restore to test database
echo "Restoring to test database: $TEST_DB"

gunzip -c "$BACKUP_GZ" | psql \
  --host="$PGHOST" \
  --port="$PGPORT" \
  --username="$PGUSER" \
  --dbname="$TEST_DB" \
  --quiet

echo "✅ Restore complete"
```

### **3. Verify Restored Data**

```bash
# Connect to test database
export PGDATABASE="$TEST_DB"

# Count tables
TABLE_COUNT=$(psql -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | xargs)
echo "Tables restored: $TABLE_COUNT"

# Sample data check
echo ""
echo "Sample data verification:"
psql -c "SELECT COUNT(*) as intelligence_events FROM intelligence_events;" || echo "Table not found"
psql -c "SELECT COUNT(*) as users FROM users;" || echo "Table not found"
psql -c "SELECT COUNT(*) as jobs FROM jobs;" || echo "Table not found"

# Check for data integrity
echo ""
echo "Data integrity check:"
psql -c "SELECT table_name, 
                (SELECT COUNT(*) FROM information_schema.columns 
                 WHERE table_name = t.table_name) as column_count
         FROM information_schema.tables t 
         WHERE table_schema = 'public'
         ORDER BY table_name;"
```

### **4. Compare with Production**

```bash
# Switch back to production database
export PGDATABASE="${PGDATABASE}"

# Get production counts
echo "Production table counts:"
psql -c "SELECT 
          (SELECT COUNT(*) FROM intelligence_events) as events,
          (SELECT COUNT(*) FROM users) as users,
          (SELECT COUNT(*) FROM jobs) as jobs;"

echo ""
echo "Test database counts:"
export PGDATABASE="$TEST_DB"
psql -c "SELECT 
          (SELECT COUNT(*) FROM intelligence_events) as events,
          (SELECT COUNT(*) FROM users) as users,
          (SELECT COUNT(*) FROM jobs) as jobs;"

# Counts should match (or test DB slightly behind if production active)
```

### **5. Cleanup**

```bash
# Drop test database
dropdb levqor_restore_test

# Or delete Neon branch via dashboard

echo "✅ Restore test cleanup complete"
```

---

## 📝 **RESTORE TEST LOG**

**Template for SECURITY-HARDENING-REPORT.md:**

```markdown
### Backup + Restore Test Results

**Test Date:** 2025-11-12 09:00 UTC  
**Backup File:** levqor-db-20251111-170000.sql.gz  
**Backup Size:** 2.4 MB  
**Checksum (SHA256):** a1b2c3d4e5f6...  

**Backup Contents:**
- Tables: 12
- Intelligence Events: 0
- Users: 3
- Jobs: 0

**Restore Test:**
- Target: Neon branch "restore-test"
- Duration: 8 seconds
- Tables Restored: 12/12 ✅
- Data Integrity: PASS ✅
- Schema Match: PASS ✅

**Verification:**
- All tables present: ✅
- Indexes intact: ✅
- Foreign keys valid: ✅
- Data counts match: ✅

**Status:** PASS ✅  
**Next Test:** 2025-11-18 (weekly)
```

---

## 🔐 **BACKUP SECURITY**

### **Encryption (Optional but Recommended)**

```bash
# Encrypt backup with GPG
gpg --symmetric --cipher-algo AES256 "${BACKUP_FILE}.gz"

# Result: ${BACKUP_FILE}.gz.gpg

# Decrypt when needed
gpg --decrypt "${BACKUP_FILE}.gz.gpg" > "${BACKUP_FILE}.gz"
```

### **Storage Locations**

**Primary:** Replit storage (local backups directory)  
**Secondary (Recommended):**
- Upload to S3/R2/B2 with encryption
- Store in private Git LFS repository
- Sync to encrypted external drive

### **Retention Policy**

```
Daily backups:  Keep 7 days
Weekly backups: Keep 4 weeks
Monthly backups: Keep 12 months
```

---

## ⚠️ **IMPORTANT NOTES**

1. **Never test restore on production database**
2. **Always verify backup integrity before deletion**
3. **Test restore at least once per week**
4. **Keep backups encrypted if containing sensitive data**
5. **Document all backup/restore operations**
6. **Store backups in multiple locations**

---

## 🚀 **AUTOMATED BACKUP SCRIPT**

```bash
#!/bin/bash
# scripts/backup_database.sh
# Run via cron: 0 2 * * * /path/to/backup_database.sh

set -euo pipefail

BACKUP_DIR="backups/$(date +%Y-%m)"
mkdir -p "$BACKUP_DIR"

BACKUP_FILE="$BACKUP_DIR/levqor-db-$(date +%Y%m%d-%H%M%S).sql"

# Create backup
pg_dump \
  --host="$PGHOST" \
  --port="$PGPORT" \
  --username="$PGUSER" \
  --dbname="$PGDATABASE" \
  --no-password \
  --format=plain \
  --no-owner \
  --no-acl \
  > "$BACKUP_FILE"

# Compress
gzip "$BACKUP_FILE"

# Calculate checksum
sha256sum "${BACKUP_FILE}.gz" > "${BACKUP_FILE}.gz.sha256"

# Log
echo "$(date -u): Backup created: $(basename ${BACKUP_FILE}.gz)" >> backups/backup-log.txt

# Cleanup old backups (keep 7 days)
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete

echo "✅ Backup complete: ${BACKUP_FILE}.gz"
```

---

**Complete backup + restore test during Day 2 burn-in and document results in SECURITY-HARDENING-REPORT.md** 📦
