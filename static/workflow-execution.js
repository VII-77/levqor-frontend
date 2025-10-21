/**
 * Visual Workflow Builder - Phase 55: Live Execution
 * Real-time workflow execution with visual feedback
 */

class WorkflowExecutor {
    constructor() {
        this.isExecuting = false;
        this.currentExecution = null;
        this.executionLog = [];
        this.debugMode = false;
    }
    
    async executeWorkflow(workflowId, testData = null) {
        if (this.isExecuting) {
            alert('A workflow is already running. Please wait...');
            return;
        }
        
        this.isExecuting = true;
        this.executionLog = [];
        this.showExecutionPanel();
        
        try {
            // Get workflow data
            const workflow = this.getCurrentWorkflowData();
            if (!workflow || !workflow.nodes || workflow.nodes.length === 0) {
                throw new Error('No workflow to execute');
            }
            
            // Find trigger node
            const triggerNode = workflow.nodes.find(n => n.type === 'trigger');
            if (!triggerNode) {
                throw new Error('Workflow must have a trigger node');
            }
            
            // Start execution
            this.addLog('info', 'Starting workflow execution...');
            this.updateNodeStatus(triggerNode.id, 'running');
            
            // Execute from trigger
            await this.executeNode(triggerNode, workflow, testData || {});
            
            this.addLog('success', '✅ Workflow completed successfully!');
            
        } catch (error) {
            this.addLog('error', `❌ Execution failed: ${error.message}`);
            console.error('Workflow execution error:', error);
        } finally {
            this.isExecuting = false;
            this.resetNodeStatuses();
        }
    }
    
    async executeNode(node, workflow, context) {
        this.updateNodeStatus(node.id, 'running');
        this.addLog('info', `▶️ Executing: ${node.data.label} (${node.type})`);
        
        let result = null;
        
        try {
            // Execute based on node type
            switch (node.type) {
                case 'trigger':
                    result = await this.executeTrigger(node, context);
                    break;
                case 'ai_task':
                    result = await this.executeAITask(node, context);
                    break;
                case 'condition':
                    result = await this.executeCondition(node, context);
                    break;
                case 'action':
                    result = await this.executeAction(node, context);
                    break;
                case 'notification':
                    result = await this.executeNotification(node, context);
                    break;
                case 'delay':
                    result = await this.executeDelay(node, context);
                    break;
                default:
                    throw new Error(`Unknown node type: ${node.type}`);
            }
            
            this.updateNodeStatus(node.id, 'success');
            this.addLog('success', `✅ ${node.data.label} completed`);
            
            // Find and execute next nodes
            const nextNodes = this.getNextNodes(node.id, workflow, result);
            for (const nextNode of nextNodes) {
                await this.executeNode(nextNode, workflow, { ...context, ...result });
            }
            
        } catch (error) {
            this.updateNodeStatus(node.id, 'error');
            this.addLog('error', `❌ ${node.data.label} failed: ${error.message}`);
            throw error;
        }
    }
    
    async executeTrigger(node, context) {
        // Simulate trigger execution
        await this.delay(500);
        return {
            triggered: true,
            timestamp: new Date().toISOString(),
            data: context
        };
    }
    
    async executeAITask(node, context) {
        const config = node.config || {};
        this.addLog('info', `🤖 Calling AI model: ${config.model || 'gpt-4o-mini'}`);
        
        // Check if we have test data
        if (this.debugMode && context.testInput) {
            await this.delay(1000);
            return {
                ai_output: `[SIMULATED] AI response for: ${context.testInput}`,
                model: config.model || 'gpt-4o-mini',
                tokens: 150
            };
        }
        
        // Call actual AI API
        try {
            const response = await fetch('/api/workflow/execute/ai', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Dash-Key': localStorage.getItem('dashKey') || 'temp'
                },
                body: JSON.stringify({
                    model: config.model || 'gpt-4o-mini',
                    system_prompt: config.system_prompt || 'You are a helpful assistant.',
                    user_message: context.data || 'Process this task.',
                    temperature: parseFloat(config.temperature || '0.7'),
                    max_tokens: parseInt(config.max_tokens || '2000')
                })
            });
            
