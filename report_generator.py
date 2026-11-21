from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import json

def generate_pdf_report(analysis_id, record, results, filepath):
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    margin = 0.5 * inch
    y = height - margin
    c.setFont('Helvetica-Bold', 16)
    c.drawString(margin, y, f"Multiple Access Techniques Comparison Report (ID: {analysis_id})")
    y -= 30
    c.setFont('Helvetica', 12)
    # Input parameters
    c.drawString(margin, y, "Input Parameters:")
    y -= 15
    params = [
        f"Total Bandwidth (MHz): {record['total_bw_mhz']}",
        f"Number of Users: {record['num_users']}",
        f"Per‑User Data Rate (Mbps): {record['per_user_rate_mbps']}",
        f"SNR (dB): {record['snr_db']}",
        f"Network Condition: {record['network_condition']}",
        f"Channel Model: {record['channel_model']}",
    ]
    for p in params:
        c.drawString(margin + 15, y, p)
        y -= 14
    y -= 10
    # Table header
    c.drawString(margin, y, "Results:")
    y -= 15
    col_titles = ["Technique", "Spectral Eff (bits/s/Hz)", "Total Rate (Mbps)", "User Cap", "BW Util (%)", "Interf (%)", "Score"]
    col_x = [margin, margin+80, margin+180, margin+260, margin+320, margin+400, margin+470]
    for i, title in enumerate(col_titles):
        c.drawString(col_x[i], y, title)
    y -= 12
    c.setLineWidth(0.5)
    c.line(margin, y+2, width - margin, y+2)
    y -= 10
    for tech, r in results.items():
        values = [
            tech,
            f"{r['spectral_efficiency_bpshz']}",
            f"{r['total_rate_mbps']}",
            str(r['user_capacity']),
            f"{r['bandwidth_utilization_pct']}",
            f"{r['interference_pct']}",
            f"{r['performance_score']}"
        ]
        for i, val in enumerate(values):
            c.drawString(col_x[i], y, val)
        y -= 14
        if y < margin:
            c.showPage()
            y = height - margin
    # Recommendation (best score)
    best_tech = max(results.items(), key=lambda kv: kv[1]['performance_score'])[0]
    y -= 20
    c.setFont('Helvetica-Bold', 12)
    c.drawString(margin, y, f"Recommended Technique: {best_tech}")
    y -= 15
    c.setFont('Helvetica', 12)
    c.drawString(margin, y, f"Based on the highest performance score among the evaluated techniques.")
    c.save()
