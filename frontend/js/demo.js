// Demo Page Controller

// Input Validation Controller
class InputValidator {
    constructor() {
        this.textInput = document.getElementById('text-input');
        this.analyzeBtn = document.getElementById('analyze-btn');
        this.errorMessage = document.getElementById('input-error');
        
        this.init();
    }

    init() {
        if (!this.textInput || !this.analyzeBtn || !this.errorMessage) return;

        // Validate on input change
        this.textInput.addEventListener('input', () => this.validateInput());
        
        // Validate on blur
        this.textInput.addEventListener('blur', () => this.validateInput());
        
        // Initial validation to set button state
        this.validateInput();
    }

    validateInput() {
        const text = this.textInput.value.trim();
        
        if (text === '') {
            this.showError('Please enter text to analyze');
            this.disableAnalyzeButton();
            return false;
        } else {
            this.clearError();
            this.enableAnalyzeButton();
            return true;
        }
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.classList.add('show');
        this.textInput.classList.add('error');
        this.textInput.setAttribute('aria-invalid', 'true');
        this.textInput.setAttribute('aria-describedby', 'input-error');
    }

    clearError() {
        this.errorMessage.textContent = '';
        this.errorMessage.classList.remove('show');
        this.textInput.classList.remove('error');
        this.textInput.removeAttribute('aria-invalid');
        this.textInput.removeAttribute('aria-describedby');
    }

    disableAnalyzeButton() {
        this.analyzeBtn.disabled = true;
    }

    enableAnalyzeButton() {
        this.analyzeBtn.disabled = false;
    }
}

// Initialize input validator on demo page
document.addEventListener('DOMContentLoaded', () => {
    const validator = new InputValidator();
});

// Loading Animation Controller
class LoadingAnimationController {
    constructor() {
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.loadingMessage = document.getElementById('loading-message');
        this.messages = [
            'Analyzing text...',
            'Extracting causality...',
            'Computing bias metrics...'
        ];
        this.currentMessageIndex = 0;
        this.messageInterval = null;
    }

    show() {
        if (!this.loadingOverlay || !this.loadingMessage) return;
        
        // Reset to first message
        this.currentMessageIndex = 0;
        this.loadingMessage.textContent = this.messages[0];
        
        // Show overlay
        this.loadingOverlay.style.display = 'flex';
        
        // Start cycling through messages
        this.messageInterval = setInterval(() => {
            this.cycleMessage();
        }, 2000); // Change message every 2 seconds
    }

    cycleMessage() {
        // Fade out current message
        this.loadingMessage.style.opacity = '0';
        
        setTimeout(() => {
            // Move to next message
            this.currentMessageIndex = (this.currentMessageIndex + 1) % this.messages.length;
            this.loadingMessage.textContent = this.messages[this.currentMessageIndex];
            
            // Fade in new message
            this.loadingMessage.style.opacity = '1';
        }, 300); // Wait for fade out to complete
    }

    hide() {
        if (!this.loadingOverlay) return;
        
        // Clear interval
        if (this.messageInterval) {
            clearInterval(this.messageInterval);
            this.messageInterval = null;
        }
        
        // Hide overlay
        this.loadingOverlay.style.display = 'none';
        
        // Reset message
        this.currentMessageIndex = 0;
        if (this.loadingMessage) {
            this.loadingMessage.textContent = this.messages[0];
            this.loadingMessage.style.opacity = '1';
        }
    }
}

// Export for use in other modules
window.LoadingAnimationController = LoadingAnimationController;

// Hate Words Table Renderer
class HateWordsRenderer {
    constructor() {
        this.container = document.getElementById('hate-words-content');
    }