            const data = await response.json();
            if (!data.ok) {
                throw new Error(data.error || 'AI task failed');
            }
            
            this.addLog('success', `✅ AI response received (${data.tokens} tokens)`);
            return {
                ai_output: data.response,
                model: data.model,
                tokens: data.tokens,
                cost: data.cost
            };
            
        } catch (error) {
            this.addLog('error', `AI API error: ${error.message}`);
            throw error;
        }
    }
    
    async executeCondition(node, context) {
        const config = node.config || {};
        const field = config.field || 'status';
        const operator = config.operator || 'equals';
        const value = config.value || '';
        
        const fieldValue = context[field] || '';
        let conditionMet = false;
        
        switch (operator) {
            case 'equals':
                conditionMet = fieldValue == value;
                break;
            case 'not_equals':
                conditionMet = fieldValue != value;
                break;
            case 'contains':
                conditionMet = String(fieldValue).includes(value);
                break;
            case 'greater_than':
                conditionMet = parseFloat(fieldValue) > parseFloat(value);
                break;
            case 'less_than':
                conditionMet = parseFloat(fieldValue) < parseFloat(value);
                break;
            default:
                conditionMet = false;
        }
        
        this.addLog('info', `Condition: ${field} ${operator} ${value} = ${conditionMet ? '✅ TRUE' : '❌ FALSE'}`);
        
        await this.delay(300);
        return {
            condition_met: conditionMet,
            branch: conditionMet ? 'true' : 'false'
        };
    }
    
    async executeAction(node, context) {
        const config = node.config || {};
        this.addLog('info', `⚡ Action: ${config.action_type || 'unknown'}`);
        
        // Simulate action execution
        await this.delay(800);
        
        return {
            action_completed: true,
            action_type: config.action_type,
            target: config.target
        };
    }
    
    async executeNotification(node, context) {
        const config = node.config || {};
        const channel = config.channel || 'email';
        const recipient = config.recipient || 'user@example.com';
        
        this.addLog('info', `📧 Sending ${channel} to ${recipient}`);
        
        // Simulate notification
        await this.delay(500);
        
        return {
            notification_sent: true,
            channel: channel,
            recipient: recipient
        };
    }
    
    async executeDelay(node, context) {
        const config = node.config || {};
        const duration = parseInt(config.duration || '5');
        const unit = config.unit || 'seconds';
        
        let ms = duration * 1000;
        if (unit === 'minutes') ms = duration * 60000;
        if (unit === 'hours') ms = duration * 3600000;
        
        // Cap at 10 seconds for demo
        ms = Math.min(ms, 10000);
        
        this.addLog('info', `⏱️ Waiting ${duration} ${unit}...`);
        await this.delay(ms);
        
        return {
            delay_completed: true,
            waited_ms: ms
        };
    }
    
    getNextNodes(nodeId, workflow, result) {
        const edges = workflow.edges || [];
        const nextEdges = edges.filter(e => e.source === nodeId);
        
        // For condition nodes, filter by branch
        const currentNode = workflow.nodes.find(n => n.id === nodeId);
        if (currentNode && currentNode.type === 'condition' && result) {
            // In a real implementation, edges would have a 'branch' property
            // For now, first edge is 'true' branch, second is 'false'
            const branchIndex = result.condition_met ? 0 : 1;
            const targetEdge = nextEdges[branchIndex];
            if (!targetEdge) return [];
            return [workflow.nodes.find(n => n.id === targetEdge.target)].filter(Boolean);
        }
        
        return nextEdges
            .map(e => workflow.nodes.find(n => n.id === e.target))
            .filter(Boolean);
    }
    
    updateNodeStatus(nodeId, status) {
        const node = document.getElementById(nodeId);
        if (!node) return;
        
        // Remove all status classes
        node.classList.remove('exec-idle', 'exec-running', 'exec-success', 'exec-error');
        
        // Add new status
        node.classList.add(`exec-${status}`);
    }
    
    resetNodeStatuses() {
        document.querySelectorAll('.workflow-node').forEach(node => {
            node.classList.remove('exec-idle', 'exec-running', 'exec-success', 'exec-error');
        });
    }
    
    addLog(type, message) {
        const timestamp = new Date().toLocaleTimeString();
        this.executionLog.push({ type, message, timestamp });
        this.renderLog();
    }
    
    renderLog() {
        const logPanel = document.getElementById('execution-log-content');
        if (!logPanel) return;
        
        const logHtml = this.executionLog.map(log => {
            const icon = {
                'info': 'ℹ️',
                'success': '✅',
                'error': '❌',
                'warning': '⚠️'
            }[log.type] || 'ℹ️';
            
            return `
                <div class="log-entry log-${log.type}">
                    <span class="log-time">${log.timestamp}</span>
                    <span class="log-icon">${icon}</span>
                    <span class="log-message">${log.message}</span>
                </div>
            `;
        }).join('');
        
        logPanel.innerHTML = logHtml;
        logPanel.scrollTop = logPanel.scrollHeight;
    }
    
    showExecutionPanel() {
        let panel = document.getElementById('execution-panel');
        if (!panel) {
            panel = document.createElement('div');
            panel.id = 'execution-panel';
            panel.className = 'execution-panel';
            panel.innerHTML = `
                <div class="execution-panel-header">
                    <h3>Execution Log</h3>
                    <div class="execution-controls">
                        <button onclick="workflowExecutor.clearLog()" class="btn-clear">Clear</button>
                        <button onclick="workflowExecutor.hideExecutionPanel()" class="btn-close">✕</button>
                    </div>
                </div>
                <div id="execution-log-content" class="execution-log-content"></div>
            `;
            document.body.appendChild(panel);
        }
        panel.style.display = 'block';
    }
    
    hideExecutionPanel() {
        const panel = document.getElementById('execution-panel');
        if (panel) panel.style.display = 'none';
    }
    
    clearLog() {
        this.executionLog = [];
        this.renderLog();
    }
    
    getCurrentWorkflowData() {
        // Get workflow from canvas
        if (typeof workflowCanvas !== 'undefined' && workflowCanvas.workflow) {
            return workflowCanvas.workflow;
        }
        return null;
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    // Debug mode
    toggleDebugMode() {
        this.debugMode = !this.debugMode;
        const btn = document.getElementById('debug-mode-btn');
        if (btn) {
            btn.textContent = this.debugMode ? '🐛 Debug: ON' : '🐛 Debug: OFF';
            btn.classList.toggle('active', this.debugMode);
        }
        
        if (this.debugMode) {
            this.showTestDataInput();
        } else {
            this.hideTestDataInput();
        }
    }
    
    showTestDataInput() {
        let modal = document.getElementById('test-data-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'test-data-modal';
            modal.className = 'test-data-modal';
            modal.innerHTML = `
                <div class="test-data-content">
                    <h3>Debug Mode - Test Data</h3>
                    <p>Enter test data to simulate workflow execution:</p>
                    <textarea id="test-data-input" placeholder='{"field": "value", "status": "High", "content": "Test content..."}'></textarea>
                    <div class="test-data-actions">
                        <button onclick="workflowExecutor.runWithTestData()" class="btn-primary">Run with Test Data</button>
                        <button onclick="workflowExecutor.hideTestDataInput()" class="btn-secondary">Cancel</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }
        modal.style.display = 'flex';
    }
    
    hideTestDataInput() {
        const modal = document.getElementById('test-data-modal');
        if (modal) modal.style.display = 'none';
    }
    
    runWithTestData() {
        const input = document.getElementById('test-data-input');
        if (!input) return;
        
        try {
            const testData = JSON.parse(input.value || '{}');
            this.hideTestDataInput();
            this.executeWorkflow(null, testData);
        } catch (error) {
            alert('Invalid JSON format. Please check your test data.');
        }
    }
}

// Global instance
const workflowExecutor = new WorkflowExecutor();
window.workflowExecutor = workflowExecutor;
