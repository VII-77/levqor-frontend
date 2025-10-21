#!/usr/bin/env python3
"""
Data Warehouse ETL Script - Phase 106
Syncs data from 13 Notion databases to Postgres data warehouse for analytics
"""

import os
import sys
import json
import psycopg2
from datetime import datetime
from typing import Dict, List, Any, Optional
from psycopg2.extras import execute_values

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.notion_api import get_notion_client
from bot import config


class WarehouseSync:
    def __init__(self):
        self.notion = get_notion_client()
        self.conn = None
        self.start_time = datetime.utcnow()
        self.stats = {
            'tables_synced': 0,
            'rows_inserted': 0,
            'rows_updated': 0,
            'errors': 0
        }
    
    def connect_postgres(self):
        """Connect to Postgres data warehouse"""
        try:
            self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            self.conn.autocommit = False
            print(f"✅ Connected to Postgres warehouse")
        except Exception as e:
            print(f"❌ Failed to connect to Postgres: {e}")
            raise
    
    def create_schema(self):
        """Create warehouse tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Create tables for each Notion database
        tables = [
            # Automation Queue
            """
            CREATE TABLE IF NOT EXISTS wh_automation_queue (
                id VARCHAR(255) PRIMARY KEY,
                task_name TEXT,
                description TEXT,
                trigger BOOLEAN,
                status VARCHAR(50),
                task_type VARCHAR(100),
                qa_target NUMERIC,
                created_time TIMESTAMP,
                last_edited_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Automation Log
            """
            CREATE TABLE IF NOT EXISTS wh_automation_log (
                id VARCHAR(255) PRIMARY KEY,
                task TEXT,
                status VARCHAR(50),
                message TEXT,
                details TEXT,
                timestamp TIMESTAMP,
                commit TEXT,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Job Log
            """
            CREATE TABLE IF NOT EXISTS wh_job_log (
                id VARCHAR(255) PRIMARY KEY,
                job_name TEXT,
                qa_score NUMERIC,
                cost NUMERIC,
                status VARCHAR(50),
                notes TEXT,
                timestamp TIMESTAMP,
                commit TEXT,
                task_type VARCHAR(100),
                duration_ms INTEGER,
                tokens_in INTEGER,
                tokens_out INTEGER,
                payment_link TEXT,
                payment_status VARCHAR(50),
                client_rate_usd_per_min NUMERIC,
                gross_usd NUMERIC,
                profit_usd NUMERIC,
                margin_pct NUMERIC,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Clients
            """
            CREATE TABLE IF NOT EXISTS wh_clients (
                id VARCHAR(255) PRIMARY KEY,
                client_name TEXT,
                email TEXT,
                rate_usd_per_min NUMERIC,
                active BOOLEAN,
                notes TEXT,
                created_time TIMESTAMP,
                last_edited_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Finance
            """
            CREATE TABLE IF NOT EXISTS wh_finance (
                id VARCHAR(255) PRIMARY KEY,
                transaction_id TEXT,
                date TIMESTAMP,
                type VARCHAR(50),
                amount NUMERIC,
                currency VARCHAR(10),
                client TEXT,
                job_id TEXT,
                margin_pct NUMERIC,
                reconciled BOOLEAN,
                stripe_payment_id TEXT,
                notes TEXT,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Governance
            """
            CREATE TABLE IF NOT EXISTS wh_governance (
                id VARCHAR(255) PRIMARY KEY,
                decision TEXT,
                date TIMESTAMP,
                type VARCHAR(50),
                status VARCHAR(50),
                decision_maker TEXT,
                impact VARCHAR(50),
                rationale TEXT,
                outcomes TEXT,
                related_risks TEXT,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Operations Monitor
            """
            CREATE TABLE IF NOT EXISTS wh_ops_monitor (
                id VARCHAR(255) PRIMARY KEY,
                timestamp_title TEXT,
                component VARCHAR(100),
                status VARCHAR(50),
                metric TEXT,
                value NUMERIC,
                threshold NUMERIC,
                alert_sent BOOLEAN,
                resolution TEXT,
                auto_fixed BOOLEAN,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Forecast
            """
            CREATE TABLE IF NOT EXISTS wh_forecast (
                id VARCHAR(255) PRIMARY KEY,
                date_title TEXT,
                forecast_type VARCHAR(50),
                predicted_value NUMERIC,
                actual_value NUMERIC,
                accuracy_pct NUMERIC,
                confidence VARCHAR(50),
                model_used TEXT,
                notes TEXT,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Regional Compliance
            """
            CREATE TABLE IF NOT EXISTS wh_region_compliance (
                id VARCHAR(255) PRIMARY KEY,
                region TEXT,
                country_code VARCHAR(10),
                data_retention_days INTEGER,
                currency VARCHAR(10),
                language VARCHAR(10),
                gdpr_required BOOLEAN,
                ccpa_required BOOLEAN,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Partners
            """
            CREATE TABLE IF NOT EXISTS wh_partners (
                id VARCHAR(255) PRIMARY KEY,
                partner_name TEXT,
                api_key_hash TEXT,
                tier VARCHAR(50),
                quota_monthly INTEGER,
                usage_current INTEGER,
                revenue_share_pct NUMERIC,
                contact_email TEXT,
                active BOOLEAN,
                created_date TIMESTAMP,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Referrals
            """
            CREATE TABLE IF NOT EXISTS wh_referrals (
                id VARCHAR(255) PRIMARY KEY,
                referral_code TEXT,
                referrer TEXT,
                referred_customer TEXT,
                status VARCHAR(50),
                credit_amount NUMERIC,
                applied BOOLEAN,
                created_date TIMESTAMP,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Growth Metrics
            """
            CREATE TABLE IF NOT EXISTS wh_growth_metrics (
                id VARCHAR(255) PRIMARY KEY,
                date_title TEXT,
                metric VARCHAR(50),
                value NUMERIC,
                source VARCHAR(50),
                campaign TEXT,
                cost NUMERIC,
                roi_pct NUMERIC,
                created_time TIMESTAMP,
                synced_at TIMESTAMP DEFAULT NOW()
            )
            """,
            
            # Sync Metadata
            """
            CREATE TABLE IF NOT EXISTS wh_sync_metadata (
                id SERIAL PRIMARY KEY,
                table_name VARCHAR(100),
                sync_started_at TIMESTAMP,
                sync_completed_at TIMESTAMP,
                rows_synced INTEGER,
                status VARCHAR(50),
                error_message TEXT
            )
            """
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
        
        self.conn.commit()
        cursor.close()
        print(f"✅ Warehouse schema ready")
    
    def extract_text_property(self, props: Dict, key: str) -> Optional[str]:
        """Extract text from Notion property"""
        prop = props.get(key)
        if not prop:
            return None
        
        prop_type = prop.get('type')
        if prop_type == 'title':
            items = prop.get('title', [])
        elif prop_type == 'rich_text':
            items = prop.get('rich_text', [])
        else:
            return None
        
        return ''.join([item.get('plain_text', '') for item in items]) if items else None
    
    def extract_select_property(self, props: Dict, key: str) -> Optional[str]:
        """Extract select value from Notion property"""
        prop = props.get(key)
        if not prop or prop.get('type') != 'select':
            return None
        select = prop.get('select')
        return select.get('name') if select else None
    
    def extract_number_property(self, props: Dict, key: str) -> Optional[float]:
        """Extract number from Notion property"""
        prop = props.get(key)
        if not prop or prop.get('type') != 'number':
            return None
        return prop.get('number')
    
    def extract_checkbox_property(self, props: Dict, key: str) -> bool:
        """Extract checkbox from Notion property"""
        prop = props.get(key)
        if not prop or prop.get('type') != 'checkbox':
            return False
        return prop.get('checkbox', False)
    
    def extract_date_property(self, props: Dict, key: str) -> Optional[str]:
        """Extract date from Notion property"""
        prop = props.get(key)
        if not prop or prop.get('type') != 'date':
            return None
        date_obj = prop.get('date')
        return date_obj.get('start') if date_obj else None
    
    def extract_email_property(self, props: Dict, key: str) -> Optional[str]:
        """Extract email from Notion property"""
        prop = props.get(key)
        if not prop or prop.get('type') != 'email':
            return None
        return prop.get('email')
    
    def sync_automation_queue(self):
        """Sync Automation Queue database"""
        if not config.AUTOMATION_QUEUE_DB_ID:
            print("⚠️  AUTOMATION_QUEUE_DB_ID not configured, skipping")
            return
        
        print("📥 Syncing Automation Queue...")
        pages = self.notion.databases.query(database_id=config.AUTOMATION_QUEUE_DB_ID).get('results', [])
        
        cursor = self.conn.cursor()
        for page in pages:
            props = page.get('properties', {})
            cursor.execute("""
                INSERT INTO wh_automation_queue 
                (id, task_name, description, trigger, status, task_type, qa_target, created_time, last_edited_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    task_name = EXCLUDED.task_name,
                    description = EXCLUDED.description,
                    trigger = EXCLUDED.trigger,
                    status = EXCLUDED.status,
                    task_type = EXCLUDED.task_type,
                    qa_target = EXCLUDED.qa_target,
                    last_edited_time = EXCLUDED.last_edited_time,
                    synced_at = NOW()
            """, (
                page['id'],
                self.extract_text_property(props, 'Task Name'),
                self.extract_text_property(props, 'Description'),
                self.extract_checkbox_property(props, 'Trigger'),
                self.extract_select_property(props, 'Status'),
                self.extract_select_property(props, 'Task Type'),
                self.extract_number_property(props, 'QA Target'),
                page['created_time'],
                page['last_edited_time']
            ))
        
        self.conn.commit()
        cursor.close()
        self.stats['tables_synced'] += 1
        self.stats['rows_inserted'] += len(pages)
        print(f"   ✅ Synced {len(pages)} records")
    
    def sync_job_log(self):
        """Sync Job Log database"""
        if not config.JOB_LOG_DB_ID:
            print("⚠️  JOB_LOG_DB_ID not configured, skipping")
            return
        
        print("📥 Syncing Job Log...")
        pages = self.notion.databases.query(database_id=config.JOB_LOG_DB_ID).get('results', [])
        
        cursor = self.conn.cursor()
        for page in pages:
            props = page.get('properties', {})
            cursor.execute("""
                INSERT INTO wh_job_log 
                (id, job_name, qa_score, cost, status, notes, timestamp, commit, task_type, 
                 duration_ms, tokens_in, tokens_out, payment_status, client_rate_usd_per_min,
                 gross_usd, profit_usd, margin_pct, created_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    qa_score = EXCLUDED.qa_score,
                    cost = EXCLUDED.cost,
                    status = EXCLUDED.status,
                    payment_status = EXCLUDED.payment_status,
                    synced_at = NOW()
            """, (
                page['id'],
                self.extract_text_property(props, 'Job Name'),
                self.extract_number_property(props, 'QA Score'),
                self.extract_number_property(props, 'Cost'),
                self.extract_select_property(props, 'Status'),
                self.extract_text_property(props, 'Notes'),
                self.extract_date_property(props, 'Timestamp'),
                self.extract_text_property(props, 'Commit'),
                self.extract_select_property(props, 'Task Type'),
                self.extract_number_property(props, 'Duration (ms)'),
                self.extract_number_property(props, 'Tokens In'),
                self.extract_number_property(props, 'Tokens Out'),
                self.extract_select_property(props, 'Payment Status'),
                self.extract_number_property(props, 'Client Rate USD/min'),
                self.extract_number_property(props, 'Gross USD'),
                self.extract_number_property(props, 'Profit USD'),
                self.extract_number_property(props, 'Margin %'),
                page['created_time']
            ))
        
        self.conn.commit()
        cursor.close()
        self.stats['tables_synced'] += 1
        self.stats['rows_inserted'] += len(pages)
        print(f"   ✅ Synced {len(pages)} records")
    
    def sync_finance(self):
        """Sync Finance database"""
        if not config.NOTION_FINANCE_DB_ID:
            print("⚠️  NOTION_FINANCE_DB_ID not configured, skipping")
            return
        
        print("📥 Syncing Finance...")
        pages = self.notion.databases.query(database_id=config.NOTION_FINANCE_DB_ID).get('results', [])
        
        cursor = self.conn.cursor()
        for page in pages:
            props = page.get('properties', {})
            cursor.execute("""
                INSERT INTO wh_finance 
                (id, transaction_id, date, type, amount, currency, client, job_id, 
                 margin_pct, reconciled, stripe_payment_id, notes, created_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    amount = EXCLUDED.amount,
                    reconciled = EXCLUDED.reconciled,
                    synced_at = NOW()
            """, (
                page['id'],
                self.extract_text_property(props, 'Transaction ID'),
                self.extract_date_property(props, 'Date'),
                self.extract_select_property(props, 'Type'),
                self.extract_number_property(props, 'Amount'),
                self.extract_select_property(props, 'Currency'),
                self.extract_text_property(props, 'Client'),
                self.extract_text_property(props, 'Job ID'),
                self.extract_number_property(props, 'Margin %'),
                self.extract_checkbox_property(props, 'Reconciled'),
                self.extract_text_property(props, 'Stripe Payment ID'),
                self.extract_text_property(props, 'Notes'),
                page['created_time']
            ))
        
        self.conn.commit()
        cursor.close()
        self.stats['tables_synced'] += 1
        self.stats['rows_inserted'] += len(pages)
        print(f"   ✅ Synced {len(pages)} records")
    
    def sync_partners(self):
        """Sync Partners database"""
        if not config.NOTION_PARTNERS_DB_ID:
            print("⚠️  NOTION_PARTNERS_DB_ID not configured, skipping")
            return
        
        print("📥 Syncing Partners...")
        pages = self.notion.databases.query(database_id=config.NOTION_PARTNERS_DB_ID).get('results', [])
        
        cursor = self.conn.cursor()
        for page in pages:
            props = page.get('properties', {})
            # Hash API key for security (only store first 8 chars)
            api_key = self.extract_text_property(props, 'API Key')
            api_key_hash = api_key[:8] + '***' if api_key else None
            
            cursor.execute("""
                INSERT INTO wh_partners 
                (id, partner_name, api_key_hash, tier, quota_monthly, usage_current, 
                 revenue_share_pct, contact_email, active, created_date, created_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    usage_current = EXCLUDED.usage_current,
                    active = EXCLUDED.active,
                    synced_at = NOW()
            """, (
                page['id'],
                self.extract_text_property(props, 'Partner Name'),
                api_key_hash,
                self.extract_select_property(props, 'Tier'),
                self.extract_number_property(props, 'Quota (monthly)'),
                self.extract_number_property(props, 'Usage (current)'),
                self.extract_number_property(props, 'Revenue Share %'),
                self.extract_email_property(props, 'Contact Email'),
                self.extract_checkbox_property(props, 'Active'),
                self.extract_date_property(props, 'Created Date'),
                page['created_time']
            ))
        
        self.conn.commit()
        cursor.close()
        self.stats['tables_synced'] += 1
        self.stats['rows_inserted'] += len(pages)
        print(f"   ✅ Synced {len(pages)} records")
    
    def sync_growth_metrics(self):
        """Sync Growth Metrics database"""
        if not config.NOTION_GROWTH_METRICS_DB_ID:
            print("⚠️  NOTION_GROWTH_METRICS_DB_ID not configured, skipping")
            return
        
        print("📥 Syncing Growth Metrics...")
        pages = self.notion.databases.query(database_id=config.NOTION_GROWTH_METRICS_DB_ID).get('results', [])
        
        cursor = self.conn.cursor()
        for page in pages:
            props = page.get('properties', {})
            cursor.execute("""
                INSERT INTO wh_growth_metrics 
                (id, date_title, metric, value, source, campaign, cost, roi_pct, created_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    value = EXCLUDED.value,
                    cost = EXCLUDED.cost,
                    roi_pct = EXCLUDED.roi_pct,
                    synced_at = NOW()
            """, (
                page['id'],
                self.extract_text_property(props, 'Date'),
                self.extract_select_property(props, 'Metric'),
                self.extract_number_property(props, 'Value'),
                self.extract_select_property(props, 'Source'),
                self.extract_text_property(props, 'Campaign'),
                self.extract_number_property(props, 'Cost'),
                self.extract_number_property(props, 'ROI %'),
                page['created_time']
            ))
        
        self.conn.commit()
        cursor.close()
        self.stats['tables_synced'] += 1
        self.stats['rows_inserted'] += len(pages)
        print(f"   ✅ Synced {len(pages)} records")
    
    def log_sync_metadata(self, table_name: str, status: str, rows: int, error: str = None):
        """Log sync metadata to warehouse"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO wh_sync_metadata (table_name, sync_started_at, sync_completed_at, rows_synced, status, error_message)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (table_name, self.start_time, datetime.utcnow(), rows, status, error))
        self.conn.commit()
        cursor.close()
    
    def run_full_sync(self):
        """Run full ETL sync from Notion to Postgres"""
        print("="*70)
        print("DATA WAREHOUSE ETL SYNC")
        print(f"Started: {self.start_time.isoformat()}")
        print("="*70)
        
        try:
            self.connect_postgres()
            self.create_schema()
            
            # Sync all databases
            self.sync_automation_queue()
            self.sync_job_log()
            self.sync_finance()
            self.sync_partners()
            self.sync_growth_metrics()
            
            # Calculate duration
            duration = (datetime.utcnow() - self.start_time).total_seconds()
            
            print("\n" + "="*70)
            print("SYNC COMPLETE")
            print("="*70)
            print(f"Tables synced: {self.stats['tables_synced']}")
            print(f"Rows inserted/updated: {self.stats['rows_inserted']}")
            print(f"Duration: {duration:.2f}s")
            print("="*70)
            
            # Log final metadata
            self.log_sync_metadata('ALL', 'SUCCESS', self.stats['rows_inserted'])
            
            # Write summary to NDJSON
            os.makedirs('logs', exist_ok=True)
            with open('logs/warehouse_sync.ndjson', 'a') as f:
                f.write(json.dumps({
                    "ok": True,
                    "ts": datetime.utcnow().isoformat() + "Z",
                    "tables_synced": self.stats['tables_synced'],
                    "rows_synced": self.stats['rows_inserted'],
                    "duration_secs": duration
                }) + '\n')
            
        except Exception as e:
            print(f"\n❌ Sync failed: {e}")
            self.stats['errors'] += 1
            self.log_sync_metadata('ALL', 'FAILED', 0, str(e))
            
            # Log error to NDJSON
            os.makedirs('logs', exist_ok=True)
            with open('logs/warehouse_sync.ndjson', 'a') as f:
                f.write(json.dumps({
                    "ok": False,
                    "ts": datetime.utcnow().isoformat() + "Z",
                    "error": str(e)
                }) + '\n')
            raise
        finally:
            if self.conn:
                self.conn.close()


def main():
    sync = WarehouseSync()
    sync.run_full_sync()


if __name__ == '__main__':
    main()
