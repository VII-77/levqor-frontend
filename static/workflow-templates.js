/**
 * Visual Workflow Builder - Phase 54: Template Library
 * Pre-built workflow templates users can clone
 */

class WorkflowTemplates {
    constructor() {
        this.templates = this.initTemplates();
    }
    
    initTemplates() {
        return [
            {
                id: 'notion-ai-summary',
                name: 'Notion AI Summarizer',
                description: 'Automatically summarize new Notion pages using AI',
                category: 'AI Automation',
                icon: '📊',
                difficulty: 'Easy',
                estimatedTime: '2 mins',
                useCase: 'Perfect for automating content summaries',
                nodes: [
                    {
                        id: 'node-trigger-1',
                        type: 'trigger',
                        position: { x: 100, y: 200 },
                        data: {
                            label: 'New Notion Page',
                            icon: '🎯',
                            color: '#667eea',
                            inputs: 0,
                            outputs: 1
                        },
                        config: {
                            trigger_type: 'notion',
                            source: 'YOUR_DATABASE_ID',
                            filter: 'Status = "To Process"'
                        }
                    },
                    {
                        id: 'node-ai-1',
                        type: 'ai_task',
                        position: { x: 350, y: 200 },
                        data: {
                            label: 'AI Summarizer',
                            icon: '🤖',
                            color: '#10b981',
                            inputs: 1,
                            outputs: 1
                        },
                        config: {
                            model: 'gpt-4o-mini',
                            system_prompt: 'Summarize the following content in 3-5 bullet points. Be concise and highlight key insights.',
                            temperature: '0.3',
                            max_tokens: '500'
                        }
                    },
                    {
                        id: 'node-action-1',
                        type: 'action',
                        position: { x: 600, y: 200 },
                        data: {
                            label: 'Update Notion',
                            icon: '⚡',
                            color: '#3b82f6',
                            inputs: 1,
                            outputs: 1
                        },
                        config: {
                            action_type: 'notion_update',
                            target: 'SAME_PAGE',
                            data: '{"summary": "{{ai_output}}", "status": "Processed"}'
                        }
                    }
                ],
                edges: [
                    { id: 'edge-1', source: 'node-trigger-1', target: 'node-ai-1' },
                    { id: 'edge-2', source: 'node-ai-1', target: 'node-action-1' }
                ]
            },
            {
                id: 'email-notification',
                name: 'Smart Email Alerts',
                description: 'Send intelligent email notifications based on conditions',
                category: 'Notifications',
                icon: '📧',
                difficulty: 'Easy',
                estimatedTime: '3 mins',
                useCase: 'Keep stakeholders informed automatically',
                nodes: [
                    {
                        id: 'node-trigger-2',
                        type: 'trigger',
                        position: { x: 100, y: 200 },
                        data: {
                            label: 'Notion Update',
                            icon: '🎯',
                            color: '#667eea',
                            inputs: 0,
                            outputs: 1
                        },
                        config: {
                            trigger_type: 'notion',
                            source: 'YOUR_DATABASE_ID'
                        }
                    },
                    {
                        id: 'node-condition-1',
                        type: 'condition',
                        position: { x: 350, y: 200 },
                        data: {
                            label: 'Check Priority',
                            icon: '❓',
                            color: '#f59e0b',
                            inputs: 1,
                            outputs: 2
                        },
                        config: {
                            field: 'priority',
                            operator: 'equals',
                            value: 'High'
                        }
                    },
                    {
                        id: 'node-notify-1',
                        type: 'notification',
                        position: { x: 600, y: 150 },
                        data: {
                            label: 'High Priority Alert',
                            icon: '📧',
                            color: '#8b5cf6',
                            inputs: 1,
                            outputs: 0
                        },
                        config: {
                            channel: 'email',
                            recipient: 'team@example.com',
                            message: '🚨 High Priority: {{title}}\n\nDetails: {{description}}',
                            priority: 'high'
                        }
                    }
                ],
                edges: [
                    { id: 'edge-1', source: 'node-trigger-2', target: 'node-condition-1' },
                    { id: 'edge-2', source: 'node-condition-1', target: 'node-notify-1' }
                ]
            },
            {
                id: 'ai-content-generator',
                name: 'AI Content Generator',
                description: 'Generate content with AI and save to Notion',
                category: 'AI Automation',
                icon: '✍️',
                difficulty: 'Medium',
                estimatedTime: '5 mins',
                useCase: 'Automate content creation workflows',
                nodes: [
                    {
                        id: 'node-trigger-3',
                        type: 'trigger',
                        position: { x: 100, y: 200 },
                        data: {
                            label: 'Manual Trigger',
                            icon: '🎯',
                            color: '#667eea',
                            inputs: 0,
                            outputs: 1
                        },
                        config: {
                            trigger_type: 'manual',
                            source: 'Manual'
                        }
                    },
                    {
                        id: 'node-ai-2',
                        type: 'ai_task',
                        position: { x: 350, y: 200 },
                        data: {
                            label: 'Generate Content',
                            icon: '🤖',
                            color: '#10b981',
                            inputs: 1,
                            outputs: 1
                        },
                        config: {
                            model: 'gpt-4o',
                            system_prompt: 'You are a professional content writer. Generate engaging, SEO-optimized content based on the topic provided.',
                            temperature: '0.7',
                            max_tokens: '2000'
                        }
                    },
                    {
                        id: 'node-action-2',
                        type: 'action',
                        position: { x: 600, y: 200 },
                        data: {
                            label: 'Save to Notion',
                            icon: '⚡',
                            color: '#3b82f6',
                            inputs: 1,
                            outputs: 1
                        },
                        config: {
                            action_type: 'notion_update',
                            target: 'YOUR_DATABASE_ID',
                            data: '{"content": "{{ai_output}}", "status": "Draft"}'
                        }
                    },
                    {
                        id: 'node-notify-2',
                        type: 'notification',
                        position: { x: 850, y: 200 },
                        data: {
                            label: 'Notify Complete',
                            icon: '📧',
                            color: '#8b5cf6',
                            inputs: 1,
                            outputs: 0
                        },
                        config: {
                            channel: 'email',
                            recipient: 'you@example.com',
                            message: '✅ Content generated and saved!',
                            priority: 'normal'
                        }
                    }
                ],
                edges: [
                    { id: 'edge-1', source: 'node-trigger-3', target: 'node-ai-2' },
                    { id: 'edge-2', source: 'node-ai-2', target: 'node-action-2' },
                    { id: 'edge-3', source: 'node-action-2', target: 'node-notify-2' }
                ]
            },
            {
                id: 'data-sync',
                name: 'Database Sync',
                description: 'Synchronize data between Notion databases',
                category: 'Data Management',
                icon: '🔄',
                difficulty: 'Medium',
                estimatedTime: '4 mins',
                useCase: 'Keep multiple databases in sync',
                nodes: [
                    {
                        id: 'node-trigger-4',
                        type: 'trigger',
                        position: { x: 100, y: 200 },
                        data: {
                            label: 'Source DB Update',
                            icon: '🎯',
                            color: '#667eea',
                            inputs: 0,
                            outputs: 1
                        },
                        config: {
                            trigger_type: 'notion',
                            source: 'SOURCE_DB_ID'
                        }
                    },
                    {
                        id: 'node-delay-1',
                        type: 'delay',
                        position: { x: 350, y: 200 },
                        data: {
                            label: 'Wait 5 Seconds',
                            icon: '⏱️',
                            color: '#ef4444',
                            inputs: 1,
                            outputs: 1
                        },
                        config: {
                            duration: '5',
                            unit: 'seconds'
                        }
                    },
                    {
                        id: 'node-action-3',
                        type: 'action',
                        position: { x: 600, y: 200 },
                        data: {
                            label: 'Update Target DB',
                            icon: '⚡',
                            color: '#3b82f6',
                            inputs: 1,
                            outputs: 1
                        },
                        config: {
                            action_type: 'notion_update',
                            target: 'TARGET_DB_ID',
                            data: '{"synced_from": "{{source_id}}", "last_sync": "{{timestamp}}"}'
                        }
                    }
                ],
                edges: [
                    { id: 'edge-1', source: 'node-trigger-4', target: 'node-delay-1' },
                    { id: 'edge-2', source: 'node-delay-1', target: 'node-action-3' }
                ]
            },
            {
                id: 'quality-check',
                name: 'AI Quality Checker',
                description: 'Use AI to validate and score content quality',
                category: 'Quality Assurance',
                icon: '✅',
                difficulty: 'Advanced',
                estimatedTime: '6 mins',
                useCase: 'Ensure content meets quality standards',
                nodes: [
                    {
                        id: 'node-trigger-5',
                        type: 'trigger',
                        position: { x: 100, y: 200 },
                        data: {
                            label: 'New Content',
                            icon: '🎯',
                            color: '#667eea',
                            inputs: 0,
                            outputs: 1
                        },
                        config: {
                            trigger_type: 'notion',
                            source: 'CONTENT_DB_ID',
                            filter: 'Status = "Ready for Review"'
                        }
                    },
                    {
                        id: 'node-ai-3',
                        type: 'ai_task',
                        position: { x: 350, y: 200 },
                        data: {
                            label: 'Quality Analysis',
                            icon: '🤖',
                            color: '#10b981',
                            inputs: 1,
                            outputs: 1
                        },
                        config: {
                            model: 'gpt-4o',
                            system_prompt: 'Analyze content quality on a scale of 0-100. Evaluate: clarity, accuracy, completeness, tone. Return JSON: {"score": X, "feedback": "..."}',
                            temperature: '0.2',
                            max_tokens: '500'
                        }
                    },
                    {
                        id: 'node-condition-2',
                        type: 'condition',
                        position: { x: 600, y: 200 },
                        data: {
                            label: 'Quality Check',
                            icon: '❓',
                            color: '#f59e0b',
                            inputs: 1,
                            outputs: 2
                        },
                        config: {
                            field: 'score',
                            operator: 'greater_than',
                            value: '80'
                        }
                    },
                    {
                        id: 'node-action-4',
                        type: 'action',
                        position: { x: 850, y: 150 },
                        data: {
                            label: 'Approve',
                            icon: '⚡',
                            color: '#10b981',
                            inputs: 1,
                            outputs: 0
                        },
                        config: {
                            action_type: 'notion_update',
                            target: 'SAME_PAGE',
                            data: '{"status": "Approved", "quality_score": "{{score}}"}'
                        }
                    },
                    {
                        id: 'node-action-5',
                        type: 'action',
                        position: { x: 850, y: 250 },
                        data: {
                            label: 'Request Revision',
                            icon: '⚡',
                            color: '#ef4444',
                            inputs: 1,
                            outputs: 0
                        },
                        config: {
                            action_type: 'notion_update',
                            target: 'SAME_PAGE',
                            data: '{"status": "Needs Revision", "feedback": "{{feedback}}"}'
                        }
                    }
                ],
                edges: [
                    { id: 'edge-1', source: 'node-trigger-5', target: 'node-ai-3' },
                    { id: 'edge-2', source: 'node-ai-3', target: 'node-condition-2' },
                    { id: 'edge-3', source: 'node-condition-2', target: 'node-action-4' },
                    { id: 'edge-4', source: 'node-condition-2', target: 'node-action-5' }
                ]
            }
        ];
    }
    