    render(hateWords) {
        if (!this.container) return;

        // Clear existing content
        this.container.innerHTML = '';

        // Check if there are hate words to display
        if (!hateWords || hateWords.length === 0) {
            this.renderEmptyState();
            return;
        }

        // Create table
        const table = document.createElement('table');
        table.className = 'hate-words-table';

        // Create table header
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Word</th>
                <th>Severity</th>
                <th>Context</th>
            </tr>
        `;
        table.appendChild(thead);

        // Create table body
        const tbody = document.createElement('tbody');
        
        hateWords.forEach(item => {
            const row = document.createElement('tr');
            
            // Word column
            const wordCell = document.createElement('td');
            wordCell.textContent = item.word;
            wordCell.setAttribute('data-label', 'Word:');
            row.appendChild(wordCell);

            // Severity column
            const severityCell = document.createElement('td');
            severityCell.setAttribute('data-label', 'Severity:');
            const severityBadge = document.createElement('span');
            severityBadge.className = `severity-badge ${item.severity.toLowerCase()}`;
            severityBadge.textContent = item.severity;
            severityCell.appendChild(severityBadge);
            row.appendChild(severityCell);

            // Context column
            const contextCell = document.createElement('td');
            contextCell.textContent = item.context;
            contextCell.setAttribute('data-label', 'Context:');
            row.appendChild(contextCell);

            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        this.container.appendChild(table);
    }

    renderEmptyState() {
        this.container.innerHTML = `
            <div class="empty-state">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                    </path>
                </svg>
                <p>No hate words detected</p>
            </div>
        `;
    }
}

// Export for use in other modules
window.HateWordsRenderer = HateWordsRenderer;

// Causal Graph Renderer
class CausalGraphRenderer {
    constructor() {
        this.container = document.getElementById('causal-graph-network');
        this.network = null;
    }

    render(graphData) {
        if (!this.container) return;

        // Check if there is graph data to display
        if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
            this.renderEmptyState();
            return;
        }

        // Clear existing content
        this.container.innerHTML = '';

        // Get current theme
        const theme = document.documentElement.getAttribute('data-theme') || 'light';
        const isDark = theme === 'dark';

        // Prepare nodes with vis.js format
        const nodes = graphData.nodes.map(node => ({
            id: node.id,
            label: node.label,
            shape: 'circle',
            size: node.size || 25,
            color: {
                background: node.color || (isDark ? '#6C63FF' : '#6C63FF'),
                border: isDark ? '#00C2A8' : '#1A2A44',
                highlight: {
                    background: '#00C2A8',
                    border: '#6C63FF'
                },
                hover: {
                    background: isDark ? '#8B83FF' : '#5A52E0',
                    border: isDark ? '#00D4B8' : '#152238'
                }
            },
            font: {
                color: isDark ? '#F7F9FC' : '#111827',
                size: 14,
                face: 'Arial'
            },
            borderWidth: 2,
            borderWidthSelected: 3
        }));

        // Prepare edges with vis.js format
        const edges = graphData.edges.map(edge => ({
            from: edge.from,
            to: edge.to,
            arrows: {
                to: {
                    enabled: true,
                    scaleFactor: 0.8
                }
            },
            color: {
                color: isDark ? '#94A3B8' : '#6B7280',
                highlight: '#6C63FF',
                hover: '#00C2A8'
            },
            width: edge.weight || 2,
            smooth: {
                enabled: true,
                type: 'continuous',
                roundness: 0.5
            },
            label: edge.label || '',
            font: {
                color: isDark ? '#CBD5E1' : '#6B7280',
                size: 11,
                align: 'middle',
                background: isDark ? '#1E293B' : '#FFFFFF',
                strokeWidth: 0
            }
        }));

        // Create vis.js data structure
        const data = {
            nodes: new vis.DataSet(nodes),
            edges: new vis.DataSet(edges)
        };

        // Configure vis.js options
        const options = {
            nodes: {
                shape: 'circle',
                scaling: {
                    min: 20,
                    max: 40
                }
            },
            edges: {
                smooth: {
                    enabled: true,
                    type: 'continuous'
                }
            },
            physics: {
                enabled: true,
                stabilization: {
                    enabled: true,
                    iterations: 200,
                    updateInterval: 25
                },
                barnesHut: {
                    gravitationalConstant: -2000,
                    centralGravity: 0.3,
                    springLength: 150,
                    springConstant: 0.04,
                    damping: 0.09,
                    avoidOverlap: 0.5
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 200,
                zoomView: true,
                dragView: true,
                navigationButtons: true,
                keyboard: {
                    enabled: true,
                    bindToWindow: false
                }
            },
            layout: {
                improvedLayout: true,
                hierarchical: false
            }
        };

        // Create network
        this.network = new vis.Network(this.container, data, options);

        // Add event listeners
        this.network.on('stabilizationIterationsDone', () => {
            this.network.setOptions({ physics: { enabled: false } });
        });

        // Handle theme changes
        this.setupThemeListener();
    }

    renderEmptyState() {
        this.container.innerHTML = `
            <div class="empty-state">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7">
                    </path>
                </svg>
                <p>No causal relationships detected</p>
            </div>
        `;
    }

    setupThemeListener() {
        // Listen for theme changes and re-render if needed
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
                    // Theme changed - could re-render graph with new colors if needed
                    // For now, we'll just note that the graph colors are set at render time
                }
            });
        });

        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['data-theme']
        });
    }

    destroy() {
        if (this.network) {
            this.network.destroy();
            this.network = null;
        }
    }
}

// Export for use in other modules
window.CausalGraphRenderer = CausalGraphRenderer;


// Bias Radar Chart Renderer
class BiasRadarChartRenderer {
    constructor() {
        this.canvas = document.getElementById('bias-radar-chart');
        this.chart = null;
    }

    render(biasData) {
        if (!this.canvas) return;

        // Check if there is bias data to display
        if (!biasData || !biasData.religion && !biasData.gender && !biasData.ethnicity) {
            this.renderEmptyState();
            return;
        }

        // Get current theme
        const theme = document.documentElement.getAttribute('data-theme') || 'light';
        const isDark = theme === 'dark';

        // Destroy existing chart if it exists
        if (this.chart) {
            this.chart.destroy();
        }

        // Prepare data for radar chart
        const data = {
            labels: ['Religion Bias', 'Gender Bias', 'Ethnicity Bias'],
            datasets: [{
                label: 'Bias Metrics',
                data: [
                    biasData.religion || 0,
                    biasData.gender || 0,
                    biasData.ethnicity || 0
                ],
                backgroundColor: isDark 
                    ? 'rgba(108, 99, 255, 0.3)' 
                    : 'rgba(108, 99, 255, 0.2)',
                borderColor: isDark 
                    ? '#6C63FF' 
                    : '#6C63FF',
                borderWidth: 2,
                pointBackgroundColor: '#00C2A8',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointHoverBackgroundColor: '#00C2A8',
                pointHoverBorderColor: '#FFFFFF',
                pointHoverBorderWidth: 3
            }]
        };

        // Configure chart options
        const options = {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 1.2,
            scales: {
                r: {
                    beginAtZero: true,
                    min: 0,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: isDark ? '#CBD5E1' : '#6B7280',
                        backdropColor: 'transparent',
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: isDark ? '#334155' : '#E5E7EB',
                        lineWidth: 1
                    },
                    angleLines: {
                        color: isDark ? '#334155' : '#E5E7EB',
                        lineWidth: 1
                    },
                    pointLabels: {
                        color: isDark ? '#F7F9FC' : '#111827',
                        font: {
                            size: 13,
                            weight: '600'
                        },
                        padding: 10
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: isDark ? '#1E293B' : '#FFFFFF',
                    titleColor: isDark ? '#F7F9FC' : '#111827',
                    bodyColor: isDark ? '#CBD5E1' : '#6B7280',
                    borderColor: isDark ? '#334155' : '#E5E7EB',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed.r.toFixed(1) + '%';
                        }
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                intersect: false
            }
        };

        // Create the radar chart
        this.chart = new Chart(this.canvas, {
            type: 'radar',
            data: data,
            options: options
        });

        // Setup theme listener
        this.setupThemeListener();
    }

    renderEmptyState() {
        // Hide canvas and show empty state
        const container = this.canvas.parentElement;
        if (!container) return;

        this.canvas.style.display = 'none';

        // Check if empty state already exists
        let emptyState = container.querySelector('.empty-state');
        if (!emptyState) {
            emptyState = document.createElement('div');
            emptyState.className = 'empty-state';
            emptyState.innerHTML = `
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                    </path>
                </svg>
                <p>No bias metrics detected</p>
            `;
            container.appendChild(emptyState);
        }
    }

    setupThemeListener() {
        // Listen for theme changes and re-render chart
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
                    // Re-render chart with new theme colors
                    if (this.chart && this.chart.data) {
                        const theme = document.documentElement.getAttribute('data-theme') || 'light';
                        const isDark = theme === 'dark';

                        // Update dataset colors
                        this.chart.data.datasets[0].backgroundColor = isDark 
                            ? 'rgba(108, 99, 255, 0.3)' 
                            : 'rgba(108, 99, 255, 0.2)';
                        this.chart.data.datasets[0].borderColor = '#6C63FF';

                        // Update scale colors
                        this.chart.options.scales.r.ticks.color = isDark ? '#CBD5E1' : '#6B7280';
                        this.chart.options.scales.r.grid.color = isDark ? '#334155' : '#E5E7EB';
                        this.chart.options.scales.r.angleLines.color = isDark ? '#334155' : '#E5E7EB';
                        this.chart.options.scales.r.pointLabels.color = isDark ? '#F7F9FC' : '#111827';

                        // Update tooltip colors
                        this.chart.options.plugins.tooltip.backgroundColor = isDark ? '#1E293B' : '#FFFFFF';
                        this.chart.options.plugins.tooltip.titleColor = isDark ? '#F7F9FC' : '#111827';
                        this.chart.options.plugins.tooltip.bodyColor = isDark ? '#CBD5E1' : '#6B7280';
                        this.chart.options.plugins.tooltip.borderColor = isDark ? '#334155' : '#E5E7EB';

                        // Update chart
                        this.chart.update();
                    }
                }
            });
        });

        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['data-theme']
        });
    }

    destroy() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
        
        // Show canvas again
        if (this.canvas) {
            this.canvas.style.display = 'block';
        }
    }
}

// Export for use in other modules
window.BiasRadarChartRenderer = BiasRadarChartRenderer;


// Demo test function for causal graph (for development/testing)
function testCausalGraph() {
    const mockGraphData = {
        nodes: [
            { id: 1, label: 'Muslims', size: 30 },
            { id: 2, label: 'Terrorists', size: 25 },
            { id: 3, label: 'Violence', size: 28 },
            { id: 4, label: 'Threat', size: 22 },
            { id: 5, label: 'Society', size: 26 }
        ],
        edges: [
            { from: 1, to: 2, label: 'causes', weight: 3 },
            { from: 2, to: 3, label: 'leads to', weight: 2 },
            { from: 3, to: 4, label: 'creates', weight: 2 },
            { from: 4, to: 5, label: 'affects', weight: 2 },
            { from: 1, to: 4, label: 'implies', weight: 1 }
        ]
    };

    const renderer = new CausalGraphRenderer();
    renderer.render(mockGraphData);
    
    // Show the results dashboard
    const dashboard = document.getElementById('results-dashboard');
    if (dashboard) {
        dashboard.style.display = 'block';
    }
}

// Demo test function for bias radar chart (for development/testing)
function testBiasChart() {
    const mockBiasData = {
        religion: 75.5,
        gender: 45.2,
        ethnicity: 62.8
    };

    const renderer = new BiasRadarChartRenderer();
    renderer.render(mockBiasData);
    
    // Show the results dashboard
    const dashboard = document.getElementById('results-dashboard');
    if (dashboard) {
        dashboard.style.display = 'block';
    }
}

// Make test functions available globally for console testing
window.testCausalGraph = testCausalGraph;
window.testBiasChart = testBiasChart;


// Risk Score Renderer
class RiskScoreRenderer {
    constructor() {
        this.scoreValue = document.getElementById('risk-score-value');
        this.scoreBadge = document.getElementById('risk-score-badge');
        this.lexicalPercentage = document.getElementById('lexical-percentage');
        this.lexicalProgress = document.getElementById('lexical-progress');
        this.causalPercentage = document.getElementById('causal-percentage');
        this.causalProgress = document.getElementById('causal-progress');
        this.biasPercentage = document.getElementById('bias-percentage');
        this.biasProgress = document.getElementById('bias-progress');
    }

    render(riskData) {
        if (!this.scoreValue || !this.scoreBadge) return;

        // Check if there is risk data to display
        if (!riskData || typeof riskData.score === 'undefined') {
            this.renderEmptyState();
            return;
        }

        // Extract data with defaults
        const score = Math.round(riskData.score || 0);
        const breakdown = riskData.breakdown || {
            lexical: 0,
            causal: 0,
            bias: 0
        };

        // Determine risk level based on score
        const riskLevel = this.getRiskLevel(score);

        // Animate score value
        this.animateScore(score);

        // Update risk badge
        this.updateRiskBadge(riskLevel);

        // Update breakdown percentages and animate progress bars
        this.updateBreakdown(breakdown);
    }

    getRiskLevel(score) {
        if (score >= 70) {
            return { level: 'High Risk', className: 'high' };
        } else if (score >= 40) {
            return { level: 'Medium Risk', className: 'medium' };
        } else {
            return { level: 'Low Risk', className: 'low' };
        }
    }

    animateScore(targetScore) {
        // Animate score from 0 to target value
        const duration = 1500; // 1.5 seconds
        const startTime = performance.now();
        const startScore = 0;

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (ease-out cubic)
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentScore = Math.round(startScore + (targetScore - startScore) * easeOut);

            this.scoreValue.textContent = currentScore;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    updateRiskBadge(riskLevel) {
        this.scoreBadge.textContent = riskLevel.level;
        
        // Remove all risk level classes
        this.scoreBadge.classList.remove('low', 'medium', 'high');
        
        // Add the appropriate class
        this.scoreBadge.classList.add(riskLevel.className);
    }

    updateBreakdown(breakdown) {
        // Update lexical severity
        const lexicalValue = Math.round(breakdown.lexical || 0);
        if (this.lexicalPercentage) {
            this.lexicalPercentage.textContent = `${lexicalValue}%`;
        }
        if (this.lexicalProgress) {
            // Trigger animation by setting width after a small delay
            setTimeout(() => {
                this.lexicalProgress.style.width = `${lexicalValue}%`;
            }, 100);
        }

        // Update causal narrative
        const causalValue = Math.round(breakdown.causal || 0);
        if (this.causalPercentage) {
            this.causalPercentage.textContent = `${causalValue}%`;
        }
        if (this.causalProgress) {
            setTimeout(() => {
                this.causalProgress.style.width = `${causalValue}%`;
            }, 200);
        }

        // Update bias indicator
        const biasValue = Math.round(breakdown.bias || 0);
        if (this.biasPercentage) {
            this.biasPercentage.textContent = `${biasValue}%`;
        }
        if (this.biasProgress) {
            setTimeout(() => {
                this.biasProgress.style.width = `${biasValue}%`;
            }, 300);
        }
    }

    renderEmptyState() {
        // Reset to default values
        if (this.scoreValue) {
            this.scoreValue.textContent = '0';
        }
        if (this.scoreBadge) {
            this.scoreBadge.textContent = 'Low Risk';
            this.scoreBadge.classList.remove('medium', 'high');
            this.scoreBadge.classList.add('low');
        }

        // Reset breakdown
        if (this.lexicalPercentage) this.lexicalPercentage.textContent = '0%';
        if (this.lexicalProgress) this.lexicalProgress.style.width = '0%';
        if (this.causalPercentage) this.causalPercentage.textContent = '0%';
        if (this.causalProgress) this.causalProgress.style.width = '0%';
        if (this.biasPercentage) this.biasPercentage.textContent = '0%';
        if (this.biasProgress) this.biasProgress.style.width = '0%';
    }

    reset() {
        // Reset all values to 0 without animation
        if (this.scoreValue) {
            this.scoreValue.textContent = '0';
        }
        if (this.scoreBadge) {
            this.scoreBadge.textContent = 'Low Risk';
            this.scoreBadge.classList.remove('medium', 'high');
            this.scoreBadge.classList.add('low');
        }

        // Reset breakdown immediately
        if (this.lexicalPercentage) this.lexicalPercentage.textContent = '0%';
        if (this.lexicalProgress) {
            this.lexicalProgress.style.transition = 'none';
            this.lexicalProgress.style.width = '0%';
            // Re-enable transition after reset
            setTimeout(() => {
                this.lexicalProgress.style.transition = '';
            }, 50);
        }

        if (this.causalPercentage) this.causalPercentage.textContent = '0%';
        if (this.causalProgress) {
            this.causalProgress.style.transition = 'none';
            this.causalProgress.style.width = '0%';
            setTimeout(() => {
                this.causalProgress.style.transition = '';
            }, 50);
        }

        if (this.biasPercentage) this.biasPercentage.textContent = '0%';
        if (this.biasProgress) {
            this.biasProgress.style.transition = 'none';
            this.biasProgress.style.width = '0%';
            setTimeout(() => {
                this.biasProgress.style.transition = '';
            }, 50);
        }
    }
}

// Export for use in other modules
window.RiskScoreRenderer = RiskScoreRenderer;


// Demo test function for risk score (for development/testing)
function testRiskScore() {
    const mockRiskData = {
        score: 78.5,
        breakdown: {
            lexical: 85,
            causal: 72,
            bias: 68
        }
    };

    const renderer = new RiskScoreRenderer();
    renderer.render(mockRiskData);
    
    // Show the results dashboard
    const dashboard = document.getElementById('results-dashboard');
    if (dashboard) {
        dashboard.style.display = 'block';
    }
}

// Make test function available globally for console testing
window.testRiskScore = testRiskScore;


// Demo Controller - Main orchestrator for demo page functionality
class DemoController {
    constructor() {
        // DOM elements
        this.textInput = document.getElementById('text-input');
        this.languageSelector = document.getElementById('language-selector');
        this.analyzeBtn = document.getElementById('analyze-btn');
        this.resetBtn = document.getElementById('reset-btn');
        this.resultsDashboard = document.getElementById('results-dashboard');
        
        // Controllers and renderers
        this.loadingController = new LoadingAnimationController();
        this.hateWordsRenderer = new HateWordsRenderer();
        this.causalGraphRenderer = new CausalGraphRenderer();
        this.biasChartRenderer = new BiasRadarChartRenderer();
        this.riskScoreRenderer = new RiskScoreRenderer();
        
        // State
        this.isAnalyzing = false;
        
        this.init();
    }

    init() {
        if (!this.analyzeBtn || !this.resetBtn) return;

        // Bind event listeners
        this.analyzeBtn.addEventListener('click', () => this.handleAnalyze());
        this.resetBtn.addEventListener('click', () => this.handleReset());
        
        // Handle Enter key in textarea (Ctrl+Enter to analyze)
        if (this.textInput) {
            this.textInput.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter' && !this.analyzeBtn.disabled) {
                    this.handleAnalyze();
                }
            });
        }
    }

    async handleAnalyze() {
        // Prevent multiple simultaneous analyses
        if (this.isAnalyzing) return;

        // Get input values
        const text = this.textInput?.value.trim();
        const language = this.languageSelector?.value || 'en';

        // Validate input (should already be validated by InputValidator, but double-check)
        if (!text) {
            return;
        }

        // Set analyzing state
        this.isAnalyzing = true;
        this.analyzeBtn.disabled = true;

        try {
            // Show loading animation
            this.loadingController.show();

            // Call API (or use mock data for now)
            const results = await this.analyzeText(text, language);

            // Hide loading animation
            this.loadingController.hide();

            // Render results
            this.renderResults(results);

            // Show results dashboard
            this.showResultsDashboard();

        } catch (error) {
            console.error('Analysis error:', error);
            this.loadingController.hide();
            this.showError('An error occurred during analysis. Please try again.');
        } finally {
            // Reset analyzing state
            this.isAnalyzing = false;
            this.analyzeBtn.disabled = false;
        }
    }

    async analyzeText(text, language) {
        // Simulate API call with delay
        await this.delay(3000);

        // Return mock data for testing
        // TODO: Replace with actual API call when backend is ready
        return this.getMockResults(text, language);
    }

    getMockResults(text, language) {
        // Generate mock results based on input
        const textLength = text.length;
        const wordCount = text.split(/\s+/).length;

        // Mock hate words detection
        const hateWords = [
            { word: 'terrorist', severity: 'High', context: 'Used in derogatory context' },
            { word: 'threat', severity: 'Medium', context: 'Implies danger or harm' },
            { word: 'inferior', severity: 'Medium', context: 'Dehumanizing language' },
            { word: 'extremist', severity: 'High', context: 'Stereotyping language' }
        ];

        // Mock causal graph
        const causalGraph = {
            nodes: [
                { id: 1, label: 'Group A', size: 30 },
                { id: 2, label: 'Negative Trait', size: 25 },
                { id: 3, label: 'Harmful Action', size: 28 },
                { id: 4, label: 'Threat', size: 22 },
                { id: 5, label: 'Society', size: 26 }
            ],
            edges: [
                { from: 1, to: 2, label: 'associated with', weight: 3 },
                { from: 2, to: 3, label: 'leads to', weight: 2 },
                { from: 3, to: 4, label: 'creates', weight: 2 },
                { from: 4, to: 5, label: 'affects', weight: 2 },
                { from: 1, to: 4, label: 'implies', weight: 1 }
            ]
        };

        // Mock bias metrics (vary based on text length for demo purposes)
        const biasMetrics = {
            religion: Math.min(95, 60 + (textLength % 35)),
            gender: Math.min(90, 40 + (wordCount % 50)),
            ethnicity: Math.min(85, 50 + ((textLength + wordCount) % 35))
        };

        // Mock risk score (calculated from bias metrics)
        const avgBias = (biasMetrics.religion + biasMetrics.gender + biasMetrics.ethnicity) / 3;
        const riskScore = {
            score: Math.round(avgBias),
            breakdown: {
                lexical: Math.min(100, Math.round(avgBias * 1.1)),
                causal: Math.min(100, Math.round(avgBias * 0.95)),
                bias: Math.min(100, Math.round(avgBias))
            }
        };

        return {
            hateWords,
            causalGraph,
            biasMetrics,
            riskScore,
            metadata: {
                language,
                textLength,
                wordCount,
                timestamp: new Date().toISOString()
            }
        };
    }

    renderResults(results) {
        // Render each component with the results data
        if (results.hateWords) {
            this.hateWordsRenderer.render(results.hateWords);
        }

        if (results.causalGraph) {
            this.causalGraphRenderer.render(results.causalGraph);
        }

        if (results.biasMetrics) {
            this.biasChartRenderer.render(results.biasMetrics);
        }

        if (results.riskScore) {
            this.riskScoreRenderer.render(results.riskScore);
        }
    }

    showResultsDashboard() {
        if (this.resultsDashboard) {
            this.resultsDashboard.style.display = 'block';
            
            // Scroll to results with smooth animation
            setTimeout(() => {
                this.resultsDashboard.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }, 100);
        }
    }

    hideResultsDashboard() {
        if (this.resultsDashboard) {
            this.resultsDashboard.style.display = 'none';
        }
    }

    handleReset() {
        // Clear input fields
        if (this.textInput) {
            this.textInput.value = '';
            this.textInput.focus();
        }

        if (this.languageSelector) {
            this.languageSelector.value = 'en';
        }

        // Hide results dashboard
        this.hideResultsDashboard();

        // Reset all renderers
        this.riskScoreRenderer.reset();
        
        // Destroy chart and graph instances to free memory
        if (this.biasChartRenderer.chart) {
            this.biasChartRenderer.destroy();
        }
        
        if (this.causalGraphRenderer.network) {
            this.causalGraphRenderer.destroy();
        }

        // Clear hate words table
        const hateWordsContent = document.getElementById('hate-words-content');
        if (hateWordsContent) {
            hateWordsContent.innerHTML = '';
        }

        // Scroll back to top of input panel
        const inputPanel = document.querySelector('.input-panel');
        if (inputPanel) {
            inputPanel.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }
    }

    showError(message) {
        // Display error message to user
        // Could be enhanced with a toast notification or modal
        alert(message);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize DemoController when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on demo page
    if (document.querySelector('.demo-page')) {
        const demoController = new DemoController();
        
        // Make it available globally for debugging
        window.demoController = demoController;
    }
});
