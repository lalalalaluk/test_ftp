import ftplib
import datetime
import time


# 遠端 FTP 設定
FTP_HOST = ''
FTP_USERNAME = ''
FTP_PASSWORD = ''
is_remote = True


def create_folder_if_not_exists(ftp, folder):
    file_list = []
    ftp.dir(file_list.append)

    # 提取資料夾名稱
    folder_names = []
    for item in file_list:
        if item.startswith('d'):  # 只處理以 'd' 開頭的行，表示是資料夾
            folder_name = item.split()[-1]
            folder_names.append(folder_name)

    # 如果資料夾不存在，則創建新的資料夾
    if folder not in folder_names:
        if is_remote:
            ftp.mkd(folder + '_remote')
        else:
            ftp.mkd(folder + '_school')


def upload_file_to_ftp(filename):
    try:
        # 建立 FTP 連線
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USERNAME, FTP_PASSWORD)

        # 創建以當天日期為名稱的資料夾
        today = datetime.datetime.now().strftime('%Y-%m-%d')

        create_folder_if_not_exists(ftp, today)

        # 進入資料夾
        ftp.cwd(today)

        # 上傳檔案
        with open(filename, 'rb') as file:
            ftp.storbinary('STOR ' + filename, file)

        ftp.quit()
        print(f'檔案 {filename} 上傳成功')
    except Exception as e:
        print(f'檔案 {filename} 上傳失敗: {e}')


def main():
    while True:
        # 建立測試檔案，這裡以當前時間戳為檔名
        filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.txt')
        with open(filename, 'w') as file:
            file.write('')

        # 上傳檔案到 FTP
        upload_file_to_ftp(filename)

        # 每隔 5 秒執行一次
        time.sleep(5)


if __name__ == '__main__':
    main()