    renderTemplateLibrary() {
        const categories = [...new Set(this.templates.map(t => t.category))];
        
        let html = `
            <div class="template-library">
                <div class="template-header">
                    <h2>Workflow Templates</h2>
                    <p>Start with a pre-built workflow and customize it to your needs</p>
                </div>
        `;
        
        categories.forEach(category => {
            const categoryTemplates = this.templates.filter(t => t.category === category);
            
            html += `
                <div class="template-category">
                    <h3 class="category-title">${category}</h3>
                    <div class="template-grid">
            `;
            
            categoryTemplates.forEach(template => {
                html += this.renderTemplateCard(template);
            });
            
            html += `
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        return html;
    }
    
    renderTemplateCard(template) {
        const difficultyColors = {
            'Easy': '#10b981',
            'Medium': '#f59e0b',
            'Advanced': '#ef4444'
        };
        
        return `
            <div class="template-card" onclick="workflowTemplates.useTemplate('${template.id}')">
                <div class="template-icon">${template.icon}</div>
                <div class="template-info">
                    <div class="template-name">${template.name}</div>
                    <div class="template-description">${template.description}</div>
                    <div class="template-meta">
                        <span class="template-badge" style="background: ${difficultyColors[template.difficulty]}20; color: ${difficultyColors[template.difficulty]};">
                            ${template.difficulty}
                        </span>
                        <span class="template-time">⏱️ ${template.estimatedTime}</span>
                    </div>
                    <div class="template-use-case">${template.useCase}</div>
                </div>
            </div>
        `;
    }
    
    async useTemplate(templateId) {
        const template = this.templates.find(t => t.id === templateId);
        if (!template) return;
        
        // Create new workflow from template
        try {
            const response = await fetch('/api/workflow', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Dash-Key': localStorage.getItem('dashKey') || 'temp'
                },
                body: JSON.stringify({
                    user_id: 'default',
                    name: template.name,
                    description: template.description,
                    nodes: template.nodes,
                    edges: template.edges
                })
            });
            
            const data = await response.json();
            if (data.ok) {
                // Redirect to builder with new workflow
                window.location.href = `/workflow/builder?id=${data.workflow_id}`;
            }
        } catch (error) {
            console.error('Failed to create workflow from template:', error);
            alert('Failed to create workflow. Please try again.');
        }
    }
}

// Global instance
const workflowTemplates = new WorkflowTemplates();
window.workflowTemplates = workflowTemplates;

// Show template library
function showTemplates() {
    const modal = document.createElement('div');
    modal.className = 'template-modal';
    modal.innerHTML = `
        <div class="template-modal-content">
            <div class="template-modal-header">
                <button class="template-close" onclick="this.closest('.template-modal').remove()">✕</button>
            </div>
            ${workflowTemplates.renderTemplateLibrary()}
        </div>
    `;
    document.body.appendChild(modal);
}
