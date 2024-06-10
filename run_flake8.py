import os
import subprocess

# Enter your path here
project_path = r'C:\Users\Damien\PycharmProjects\echecs'

flake8_report_dir = os.path.join(project_path, 'flake8_rapport')

if not os.path.exists(flake8_report_dir):
    os.makedirs(flake8_report_dir)

flake8_command = [
    'flake8',
    '--max-line-length=119',
    '--format=html',
    f'--htmldir={flake8_report_dir}',
    os.path.join(project_path, 'controllers'),
    os.path.join(project_path, 'data'),
    os.path.join(project_path, 'models'),
    os.path.join(project_path, 'views'),
    os.path.join(project_path, 'Main.py'),
]

subprocess.run(flake8_command)
