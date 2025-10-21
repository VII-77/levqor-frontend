/**
 * Visual Workflow Builder - Phase 52: Interactive Canvas
 * Drag-and-drop nodes, draw connections, mobile touch support
 */

class WorkflowCanvas {
    constructor(canvasElement, viewportElement) {
        this.canvas = canvasElement;
        this.viewport = viewportElement;
        this.nodes = [];
        this.connections = [];
        this.selectedNode = null;
        this.selectedConnection = null;
        this.isDraggingNode = false;
        this.isDrawingConnection = false;
        this.draggedNode = null;
        this.connectionStart = null;
        this.tempConnection = null;
        this.zoom = 1;
        this.panOffset = { x: 0, y: 0 };
        
        this.init();
    }
    
    init() {
        // Create SVG layer for connections
        this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        this.svg.id = 'connections-svg';
        this.svg.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1';
        this.viewport.insertBefore(this.svg, this.viewport.firstChild);
        
        // Canvas drop event
        this.canvas.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
        });
        
        this.canvas.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Canvas click (deselect)
        this.canvas.addEventListener('click', (e) => {
            if (e.target === this.canvas || e.target === this.viewport) {
                this.deselectAll();
            }
        });
        
        // Mobile touch support
        this.setupTouchHandlers();
    }
    
    handleDrop(e) {
        e.preventDefault();
        const nodeType = e.dataTransfer.getData('nodeType');
        if (!nodeType) return;
        
        // Get drop position relative to viewport
        const rect = this.viewport.getBoundingClientRect();
        const x = e.clientX - rect.left + this.canvas.scrollLeft;
        const y = e.clientY - rect.top + this.canvas.scrollTop;
        
        this.addNode(nodeType, x, y);
    }
    
    addNode(type, x, y) {
        const nodeConfig = window.nodeTypes?.find(n => n.type === type);
        if (!nodeConfig) return;
        
        const node = {
            id: `node-${Date.now()}`,
            type: type,
            position: { x, y },
            data: {
                label: nodeConfig.name,
                icon: nodeConfig.icon,
                color: nodeConfig.color,
                inputs: nodeConfig.inputs,
                outputs: nodeConfig.outputs
            }
        };
        
        this.nodes.push(node);
        this.renderNode(node);
        this.saveWorkflow();
        
        // Show empty state if first node
        if (this.nodes.length === 1) {
            const emptyState = document.getElementById('emptyState');
            if (emptyState) emptyState.style.display = 'none';
        }
    }
    
    renderNode(node) {
        const nodeEl = document.createElement('div');
        nodeEl.className = 'workflow-node';
        nodeEl.id = node.id;
        nodeEl.style.left = `${node.position.x}px`;
        nodeEl.style.top = `${node.position.y}px`;
        nodeEl.draggable = false; // Use mouse events for dragging
        
        nodeEl.innerHTML = `
            <div class="node-header">
                <div class="node-type-icon" style="background: ${node.data.color}20; color: ${node.data.color};">
                    ${node.data.icon}
                </div>
                <div class="node-label">${node.data.label}</div>
                <div class="node-delete" onclick="workflowCanvas.deleteNode('${node.id}')">✕</div>
            </div>
            <div class="node-body">${node.type}</div>
            ${node.data.inputs > 0 ? '<div class="node-port input"></div>' : ''}
            ${node.data.outputs > 0 ? '<div class="node-port output"></div>' : ''}
        `;
        
        this.viewport.appendChild(nodeEl);
        
        // Click to select
        nodeEl.addEventListener('click', (e) => {
            e.stopPropagation();
            this.selectNode(node.id);
        });
        
        // Drag to move
        nodeEl.addEventListener('mousedown', (e) => this.startNodeDrag(e, node.id));
        nodeEl.addEventListener('touchstart', (e) => this.startNodeDrag(e, node.id), { passive: false });
        
        // Connection ports
        const outputPort = nodeEl.querySelector('.node-port.output');
        if (outputPort) {
            outputPort.addEventListener('mousedown', (e) => this.startConnection(e, node.id));
            outputPort.addEventListener('touchstart', (e) => this.startConnection(e, node.id), { passive: false });
        }
        
        const inputPort = nodeEl.querySelector('.node-port.input');
        if (inputPort) {
            inputPort.addEventListener('mouseup', (e) => this.endConnection(e, node.id));
            inputPort.addEventListener('touchend', (e) => this.endConnection(e, node.id));
        }
    }
    
    startNodeDrag(e, nodeId) {
        if (e.target.classList.contains('node-port')) return;
        if (e.target.classList.contains('node-delete')) return;
        
        e.preventDefault();
        e.stopPropagation();
        
        this.isDraggingNode = true;
        this.draggedNode = nodeId;
        
        const node = this.nodes.find(n => n.id === nodeId);
        const nodeEl = document.getElementById(nodeId);
        const clientX = e.clientX || e.touches[0].clientX;
        const clientY = e.clientY || e.touches[0].clientY;
        const rect = nodeEl.getBoundingClientRect();
        
        this.dragOffset = {
            x: clientX - rect.left,
            y: clientY - rect.top
        };
        
        nodeEl.classList.add('dragging');
        
        const moveHandler = (e2) => this.handleNodeDrag(e2);
        const upHandler = (e2) => {
            this.isDraggingNode = false;
            this.draggedNode = null;
            nodeEl.classList.remove('dragging');
            document.removeEventListener('mousemove', moveHandler);
            document.removeEventListener('touchmove', moveHandler);
            document.removeEventListener('mouseup', upHandler);
            document.removeEventListener('touchend', upHandler);
            this.saveWorkflow();
        };
        
        document.addEventListener('mousemove', moveHandler);
        document.addEventListener('touchmove', moveHandler, { passive: false });
        document.addEventListener('mouseup', upHandler);
        document.addEventListener('touchend', upHandler);
    }
    
    handleNodeDrag(e) {
        if (!this.isDraggingNode || !this.draggedNode) return;
        
        e.preventDefault();
        const clientX = e.clientX || e.touches[0].clientX;
        const clientY = e.clientY || e.touches[0].clientY;
        const rect = this.viewport.getBoundingClientRect();
        
        const x = clientX - rect.left + this.canvas.scrollLeft - this.dragOffset.x;
        const y = clientY - rect.top + this.canvas.scrollTop - this.dragOffset.y;
        
        const node = this.nodes.find(n => n.id === this.draggedNode);
        node.position = { x, y };
        
        const nodeEl = document.getElementById(this.draggedNode);
        nodeEl.style.left = `${x}px`;
        nodeEl.style.top = `${y}px`;
        
        this.updateConnections();
    }
    
    startConnection(e, nodeId) {
        e.preventDefault();
        e.stopPropagation();
        
        this.isDrawingConnection = true;
        this.connectionStart = nodeId;
        
        const port = e.target;
        port.classList.add('active');
        
        // Create temporary connection line
        this.tempConnection = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        this.tempConnection.classList.add('temp-connection');
        this.svg.appendChild(this.tempConnection);
        
        const moveHandler = (e2) => {
            const clientX = e2.clientX || e2.touches[0].clientX;
            const clientY = e2.clientY || e2.touches[0].clientY;
            const rect = this.viewport.getBoundingClientRect();
            
            const startNode = this.nodes.find(n => n.id === nodeId);
            const startEl = document.getElementById(nodeId);
            const startPort = startEl.querySelector('.node-port.output');
            const startRect = startPort.getBoundingClientRect();
            
            const x1 = startRect.left + startRect.width / 2 - rect.left + this.canvas.scrollLeft;
            const y1 = startRect.top + startRect.height / 2 - rect.top + this.canvas.scrollTop;
            const x2 = clientX - rect.left + this.canvas.scrollLeft;
            const y2 = clientY - rect.top + this.canvas.scrollTop;
            
            const path = this.createBezierPath(x1, y1, x2, y2);
            this.tempConnection.setAttribute('d', path);
        };
        
        const upHandler = (e2) => {
            port.classList.remove('active');
            if (this.tempConnection) {
                this.tempConnection.remove();
                this.tempConnection = null;
            }
            this.isDrawingConnection = false;
            this.connectionStart = null;
            document.removeEventListener('mousemove', moveHandler);
            document.removeEventListener('touchmove', moveHandler);
            document.removeEventListener('mouseup', upHandler);
            document.removeEventListener('touchend', upHandler);
        };
        
        document.addEventListener('mousemove', moveHandler);
        document.addEventListener('touchmove', moveHandler, { passive: false });
        document.addEventListener('mouseup', upHandler);
        document.addEventListener('touchend', upHandler);
    }
    
    endConnection(e, nodeId) {
        if (!this.isDrawingConnection || !this.connectionStart) return;
        if (this.connectionStart === nodeId) return; // Can't connect to self
        
        e.preventDefault();
        e.stopPropagation();
        
        const connection = {
            id: `conn-${Date.now()}`,
            source: this.connectionStart,
            target: nodeId
        };
        
        this.connections.push(connection);
        this.renderConnection(connection);
        this.saveWorkflow();
    }
    
    renderConnection(connection) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.classList.add('connection-path');
        path.id = connection.id;
        path.setAttribute('data-source', connection.source);
        path.setAttribute('data-target', connection.target);
        
        path.addEventListener('click', (e) => {
            e.stopPropagation();
            this.selectConnection(connection.id);
        });
        
        this.svg.appendChild(path);
        this.updateConnection(connection.id);
    }
    
    updateConnection(connId) {
        const connection = this.connections.find(c => c.id === connId);
        if (!connection) return;
        
        const sourceNode = document.getElementById(connection.source);
        const targetNode = document.getElementById(connection.target);
        if (!sourceNode || !targetNode) return;
        
        const sourcePort = sourceNode.querySelector('.node-port.output');
        const targetPort = targetNode.querySelector('.node-port.input');
        if (!sourcePort || !targetPort) return;
        
        const rect = this.viewport.getBoundingClientRect();
        const sourceRect = sourcePort.getBoundingClientRect();
        const targetRect = targetPort.getBoundingClientRect();
        
        const x1 = sourceRect.left + sourceRect.width / 2 - rect.left + this.canvas.scrollLeft;
        const y1 = sourceRect.top + sourceRect.height / 2 - rect.top + this.canvas.scrollTop;
        const x2 = targetRect.left + targetRect.width / 2 - rect.left + this.canvas.scrollLeft;
        const y2 = targetRect.top + targetRect.height / 2 - rect.top + this.canvas.scrollTop;
        
        const path = this.createBezierPath(x1, y1, x2, y2);
        const pathEl = document.getElementById(connId);
        if (pathEl) pathEl.setAttribute('d', path);
    }
    
    updateConnections() {
        this.connections.forEach(conn => this.updateConnection(conn.id));
    }
    
    createBezierPath(x1, y1, x2, y2) {
        const dx = Math.abs(x2 - x1);
        const offsetX = Math.min(dx / 2, 100);
        
        return `M ${x1} ${y1} C ${x1 + offsetX} ${y1}, ${x2 - offsetX} ${y2}, ${x2} ${y2}`;
    }
    
    selectNode(nodeId) {
        this.deselectAll();
        this.selectedNode = nodeId;
        document.getElementById(nodeId)?.classList.add('selected');
        this.showNodeProperties(nodeId);
    }
    
    selectConnection(connId) {
        this.deselectAll();
        this.selectedConnection = connId;
        document.getElementById(connId)?.classList.add('selected');
    }
    
    deselectAll() {
        document.querySelectorAll('.workflow-node.selected').forEach(el => el.classList.remove('selected'));
        document.querySelectorAll('.connection-path.selected').forEach(el => el.classList.remove('selected'));
        this.selectedNode = null;
        this.selectedConnection = null;
    }
    
    deleteNode(nodeId) {
        // Remove connections
        this.connections = this.connections.filter(conn => {
            if (conn.source === nodeId || conn.target === nodeId) {
                document.getElementById(conn.id)?.remove();
                return false;
            }
            return true;
        });
        
        // Remove node
        this.nodes = this.nodes.filter(n => n.id !== nodeId);
        document.getElementById(nodeId)?.remove();
        
        this.saveWorkflow();
        
        // Show empty state if no nodes
        if (this.nodes.length === 0) {
            const emptyState = document.getElementById('emptyState');
            if (emptyState) emptyState.style.display = 'block';
        }
    }
    
    deleteConnection(connId) {
        this.connections = this.connections.filter(c => c.id !== connId);
        document.getElementById(connId)?.remove();
        this.saveWorkflow();
    }
    
    showNodeProperties(nodeId) {
        const node = this.nodes.find(n => n.id === nodeId);
        if (!node) return;
        
        const panel = document.getElementById('propertiesContent');
        panel.innerHTML = `
            <div class="property-group">
                <div class="property-label">Node Type</div>
                <div style="color: var(--text-primary);">${node.data.label}</div>
            </div>
            <div class="property-group">
                <div class="property-label">Label</div>
                <input type="text" class="property-input" value="${node.data.label}" 
                       onchange="workflowCanvas.updateNodeLabel('${nodeId}', this.value)">
            </div>
            <div class="property-group">
                <button class="btn btn-secondary" style="width: 100%;" 
                        onclick="workflowCanvas.deleteNode('${nodeId}')">
                    Delete Node
                </button>
            </div>
        `;
    }
    
    updateNodeLabel(nodeId, label) {
        const node = this.nodes.find(n => n.id === nodeId);
        if (node) {
            node.data.label = label;
            const labelEl = document.querySelector(`#${nodeId} .node-label`);
            if (labelEl) labelEl.textContent = label;
            this.saveWorkflow();
        }
    }
    
    setupTouchHandlers() {
        // Prevent default touch behaviors on canvas
        this.canvas.addEventListener('touchmove', (e) => {
            if (this.isDraggingNode || this.isDrawingConnection) {
                e.preventDefault();
            }
        }, { passive: false });
    }
    
    zoom In() {
        this.zoom = Math.min(this.zoom + 0.25, 2);
        this.applyZoom();
    }
    
    zoomOut() {
        this.zoom = Math.max(this.zoom - 0.25, 0.5);
        this.applyZoom();
    }
    
    resetZoom() {
        this.zoom = 1;
        this.applyZoom();
    }
    
    applyZoom() {
        this.viewport.style.transform = `scale(${this.zoom})`;
        this.viewport.style.transformOrigin = '0 0';
    }
    
    async saveWorkflow() {
        if (!window.currentWorkflow) return;
        
        const edges = this.connections.map(conn => ({
            id: conn.id,
            source: conn.source,
            target: conn.target
        }));
        
        try {
            const response = await fetch(`/api/workflow/${window.currentWorkflow.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Dash-Key': localStorage.getItem('dashKey')
                },
                body: JSON.stringify({
                    nodes: this.nodes,
                    edges: edges
                })
            });
            
            const data = await response.json();
            if (data.ok) {
                console.log('Workflow saved');
            }
        } catch (error) {
            console.error('Failed to save workflow:', error);
        }
    }
    
    loadWorkflow(workflow) {
        // Clear existing
        this.nodes = [];
        this.connections = [];
        this.viewport.querySelectorAll('.workflow-node').forEach(el => el.remove());
        this.svg.querySelectorAll('.connection-path').forEach(el => el.remove());
        
        // Load nodes
        if (workflow.nodes && workflow.nodes.length > 0) {
            workflow.nodes.forEach(node => {
                this.nodes.push(node);
                this.renderNode(node);
            });
            document.getElementById('emptyState').style.display = 'none';
        }
        
        // Load connections
        if (workflow.edges && workflow.edges.length > 0) {
            workflow.edges.forEach(edge => {
                const connection = {
                    id: edge.id || `conn-${Date.now()}-${Math.random()}`,
                    source: edge.source,
                    target: edge.target
                };
                this.connections.push(connection);
                this.renderConnection(connection);
            });
        }
    }
}

// Initialize canvas when page loads
let workflowCanvas;
window.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    const viewport = document.getElementById('viewport');
    if (canvas && viewport) {
        workflowCanvas = new WorkflowCanvas(canvas, viewport);
        window.workflowCanvas = workflowCanvas;
    }
});
