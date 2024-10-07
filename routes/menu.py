import shutil
import tempfile
import threading
import time
from flask import Flask, send_file, send_from_directory, current_app, request, jsonify, render_template, redirect, url_for, flash, session
from . import routes
from .db import User, RsyncJob, db, StackRsyncJob
from datetime import datetime
import os

@routes.route('/backupManage', methods=['GET', 'POST'])
def backupManage():
    page = request.args.get('page', 1, type=int)  # Lấy trang hiện tại từ URL (nếu không có thì mặc định là trang 1)
    per_page = 5  # Số bản ghi trên mỗi trang
    pagination = RsyncJob.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Lấy danh sách các bản ghi của trang hiện tại
    rsync_jobs = pagination.items
    
    return render_template('./dashboard/manageBackup.html', rsync_jobs=rsync_jobs, pagination=pagination)

@routes.route('/start_backup/<int:job_id>', methods=['POST'])
def start_backup(job_id):
    job = RsyncJob.query.get_or_404(job_id)
    
    # Get the last StackRsyncJob ID and calculate the next stack ID
    last_stack_job = StackRsyncJob.query.order_by(StackRsyncJob.id.desc()).first()
    next_stack_id = (last_stack_job.id + 1) if last_stack_job else 1
    
    # Modify the destination path to include the next stack ID for differentiation
    modified_dest_path = os.path.join(job.dest_path, f"backup_{next_stack_id}")
    
    # Example command incorporating the stack ID
    rsync_command = f"rsync -avz -e 'ssh -p {job.ssh_port}' {job.source_user}@{job.source_host}:{job.source_path} {modified_dest_path}"
    
    # Output for debugging/logging
    print(f"Starting backup job {job_id} with rsync command: {rsync_command}")
    execute_rsync_command = os.system(rsync_command)
    stack_job = StackRsyncJob(
        commandLine=rsync_command,
        completed=True
    )
    db.session.add(stack_job)
    db.session.commit()

    flash(f"Backup job {job_id} started successfully with stack ID {next_stack_id}.", "success")
    return redirect(url_for('routes.backupManage'))



@routes.route('/rsync/add', methods=['POST'])
def add_rsync_job():
    name_rent = request.form['name_rent']
    source_user = request.form['source_user']
    source_host = request.form['source_host']
    source_path = request.form['source_path']
    dest_path = request.form['dest_path'] + name_rent.replace(" ","_")
    ssh_port = request.form['ssh_port']
    backuptime = request.form['schedule_type']

    new_job = RsyncJob(
        name_rent=name_rent,
        source_user=source_user,
        source_host=source_host,
        source_path=source_path,
        dest_path=dest_path,
        ssh_port=ssh_port,
        backuptime=backuptime
    )

    db.session.add(new_job)
    db.session.commit()

    return redirect(url_for('routes.backupManage'))

@routes.route('/rsync/delete/<int:job_id>', methods=['POST'])
def delete_rsync_job(job_id):
    job = RsyncJob.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('routes.backupManage'))


def stackRsyncJob():
    with current_app.app_context():
        now = datetime.now()
        rsync_jobs = RsyncJob.query.all()
        
        last_stack_job = StackRsyncJob.query.order_by(StackRsyncJob.id.desc()).first()
        next_stack_id = (last_stack_job.id + 1) if last_stack_job else 1

        for job in rsync_jobs:
            if job.completed:
                continue

            command = None
            print("Run...")
            if job.backuptime == "daily" and now.hour == 0 and now.minute == 0:
                print("Thực Thi Rsync -----")
                command = f"rsync -avz -e 'ssh -p {job.ssh_port}' {job.source_user}@{job.source_host}:{job.source_path} {job.dest_path}/{next_stack_id}"

            elif job.backuptime == "hằng tuần" and now.weekday() == 6 and now.hour == 0 and now.minute == 0:
                command = f"rsync -avz -e 'ssh -p {job.ssh_port}' {job.source_user}@{job.source_host}:{job.source_path} {job.dest_path}/{next_stack_id}"

            elif job.backuptime == "hằng tháng" and now.day == 1 and now.hour == 0 and now.minute == 0:
                command = f"rsync -avz -e 'ssh -p {job.ssh_port}' {job.source_user}@{job.source_host}:{job.source_path} {job.dest_path}/{next_stack_id}"
            print(command)
            if command:
                stack_job = StackRsyncJob(commandLine=command)
                db.session.add(stack_job)
                db.session.commit()
                next_stack_id += 1

def rsync_scheduler_loop(app):
    with app.app_context():
        while True:
            print("Checking for rsync jobs...")
            now = datetime.now()
            if now.hour == 23 and now.minute == 36:
                print("Thực Thi Rsync")
                stackRsyncJob()
            time.sleep(60)  # Sleep for 60 seconds between checks

def threading_resync_scheduler_loop(app):
    thread = threading.Thread(target=rsync_scheduler_loop, args=(app,))
    thread.daemon = True
    thread.start()
