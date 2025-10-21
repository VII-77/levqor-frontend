/**
 * Visual Workflow Builder - Phase 53: Node Configuration
 * Dynamic configuration panels for each node type
 */

class NodeConfigurator {
    constructor() {
        this.configSchemas = this.initSchemas();
        this.validationRules = this.initValidationRules();
    }
    
    initSchemas() {
        return {
            trigger: {
                title: 'Trigger Configuration',
                fields: [
                    {
                        name: 'trigger_type',
                        label: 'Trigger Type',
                        type: 'select',
                        required: true,
                        options: [
                            { value: 'notion', label: '📊 Notion Database' },
                            { value: 'webhook', label: '🔗 Webhook' },
                            { value: 'schedule', label: '⏰ Schedule' },
                            { value: 'manual', label: '👆 Manual' }
                        ]
                    },
                    {
                        name: 'source',
                        label: 'Source',
                        type: 'text',
                        required: true,
                        placeholder: 'Database ID or webhook URL'
                    },
                    {
                        name: 'filter',
                        label: 'Filter Condition',
                        type: 'textarea',
                        placeholder: 'Optional: Filter expression'
                    }
                ]
            },
            ai_task: {
                title: 'AI Task Configuration',
                fields: [
                    {
                        name: 'model',
                        label: 'AI Model',
                        type: 'select',
                        required: true,
                        options: [
                            { value: 'gpt-4o', label: '🧠 GPT-4o (Best Quality)' },
                            { value: 'gpt-4o-mini', label: '⚡ GPT-4o-mini (Fast)' },
                            { value: 'claude-3-5-sonnet', label: '🎭 Claude 3.5 Sonnet' }
                        ]
                    },
                    {
                        name: 'system_prompt',
                        label: 'System Prompt',
                        type: 'textarea',
                        required: true,
                        placeholder: 'Instructions for the AI...',
                        rows: 4
                    },
                    {
                        name: 'temperature',
                        label: 'Temperature',
                        type: 'range',
                        min: 0,
                        max: 2,
                        step: 0.1,
                        default: 0.7
                    },
                    {
                        name: 'max_tokens',
                        label: 'Max Tokens',
                        type: 'number',
                        min: 1,
                        max: 4096,
                        default: 2000
                    }
                ]
            },
            condition: {
                title: 'Condition Configuration',
                fields: [
                    {
                        name: 'field',
                        label: 'Field to Check',
                        type: 'text',
                        required: true,
                        placeholder: 'e.g., status, priority'
                    },
                    {
                        name: 'operator',
                        label: 'Operator',
                        type: 'select',
                        required: true,
                        options: [
                            { value: 'equals', label: '= Equals' },
                            { value: 'not_equals', label: '≠ Not Equals' },
                            { value: 'contains', label: '⊃ Contains' },
                            { value: 'greater_than', label: '> Greater Than' },
                            { value: 'less_than', label: '< Less Than' },
                            { value: 'is_empty', label: '∅ Is Empty' }
                        ]
                    },
                    {
                        name: 'value',
                        label: 'Value',
                        type: 'text',
                        placeholder: 'Comparison value'
                    }
                ]
            },
            action: {
                title: 'Action Configuration',
                fields: [
                    {
                        name: 'action_type',
                        label: 'Action Type',
                        type: 'select',
                        required: true,
                        options: [
                            { value: 'notion_update', label: '📝 Update Notion' },
                            { value: 'send_email', label: '📧 Send Email' },
                            { value: 'api_call', label: '🔌 API Call' },
                            { value: 'webhook', label: '🔗 Webhook' }
                        ]
                    },
                    {
                        name: 'target',
                        label: 'Target',
                        type: 'text',
                        required: true,
                        placeholder: 'Database ID, email, or URL'
                    },
                    {
                        name: 'data',
                        label: 'Data/Payload',
                        type: 'textarea',
                        placeholder: 'JSON data to send',
                        rows: 4
                    }
                ]
            },
            notification: {
                title: 'Notification Configuration',
                fields: [
                    {
                        name: 'channel',
                        label: 'Channel',
                        type: 'select',
                        required: true,
                        options: [
                            { value: 'email', label: '📧 Email' },
                            { value: 'telegram', label: '💬 Telegram' },
                            { value: 'webhook', label: '🔗 Webhook' }
                        ]
                    },
                    {
                        name: 'recipient',
                        label: 'Recipient',
                        type: 'text',
                        required: true,
                        placeholder: 'Email or chat ID'
                    },
                    {
                        name: 'message',
                        label: 'Message Template',
                        type: 'textarea',
                        required: true,
                        placeholder: 'Use {{field}} for dynamic values',
                        rows: 3
                    },
                    {
                        name: 'priority',
                        label: 'Priority',
                        type: 'select',
                        options: [
                            { value: 'low', label: 'Low' },
                            { value: 'normal', label: 'Normal' },
                            { value: 'high', label: 'High' }
                        ]
                    }
                ]
            },
            delay: {
                title: 'Delay Configuration',
                fields: [
                    {
                        name: 'duration',
                        label: 'Duration',
                        type: 'number',
                        required: true,
                        min: 1,
                        default: 5
                    },
                    {
                        name: 'unit',
                        label: 'Unit',
                        type: 'select',
                        required: true,
                        options: [
                            { value: 'seconds', label: 'Seconds' },
                            { value: 'minutes', label: 'Minutes' },
                            { value: 'hours', label: 'Hours' },
                            { value: 'days', label: 'Days' }
                        ]
                    }
                ]
            }
        };
    }
    
