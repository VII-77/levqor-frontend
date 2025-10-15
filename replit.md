# EchoPilot AI Automation Bot

## Overview

EchoPilot is an intelligent automation bot that polls Notion databases for triggered tasks, processes them using AI (OpenAI via Replit AI Integrations), and maintains comprehensive logging and quality assurance. The system operates on a 60-second polling cycle, automatically processing tasks marked with a trigger flag, evaluating quality with a 95% target score, and tracking job performance metrics including costs and QA scores.

**Current Status**: ✅ Bot is LIVE and RUNNING in demo mode. Ready to switch to production with Notion database IDs.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Architecture Pattern

**Polling-Based Event-Driven System**
- The application uses a scheduled polling mechanism (60-second intervals) rather than webhooks or event streaming
- Tasks are queued in Notion, triggered by checkbox activation, and processed sequentially
- This approach was chosen for simplicity and reliability with Notion's API limitations
- Trade-off: Higher API usage and slight latency vs. real-time webhooks, but more predictable and easier to debug

### Application Structure

**Modular Component Design**
- `main.py`: Orchestration layer with health checks and polling scheduler (entry point)
- `processor.py`: Task processing logic with AI integration and QA scoring
- `notion_api.py`: Notion client wrapper for database operations (renamed from notion_client.py to avoid circular imports)
- `google_drive_client.py`: Google Drive integration for file handling
- `config.py`: Centralized configuration management
- `README.md`: Complete setup and usage documentation
- Rationale: Separation of concerns allows independent testing and maintenance of each integration point

### AI Integration

**OpenAI via Replit AI Integrations**
- Uses OpenAI's GPT-4o-mini model for task processing and QA evaluation
- Authentication handled through Replit's AI integration environment variables
- Custom base URL configuration for Replit's AI proxy
- Temperature set to 0.3 for QA scoring to ensure consistent evaluations
- Choice rationale: Replit's managed integration simplifies API key management and provides cost tracking

### Quality Assurance System

**Automated QA Scoring (0-100 scale)**
- Multi-criteria evaluation: Clarity (30%), Accuracy (30%), Completeness (20%), Professional tone (20%)
- Target threshold: 95% pass rate
- AI-powered evaluation using structured prompts with constrained outputs (number-only responses)
- Scores stored in job logs for performance tracking
- Design decision: Automated QA reduces manual review burden while maintaining quality standards

### Authentication & Token Management

**Replit Connectors OAuth Flow (Python Implementation)**
- Dynamic token refresh mechanism for Notion and Google Drive
- Token expiration checking with automatic renewal using Python requests library
- Supports both REPL and deployment (DEPL) identity tokens via environment variables
- Uses Replit's connector hostname for centralized credential management
- Python implementation adapts JavaScript connector pattern to work with Python SDKs
- Architecture choice: Leverages Replit's infrastructure for secure credential storage rather than managing OAuth flows manually

### Data Flow Architecture

**Three-Database System in Notion**

1. **Automation Queue Database** (Input)
   - Properties: Task Name, Description, Trigger (checkbox), Status (select)
   - Bot polls for Trigger=true records
   - Status updated during processing lifecycle

2. **Automation Log Database** (Audit Trail)
   - Properties: Task, Status, Message, Details, Timestamp
   - Records all bot activities (processing, success, error, warning states)
   - Provides complete audit history

3. **EchoPilot Job Log Database** (Performance Metrics)
   - Properties: Job Name, QA Score, Cost, Status, Notes, Timestamp
   - Tracks completed jobs with quality and cost metrics
   - Enables performance analysis and optimization

**Design rationale**: Separation into three databases allows concurrent access patterns (read queue, write logs) without lock contention, and provides clear data ownership boundaries.

### Scheduling & Process Management

**Schedule-Based Polling System**
- 60-second polling interval defined in config
- Health check mechanism for system status monitoring
- Graceful error handling with status reporting
- Alternative considered: Webhook-based triggers were not used due to Notion API webhook limitations and complexity of managing callback URLs in Replit environment

### Error Handling Strategy

**Multi-Level Error Management**
- Connection-level: Token refresh and API connectivity validation
- Task-level: Individual task failures don't crash the bot
- Logging-level: All errors captured in Automation Log database
- Health check endpoint provides system status visibility
- Approach ensures resilience and debuggability in production

## External Dependencies

### Third-Party APIs

**Notion API**
- Purpose: Primary data storage and task queue management
- Integration: Via official `notion-client` Python SDK
- Authentication: OAuth2 via Replit Connectors
- Database IDs required: AUTOMATION_QUEUE_DB_ID, AUTOMATION_LOG_DB_ID, JOB_LOG_DB_ID

**OpenAI API**
- Purpose: AI-powered task processing and QA evaluation
- Model: GPT-4o-mini for cost optimization
- Integration: Via official `openai` Python SDK
- Configuration: Custom base URL through Replit AI Integrations (AI_INTEGRATIONS_OPENAI_API_KEY, AI_INTEGRATIONS_OPENAI_BASE_URL)

**Google Drive API**
- Purpose: File handling and storage capabilities
- Integration: Via `googleapiclient` library
- Authentication: OAuth2 via Replit Connectors
- Note: Client wrapper implemented but file operations not fully shown in current codebase

### Python Dependencies

**Core Libraries**
- `notion-client`: Official Notion SDK for database operations
- `openai`: Official OpenAI SDK for AI completions
- `google-api-python-client`: Google Drive integration
- `google-auth`: OAuth2 credential management
- `requests`: HTTP client for Replit Connectors API
- `schedule`: Task scheduling for polling mechanism
- `python-dotenv`: Environment variable management

### Replit-Specific Infrastructure

**Replit Connectors API**
- Hostname: REPLIT_CONNECTORS_HOSTNAME environment variable
- Provides centralized OAuth token management for Notion and Google Drive
- Endpoint: `/api/v2/connection` for credential retrieval
- Identity tokens: REPL_IDENTITY (development) or WEB_REPL_RENEWAL (deployment)

**Replit AI Integrations**
- Managed OpenAI API access with built-in cost tracking
- Environment variables for API key and base URL
- Eliminates need for separate OpenAI account management

### Configuration Requirements

**Required Environment Variables**
- `AI_INTEGRATIONS_OPENAI_API_KEY`: OpenAI API key via Replit
- `AI_INTEGRATIONS_OPENAI_BASE_URL`: Custom base URL for Replit AI proxy
- `REPLIT_CONNECTORS_HOSTNAME`: Replit connectors service hostname
- `REPL_IDENTITY` or `WEB_REPL_RENEWAL`: Replit authentication tokens
- `AUTOMATION_QUEUE_DB_ID`: Notion database ID for task queue
- `AUTOMATION_LOG_DB_ID`: Notion database ID for activity logs
- `JOB_LOG_DB_ID`: Notion database ID for job metrics

**Application Constants**
- `POLL_INTERVAL_SECONDS`: 60 (polling frequency)
- `QA_TARGET_SCORE`: 95 (quality threshold percentage)