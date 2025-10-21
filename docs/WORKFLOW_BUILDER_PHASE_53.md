# Visual Workflow Builder - Phase 53: Enhanced Node Configuration 🔧

**Status:** 🚧 IN PROGRESS  
**Date:** October 21, 2025  
**Goal:** Advanced node configuration with validation and enhanced UI

## Objectives

Transform basic nodes into fully configurable components with:
1. Dynamic configuration panels
2. Input/output validation
3. Node copy/paste functionality
4. Enhanced visual feedback
5. Error states and warnings

## Planned Features

### 1. **Dynamic Configuration Panels**
Each node type will have a custom configuration UI:

**Trigger Node:**
- Trigger type selector (Notion, Webhook, Schedule, Manual)
- Database/endpoint configuration
- Filter conditions
- Polling interval settings

**AI Task Node:**
- Model selector (GPT-4o, GPT-4o-mini, Claude)
- System prompt editor
- Temperature slider
- Max tokens input
- Cost estimation

**Condition Node:**
- Condition builder (if/then/else)
- Field selector
- Operator selector (equals, contains, greater than, etc.)
- Value input
- Multiple condition support (AND/OR)

**Action Node:**
- Action type (Update Notion, Send Email, API Call)
- Field mapping
- Template editor
- Test action button

**Notification Node:**
- Channel selector (Email, Telegram, Webhook)
- Recipient configuration
- Message template
- Priority level

**Delay Node:**
- Duration input
- Unit selector (seconds, minutes, hours, days)
- Preview of execution time

### 2. **Input/Output Validation**
- Type checking for connections
- Required field validation
- Format validation (email, URL, JSON)
- Warning indicators
- Error tooltips

### 3. **Node Operations**
- Copy node (Ctrl+C / Cmd+C)
- Paste node (Ctrl+V / Cmd+V)
- Duplicate node (Ctrl+D / Cmd+D)
- Delete node (Delete / Backspace)
- Rename node (double-click label)

### 4. **Enhanced Visual States**
- Configuration incomplete (yellow border)
- Configuration error (red border)
- Validation warning (orange indicator)
- Active/running (blue pulse)
- Disabled (gray opacity)

### 5. **Connection Validation**
- Type compatibility checking
- Prevent invalid connections
- Visual feedback on hover
- Connection labels
- Multi-output support

## Technical Design

### Node Configuration Schema

```typescript
interface NodeConfig {
  id: string;
  type: string;
  label: string;
  config: {
    [key: string]: any;
  };
  validation: {
    valid: boolean;
    errors: string[];
    warnings: string[];
  };
}
```

### Configuration Panels

```javascript
class NodeConfigPanel {
  constructor(nodeType) {
    this.nodeType = nodeType;
    this.fields = [];
  }
  
  render(node) {
    // Generate dynamic form based on node type
  }
  
  validate(config) {
    // Validate configuration
  }
  
  save(config) {
    // Save to node and workflow
  }
}
```

### Validation Rules

```javascript
const validationRules = {
  trigger: {
    required: ['trigger_type', 'source'],
    types: {
      trigger_type: 'string',
      source: 'string'
    }
  },
  ai_task: {
    required: ['model', 'prompt'],
    types: {
      model: 'string',
      prompt: 'string',
      temperature: 'number',
      max_tokens: 'number'
    },
    ranges: {
      temperature: [0, 2],
      max_tokens: [1, 4096]
    }
  }
  // ... more rules
};
```

## UI Components

### Configuration Panel Layout
```
┌─────────────────────────────┐
│ Node: AI Task              │
│                            │
│ ┌────────────────────────┐ │
│ │ Model                  │ │
│ │ [GPT-4o ▼]            │ │
│ └────────────────────────┘ │
│                            │
│ ┌────────────────────────┐ │
│ │ System Prompt          │ │
│ │ [                    ] │ │
│ │ [                    ] │ │
│ └────────────────────────┘ │
│                            │
│ Temperature: [0.7]         │
│ ├──────────────────────┤   │
│ 0                    2     │
│                            │
│ Max Tokens: [2000]         │
│                            │
│ Estimated Cost: $0.02      │
│                            │
│ [Test]  [Save]  [Cancel]   │
└─────────────────────────────┘
```

### Error Indicators
```html
<div class="workflow-node error">
  <div class="node-error-indicator" title="Configuration incomplete">
    ⚠️
  </div>
  <!-- node content -->
</div>
```

## Implementation Plan

### Step 1: Configuration Schema (30 mins)
- Define configuration schema for each node type
- Create validation rules
- Build validation engine

### Step 2: Dynamic Forms (45 mins)
- Build form generator
- Create input components
- Add validation UI

### Step 3: Node Operations (30 mins)
- Implement copy/paste
- Add keyboard shortcuts
- Create context menu

### Step 4: Visual Enhancements (30 mins)
- Add error states
- Create warning indicators
- Enhance hover effects

### Step 5: Connection Validation (30 mins)
- Type compatibility checks
- Prevent invalid connections
- Add connection labels

**Total Estimated Time:** 2.5 hours

## API Endpoints

### Update Node Configuration
```
PUT /api/workflow/:workflow_id/node/:node_id/config
Body: { config: {...}, validation: {...} }
Response: { ok: true, node: {...} }
```

### Validate Node Configuration
```
POST /api/workflow/validate-node
Body: { type: "ai_task", config: {...} }
Response: { valid: true, errors: [], warnings: [] }
```

## Files to Modify

```
static/workflow-canvas.js          Add config panels
static/workflow-canvas.css         Add error states
templates/workflow_builder.html    Add config UI
bot/workflow_builder.py            Add validation
```

## Success Criteria

- ✅ All 6 node types have configuration panels
- ✅ Validation rules prevent invalid workflows
- ✅ Copy/paste works correctly
- ✅ Visual feedback for all states
- ✅ No breaking changes to Phase 51-52

---

**Next:** Begin implementation of Phase 53 configuration panels