    initValidationRules() {
        return {
            trigger: {
                required: ['trigger_type', 'source'],
                formats: {
                    source: (value, config) => {
                        if (config.trigger_type === 'webhook') {
                            return /^https?:\/\/.+/.test(value) || 'Must be a valid URL';
                        }
                        return true;
                    }
                }
            },
            ai_task: {
                required: ['model', 'system_prompt'],
                ranges: {
                    temperature: [0, 2],
                    max_tokens: [1, 4096]
                }
            },
            condition: {
                required: ['field', 'operator']
            },
            action: {
                required: ['action_type', 'target'],
                formats: {
                    data: (value) => {
                        if (!value) return true;
                        try {
                            JSON.parse(value);
                            return true;
                        } catch {
                            return 'Must be valid JSON';
                        }
                    }
                }
            },
            notification: {
                required: ['channel', 'recipient', 'message'],
                formats: {
                    recipient: (value, config) => {
                        if (config.channel === 'email') {
                            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || 'Must be a valid email';
                        }
                        return true;
                    }
                }
            },
            delay: {
                required: ['duration', 'unit'],
                ranges: {
                    duration: [1, 999999]
                }
            }
        };
    }
    
    renderConfigPanel(node) {
        const schema = this.configSchemas[node.type];
        if (!schema) return '<p>No configuration available</p>';
        
        let html = `
            <div class="config-panel">
                <div class="config-title">${schema.title}</div>
                <form id="nodeConfigForm" onsubmit="return false;">
        `;
        
        schema.fields.forEach(field => {
            html += this.renderField(field, node.config || {});
        });
        
        html += `
                    <div class="config-actions">
                        <button type="button" class="btn btn-ghost" onclick="closeConfigPanel()">
                            Cancel
                        </button>
                        <button type="button" class="btn btn-primary" onclick="saveNodeConfig('${node.id}')">
                            Save Configuration
                        </button>
                    </div>
                </form>
            </div>
        `;
        
        return html;
    }
    
