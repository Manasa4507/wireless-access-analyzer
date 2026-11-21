
import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from calculations import calculate_metrics
from database import init_db, insert_analysis, get_all_analyses, get_analysis, delete_analysis, clear_history

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'reports')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)

init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/techniques')
def techniques():
    return render_template('techniques.html')


@app.route('/comparison')
def comparison():
    return render_template('comparison.html')


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


@app.route('/results/<int:analysis_id>')
def results(analysis_id):
    record = get_analysis(analysis_id)

    if not record:
        return redirect(url_for('history'))

    record['results'] = json.loads(record['results'])
    return render_template('results.html', analysis=record)


@app.route('/history')
def history():
    analyses = get_all_analyses()

    for record in analyses:
        record['results'] = json.loads(record['results']) if record.get('results') else {}

    return render_template('history.html', analyses=analyses)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({'success': False, 'error': 'Invalid JSON input'}), 400

    required = [
        'total_bw_mhz',
        'num_users',
        'per_user_rate_mbps',
        'snr_db',
        'network_condition',
        'channel_model'
    ]

    missing = [field for field in required if field not in data]

    if missing:
        return jsonify({
            'success': False,
            'error': 'Missing fields: ' + ', '.join(missing)
        }), 400

    try:
        total_bw = float(data['total_bw_mhz'])
        num_users = int(data['num_users'])
        per_user = float(data['per_user_rate_mbps'])
        snr = float(data['snr_db'])
        network_condition = str(data['network_condition'])
        channel_model = str(data['channel_model'])

        if total_bw <= 0 or num_users <= 0 or per_user <= 0:
            return jsonify({
                'success': False,
                'error': 'Bandwidth, users and data rate must be greater than zero.'
            }), 400

        results = calculate_metrics(
            total_bw_mhz=total_bw,
            num_users=num_users,
            per_user_rate_mbps=per_user,
            snr_db=snr,
            network_condition=network_condition,
            channel_model=channel_model
        )

        analysis_id = insert_analysis(
            total_bw_mhz=total_bw,
            num_users=num_users,
            per_user_rate_mbps=per_user,
            snr_db=snr,
            network_condition=network_condition,
            channel_model=channel_model,
            results=json.dumps(results)
        )

        return jsonify({
            'success': True,
            'analysis_id': analysis_id,
            'results': results
        })

    except (ValueError, TypeError) as error:
        return jsonify({'success': False, 'error': str(error)}), 400

    except Exception:
        app.logger.exception('Calculation failed')
        return jsonify({
            'success': False,
            'error': 'Calculation failed. Check the application terminal.'
        }), 500


@app.route('/api/history/delete/<int:analysis_id>', methods=['POST'])
def api_delete_analysis(analysis_id):
    delete_analysis(analysis_id)
    return jsonify({'success': True})


@app.route('/api/history/clear', methods=['POST'])
def api_clear_history():
    clear_history()
    return jsonify({'success': True})


@app.route('/download/report/<int:analysis_id>')
def download_report(analysis_id):
    filename = f'report_{analysis_id}.pdf'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.isfile(filepath):
        from report_generator import generate_pdf_report

        record = get_analysis(analysis_id)

        if not record:
            return 'Analysis not found', 404

        results = json.loads(record['results'])
        generate_pdf_report(analysis_id, record, results, filepath)

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )


if __name__ == '__main__':
    app.config['DEBUG'] = False
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False
    )
