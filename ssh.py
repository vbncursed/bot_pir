def upload_file_to_server(ssh, local_file, remote_file):
    # Загружаем файл на удаленный сервер
    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_file)
    sftp.close()

def unpack_rar_file(ssh, remote_rar_file, remote_unpacked_files):
    # Распаковываем файл на удаленном сервере
    ssh.exec_command(f'unrar x {remote_rar_file} {remote_unpacked_files}')

def run_qgis_script(ssh, script_path):
    # Запуск скрипта QGIS для создания файла export.csv
    ssh.exec_command(f'python3 {script_path}')

def download_file_from_server(ssh, remote_file, local_file):
    # Загружаем файл с удаленного сервера
    sftp = ssh.open_sftp()
    sftp.get(remote_file, local_file)
    sftp.close()

def delete_file_on_server(ssh, remote_file):
    # Удаляем файл с удаленного сервера
    ssh.exec_command(f'rm {remote_file}')
