"""
Visual Workflow Builder - Phase 51: Foundation
Manages workflow definitions, templates, and execution
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WORKFLOWS_DIR = Path("data/workflows")
TEMPLATES_DIR = Path("data/workflow_templates")

def ensure_dirs():
    """Ensure workflow directories exist"""
    WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

def generate_workflow_id():
    """Generate unique workflow ID"""
    return str(uuid.uuid4())[:8]

def create_workflow(user_id: str, name: str, description: str = "", template_id: Optional[str] = None):
    """Create a new workflow"""
    ensure_dirs()
    
    workflow_id = generate_workflow_id()
    
    # If template provided, clone it
    if template_id:
        template_path = TEMPLATES_DIR / f"{template_id}.json"
        if template_path.exists():
            template_data = json.loads(template_path.read_text())
            nodes = template_data.get("nodes", [])
            edges = template_data.get("edges", [])
        else:
            nodes = []
            edges = []
    else:
        nodes = []
        edges = []
    
    workflow = {
        "id": workflow_id,
        "user_id": user_id,
        "name": name,
        "description": description,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "status": "draft",
        "nodes": nodes,
        "edges": edges,
        "settings": {
            "trigger_type": "manual",
            "schedule": None,
            "enabled": False
        }
    }
    
    workflow_path = WORKFLOWS_DIR / f"{workflow_id}.json"
    workflow_path.write_text(json.dumps(workflow, indent=2))
    
    return {"ok": True, "workflow_id": workflow_id, "workflow": workflow}

def get_workflow(workflow_id: str):
    """Get workflow by ID"""
    ensure_dirs()
    
    workflow_path = WORKFLOWS_DIR / f"{workflow_id}.json"
    if not workflow_path.exists():
        return {"ok": False, "error": "Workflow not found"}
    
    workflow = json.loads(workflow_path.read_text())
    return {"ok": True, "workflow": workflow}

def update_workflow(workflow_id: str, updates: Dict):
    """Update workflow"""
    ensure_dirs()
    
    workflow_path = WORKFLOWS_DIR / f"{workflow_id}.json"
    if not workflow_path.exists():
        return {"ok": False, "error": "Workflow not found"}
    
    workflow = json.loads(workflow_path.read_text())
    
    # Update fields
    if "name" in updates:
        workflow["name"] = updates["name"]
    if "description" in updates:
        workflow["description"] = updates["description"]
    if "nodes" in updates:
        workflow["nodes"] = updates["nodes"]
    if "edges" in updates:
        workflow["edges"] = updates["edges"]
    if "settings" in updates:
        workflow["settings"].update(updates["settings"])
    if "status" in updates:
        workflow["status"] = updates["status"]
    
    workflow["updated_at"] = datetime.utcnow().isoformat()
    
    workflow_path.write_text(json.dumps(workflow, indent=2))
    
    return {"ok": True, "workflow": workflow}

def delete_workflow(workflow_id: str):
    """Delete workflow"""
    ensure_dirs()
    
    workflow_path = WORKFLOWS_DIR / f"{workflow_id}.json"
    if not workflow_path.exists():
        return {"ok": False, "error": "Workflow not found"}
    
    workflow_path.unlink()
    return {"ok": True, "deleted": workflow_id}

def list_workflows(user_id: Optional[str] = None):
    """List all workflows, optionally filtered by user"""
    ensure_dirs()
    
    workflows = []
    for workflow_path in WORKFLOWS_DIR.glob("*.json"):
        workflow = json.loads(workflow_path.read_text())
        
        # Filter by user if specified
        if user_id and workflow.get("user_id") != user_id:
            continue
        
        # Return summary only
        workflows.append({
            "id": workflow["id"],
            "name": workflow["name"],
            "description": workflow["description"],
            "status": workflow["status"],
            "created_at": workflow["created_at"],
            "updated_at": workflow["updated_at"],
            "node_count": len(workflow.get("nodes", [])),
            "enabled": workflow.get("settings", {}).get("enabled", False)
        })
    
    # Sort by updated_at desc
    workflows.sort(key=lambda x: x["updated_at"], reverse=True)
    
    return {"ok": True, "workflows": workflows, "count": len(workflows)}

def get_available_node_types():
    """Get available node types for workflow builder"""
    return {
        "ok": True,
        "node_types": [
            {
                "type": "trigger",
                "name": "Trigger",
                "icon": "⚡",
                "color": "#667eea",
                "inputs": 0,
                "outputs": 1,
                "config": ["trigger_type", "schedule"]
            },
            {
                "type": "ai_task",
                "name": "AI Task",
                "icon": "🤖",
                "color": "#48bb78",
                "inputs": 1,
                "outputs": 2,
                "config": ["prompt", "model", "temperature"]
            },
            {
                "type": "condition",
                "name": "Condition",
                "icon": "🔀",
                "color": "#f6ad55",
                "inputs": 1,
                "outputs": 2,
                "config": ["condition_type", "field", "operator", "value"]
            },
            {
                "type": "action",
                "name": "Action",
                "icon": "⚙️",
                "color": "#764ba2",
                "inputs": 1,
                "outputs": 1,
                "config": ["action_type", "parameters"]
            },
            {
                "type": "notification",
                "name": "Notification",
                "icon": "📧",
                "color": "#38b2ac",
                "inputs": 1,
                "outputs": 0,
                "config": ["notification_type", "recipient", "message"]
            },
            {
                "type": "delay",
                "name": "Delay",
                "icon": "⏱️",
                "color": "#ed8936",
                "inputs": 1,
                "outputs": 1,
                "config": ["duration", "unit"]
            }
        ]
    }

def create_template(name: str, description: str, nodes: List, edges: List):
    """Create a workflow template"""
    ensure_dirs()
    
    template_id = generate_workflow_id()
    
    template = {
        "id": template_id,
        "name": name,
        "description": description,
        "created_at": datetime.utcnow().isoformat(),
        "nodes": nodes,
        "edges": edges,
        "category": "custom"
    }
    
    template_path = TEMPLATES_DIR / f"{template_id}.json"
    template_path.write_text(json.dumps(template, indent=2))
    
    return {"ok": True, "template_id": template_id}

def list_templates():
    """List all workflow templates"""
    ensure_dirs()
    
    templates = []
    for template_path in TEMPLATES_DIR.glob("*.json"):
        template = json.loads(template_path.read_text())
        templates.append({
            "id": template["id"],
            "name": template["name"],
            "description": template["description"],
            "category": template.get("category", "custom"),
            "node_count": len(template.get("nodes", []))
        })
    
    return {"ok": True, "templates": templates}

def initialize_default_templates():
    """Create default workflow templates on first run"""
    ensure_dirs()
    
    # Check if templates already exist
    if len(list(TEMPLATES_DIR.glob("*.json"))) > 0:
        return {"ok": True, "message": "Templates already initialized"}
    
    # Template 1: Simple AI Processing
    create_template(
        name="Simple AI Processing",
        description="Single AI task with notification",
        nodes=[
            {"id": "trigger-1", "type": "trigger", "position": {"x": 100, "y": 100}, "data": {"label": "Manual Trigger"}},
            {"id": "ai-1", "type": "ai_task", "position": {"x": 300, "y": 100}, "data": {"label": "Process with AI"}},
            {"id": "notify-1", "type": "notification", "position": {"x": 500, "y": 100}, "data": {"label": "Send Result"}}
        ],
        edges=[
            {"id": "e1", "source": "trigger-1", "target": "ai-1"},
            {"id": "e2", "source": "ai-1", "target": "notify-1"}
        ]
    )
    
    # Template 2: Conditional Workflow
    create_template(
        name="Conditional Processing",
        description="AI task with conditional branching",
        nodes=[
            {"id": "trigger-1", "type": "trigger", "position": {"x": 100, "y": 150}},
            {"id": "ai-1", "type": "ai_task", "position": {"x": 300, "y": 150}},
            {"id": "cond-1", "type": "condition", "position": {"x": 500, "y": 150}},
            {"id": "action-1", "type": "action", "position": {"x": 700, "y": 100}},
            {"id": "action-2", "type": "action", "position": {"x": 700, "y": 200}}
        ],
        edges=[
            {"id": "e1", "source": "trigger-1", "target": "ai-1"},
            {"id": "e2", "source": "ai-1", "target": "cond-1"},
            {"id": "e3", "source": "cond-1", "target": "action-1", "sourceHandle": "true"},
            {"id": "e4", "source": "cond-1", "target": "action-2", "sourceHandle": "false"}
        ]
    )
    
    return {"ok": True, "message": "Default templates created"}
