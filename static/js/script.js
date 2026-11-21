// static/js/script.js

document.addEventListener('DOMContentLoaded', function () {
    // Analysis page handling
    const form = document.getElementById('analysis-form');
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            const payload = {};
            formData.forEach((value, key) => {
                payload[key] = value;
            });
            // Simple validation (ensure positive numbers)
            const numFields = ['total_bw_mhz', 'num_users', 'per_user_rate_mbps', 'snr_db'];
            for (const f of numFields) {
                if (isNaN(parseFloat(payload[f]))) {
                    alert('Please enter valid numbers for all numeric fields.');
                    return;
                }
            }
            try {
                const resp = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await resp.json();
                if (!data.success) {
                    alert('Error: ' + data.error);
                    return;
                }
                // Show results section
                const resultsSec = document.getElementById('results-section');
                resultsSec.classList.remove('d-none');
                // Populate summary table
                const tableDiv = document.getElementById('summary-table');
                const results = data.results;
                let html = `<table class="table table-dark table-striped"><thead><tr><th>Technique</th><th>Spectral Efficiency (bits/s/Hz)</th><th>Total Rate (Mbps)</th><th>User Capacity</th><th>Bandwidth Utilization (%)</th><th>Interference (%)</th><th>Score</th></tr></thead><tbody>`;
                for (const tech in results) {
                    const r = results[tech];
                    html += `<tr><td>${tech}</td><td>${r.spectral_efficiency_bpshz}</td><td>${r.total_rate_mbps}</td><td>${r.user_capacity}</td><td>${r.bandwidth_utilization_pct}</td><td>${r.interference_pct}</td><td>${r.performance_score}</td></tr>`;
                }
                html += `</tbody></table>`;
                tableDiv.innerHTML = html;
                // Prepare chart data
                const labels = Object.keys(results);
                const spectralData = labels.map(l => results[l].spectral_efficiency_bpshz);
                const rateData = labels.map(l => results[l].total_rate_mbps);
                const capacityData = labels.map(l => results[l].user_capacity);
                const bwUtilData = labels.map(l => results[l].bandwidth_utilization_pct);
                const radarData = labels.map(l => results[l].performance_score);
                // Destroy previous charts if exist
                if (window.charts) {
                    window.charts.forEach(c => c.destroy());
                }
                window.charts = [];
                // Spectral Efficiency Bar
                const ctx1 = document.getElementById('spectralChart').getContext('2d');
                window.charts.push(new Chart(ctx1, {
                    type: 'bar',
                    data: { labels, datasets: [{ label: 'Spectral Efficiency (bits/s/Hz)', data: spectralData, backgroundColor: '#00bcd4' }] },
                    options: { responsive: true, plugins: { title: { display: true, text: 'Spectral Efficiency Comparison' } } }
                }));
                // Total Rate Bar
                const ctx2 = document.getElementById('rateChart').getContext('2d');
                window.charts.push(new Chart(ctx2, {
                    type: 'bar',
                    data: { labels, datasets: [{ label: 'Total Rate (Mbps)', data: rateData, backgroundColor: '#2196f3' }] },
                    options: { responsive: true, plugins: { title: { display: true, text: 'Total Achievable Data Rate' } } }
                }));
                // User Capacity Bar
                const ctx3 = document.getElementById('capacityChart').getContext('2d');
                window.charts.push(new Chart(ctx3, {
                    type: 'bar',
                    data: { labels, datasets: [{ label: 'User Capacity', data: capacityData, backgroundColor: '#66bb6a' }] },
                    options: { responsive: true, plugins: { title: { display: true, text: 'User Capacity Comparison' } } }
                }));
                // Bandwidth Utilization Doughnut
                const ctx4 = document.getElementById('bandwidthChart').getContext('2d');
                window.charts.push(new Chart(ctx4, {
                    type: 'doughnut',
                    data: { labels, datasets: [{ label: 'Bandwidth Utilization (%)', data: bwUtilData, backgroundColor: ['#ffca28', '#ffa726', '#ff7043', '#26c6da', '#ab47bc'] }] },
                    options: { responsive: true, plugins: { title: { display: true, text: 'Bandwidth Utilization' } } }
                }));
                // Radar chart for performance score
                const ctx5 = document.getElementById('radarChart').getContext('2d');
                window.charts.push(new Chart(ctx5, {
                    type: 'radar',
                    data: { labels, datasets: [{ label: 'Performance Score', data: radarData, backgroundColor: 'rgba(0,188,212,0.2)', borderColor: '#00bcd4' }] },
                    options: { responsive: true, plugins: { title: { display: true, text: 'Overall Technique Comparison (Score)' } } }
                }));
                // Set download link
                const dlLink = document.getElementById('download-pdf');
                dlLink.href = `/download/report/${data.analysis_id}`;
            } catch (err) {
                console.error(err);
                alert('An error occurred while calculating.');
            }
        });
    }
    // History page deletion handlers (if present)
    const deleteBtns = document.querySelectorAll('.delete-analysis');
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', async function () {
            if (!confirm('Delete this analysis permanently?')) return;
            const id = this.dataset.id;
            await fetch(`/api/history/delete/${id}`, { method: 'POST' });
            location.reload();
        });
    });
    const clearBtn = document.getElementById('clear-history');
    if (clearBtn) {
        clearBtn.addEventListener('click', async function () {
            if (!confirm('Clear all history? This cannot be undone.')) return;
            await fetch('/api/history/clear', { method: 'POST' });
            location.reload();
        });
    }
});