    renderField(field, config) {
        const value = config[field.name] || field.default || '';
        let fieldHtml = `
            <div class="config-field">
                <label class="config-label">
                    ${field.label}
                    ${field.required ? '<span class="required">*</span>' : ''}
                </label>
        `;
        
        switch (field.type) {
            case 'text':
                fieldHtml += `
                    <input type="text" 
                           name="${field.name}" 
                           class="config-input"
                           value="${this.escapeHtml(value)}"
                           placeholder="${field.placeholder || ''}"
                           ${field.required ? 'required' : ''}>
                `;
                break;
                
            case 'textarea':
                fieldHtml += `
                    <textarea name="${field.name}" 
                              class="config-input"
                              rows="${field.rows || 3}"
                              placeholder="${field.placeholder || ''}"
                              ${field.required ? 'required' : ''}>${this.escapeHtml(value)}</textarea>
                `;
                break;
                
            case 'number':
                fieldHtml += `
                    <input type="number" 
                           name="${field.name}" 
                           class="config-input"
                           value="${value}"
                           min="${field.min || ''}"
                           max="${field.max || ''}"
                           ${field.required ? 'required' : ''}>
                `;
                break;
                
            case 'range':
                fieldHtml += `
                    <div class="range-container">
                        <input type="range" 
                               name="${field.name}" 
                               class="config-range"
                               value="${value}"
                               min="${field.min}"
                               max="${field.max}"
                               step="${field.step || 1}"
                               oninput="updateRangeValue(this, '${field.name}-value')">
                        <span class="range-value" id="${field.name}-value">${value}</span>
                    </div>
                `;
                break;
                
            case 'select':
                fieldHtml += `
                    <select name="${field.name}" class="config-input" ${field.required ? 'required' : ''}>
                        <option value="">Select ${field.label}...</option>
                `;
                field.options.forEach(opt => {
                    fieldHtml += `
                        <option value="${opt.value}" ${value === opt.value ? 'selected' : ''}>
                            ${opt.label}
                        </option>
                    `;
                });
                fieldHtml += '</select>';
                break;
        }
        
        fieldHtml += '</div>';
        return fieldHtml;
    }
    
    validate(nodeType, config) {
        const rules = this.validationRules[nodeType];
        if (!rules) return { valid: true, errors: [], warnings: [] };
        
        const errors = [];
        const warnings = [];
        
        // Check required fields
        if (rules.required) {
            rules.required.forEach(field => {
                if (!config[field] || config[field].trim() === '') {
                    errors.push(`${field} is required`);
                }
            });
        }
        
        // Check ranges
        if (rules.ranges) {
            Object.keys(rules.ranges).forEach(field => {
                const [min, max] = rules.ranges[field];
                const value = parseFloat(config[field]);
                if (!isNaN(value) && (value < min || value > max)) {
                    errors.push(`${field} must be between ${min} and ${max}`);
                }
            });
        }
        
        // Check formats
        if (rules.formats) {
            Object.keys(rules.formats).forEach(field => {
                const validator = rules.formats[field];
                const result = validator(config[field], config);
                if (result !== true) {
                    errors.push(result);
                }
            });
        }
        
        return {
            valid: errors.length === 0,
            errors,
            warnings
        };
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global instance
const nodeConfigurator = new NodeConfigurator();
window.nodeConfigurator = nodeConfigurator;

// Helper functions for UI
function updateRangeValue(input, targetId) {
    document.getElementById(targetId).textContent = input.value;
}

function closeConfigPanel() {
    const panel = document.getElementById('propertiesContent');
    panel.innerHTML = '<p style="color: var(--text-secondary); font-size: var(--text-sm);">Select a node to view its properties</p>';
}

function saveNodeConfig(nodeId) {
    const form = document.getElementById('nodeConfigForm');
    const formData = new FormData(form);
    const config = {};
    
    for (const [key, value] of formData.entries()) {
        config[key] = value;
    }
    
    if (window.workflowCanvas) {
        window.workflowCanvas.updateNodeConfig(nodeId, config);
    }
    
    alert('Configuration saved!');
}
