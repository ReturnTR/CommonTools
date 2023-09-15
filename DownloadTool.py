from tqdm import tqdm
import requests
import wget
import sys
import asyncio
import logging
from tqdm.asyncio import tqdm
from multiprocessing import Pool

"""利用异步"""
async def download_file(url, save_path, proxy=None):
    import aiohttp
    try:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=proxy) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to download file: {url}, status: {response.status}")
                    total_size = int(response.headers.get('Content-Length', 0))
                    with open(save_path, 'wb') as f:
                        with tqdm(total=total_size, desc=save_path, unit='B', unit_scale=True) as pbar:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    break
                                f.write(chunk)
                                pbar.update(len(chunk))
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")
        return None

async def download_files(urls,save_dir,concurrency=4,proxy=None):
    global semaphore
    semaphore = asyncio.Semaphore(concurrency)

    tasks = [
        download_file(url, save_dir+url.split("/")[-1], proxy=proxy) for url in urls
    ]

    await asyncio.gather(*tasks, return_exceptions=True)

"""利用线程池"""
def multiprocess_data(data,fun,process_num):
    """使用多进程加速数据处理"""
    with Pool(processes = process_num) as pool:result = list(tqdm(pool.imap(fun, data), total=len(data)))
    return result

class DownloadInterface():

    def __init__(self,url,save_dir="./"):
        self.url=url
        self.save_filename=save_dir+url.split("/")[-1]
    def start(self):
        """开始下载"""
        pass

class DownloadRequests(DownloadInterface):
    """用Requests模块"""

    def start_simple(self):
        """简单下载，没有进度条"""
        f=requests.get(self.url)
        open(self.save_filename,'wb').write(f.content)

    def start(self):
        """流式下载，带进度条"""
        # 用流stream的方式获取url的数据
        resp = requests.get(self.url, stream=True)
        # 拿到文件的长度，并把total初始化为0
        total = int(resp.headers.get('content-length', 0))
        # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
        with open(self.save_filename, 'wb') as file, tqdm(
                desc=self.save_filename,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

class DownloadWget(DownloadInterface):
    """使用wegt模块，可以连外网"""
    def bar_pycharm(self, current, total, width=80):
        current_tell, total_tell = current, total
        unit=['B', 'K', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'BB', 'NB', 'DB']
        for i in unit: # 单位转换
            if current_tell >= 1024:
                current_tell = current_tell / 1024
            else:
                current_tell = format(round(current_tell, 2), ".2f") + i
                break
        for i in unit: # 单位转换
            if total_tell >= 1024:
                total_tell = total_tell / 1024
            else:
                total_tell = format(round(total_tell, 2), ".2f") + i
                break
        
        progress_message = "{:.2f}% |".format(current/total*100)+self.url + "|"+current_tell+"/"+total_tell+"\n"
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    def bar_adaptive(self,current, total, width=80):
        # 这段代码是wget库的bar_adaptive()函数所简单修改来的，这个只改了下载进度条显示下载单位的功能,
        # process special case when total size is unknown and return immediately
        if not total or total < 0:
            current_tell = current
            for i in ['B', 'K', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'BB', 'NB', 'DB']:  # 单位转换
                if current_tell >= 1024:
                    current_tell = current_tell / 1024
                else:
                    current_tell = format(round(current_tell, 2), ".2f") + i
                    break
            msg = "%s / unknown" % current_tell
            if len(msg) < width:  # leaves one character to avoid linefeed
                return msg
            if len("%s" % current) < width:
                return "%s" % current_tell

        # --- adaptive layout algorithm ---
        #
        # [x] describe the format of the progress bar
        # [x] describe min width for each data field
        # [x] set priorities for each element
        # [x] select elements to be shown
        #   [x] choose top priority element min_width < avail_width
        #   [x] lessen avail_width by value if min_width
        #   [x] exclude element from priority list and repeat

        #  10% [.. ]  10/100
        # pppp bbbbb sssssss
        min_width = {
            'percent': 4,  # 100%
            'bar': 3,  # [.]
            'size': len("%s" % total) * 2 + 3,  # 'xxxx / yyyy'
        }
        priority = ['percent', 'bar', 'size']

        # select elements to show
        selected = []
        avail = width
        for field in priority:
            if min_width[field] < avail:
                selected.append(field)
                avail -= min_width[field] + 1  # +1 is for separator or for reserved space at
                # the end of line to avoid linefeed on Windows
        # render
        output = ''
        for field in selected:

            if field == 'percent':
                # fixed size width for percentage
                output += ('%s%%' % (100 * current // total)).rjust(min_width['percent'])
            elif field == 'bar':  # [. ]
                # bar takes its min width + all available space
                # 这里需要注意一下,这段代码原来是wget库里面的，因此下面的部分也要加上，当然下面的可以去掉，它的作用只是显示[...]这样子的进度条
                output += wget.bar_thermometer(current, total, min_width['bar'] + avail)
            elif field == 'size':
                # size field has a constant width (min == max)
                # 显示实际的单位,默认值的单位是B
                # 下面的单位转换是笔者自己加的
                current_tell, total_tell = current, total
                for i in ['B', 'K', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'BB', 'NB', 'DB']:  # 单位转换
                    if current_tell >= 1024:
                        current_tell = current_tell / 1024
                    else:
                        current_tell = format(round(current_tell, 2), ".2f") + i
                        break
                for i in ['B', 'K', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'BB', 'NB', 'DB']:  # 单位转换
                    if total_tell >= 1024:
                        total_tell = total_tell / 1024
                    else:
                        total_tell = format(round(total_tell, 2), ".2f") + i
                        break
                output += ("%s / %s" % (current_tell, total_tell)).rjust(min_width['size'])

            selected = selected[1:]
            if selected:
                output += ' '  # add field separator
            print(self.url,end="")
        return output

    def start(self):
        wget.download(self.url,self.save_filename,bar=self.bar_pycharm)
        # while True:
        #     try:
        #         break
        #     except:
        #         print("失败重连!")

def download_fun(data):data[0](data[1],data[2]).start()
def download(urls,save_dir="./",mode=DownloadRequests,process_num=4):
    data=(list(range(len(urls))),urls,[save_dir]*len(urls))
    data=[(mode,data[1][i],data[2][i]) for i in range(len(data[0]))]
    multiprocess_data(data,download_fun,process_num)


if __name__=="__main__":

    urls=[
        "https://huggingface.co/THUDM/chatglm2-6b/resolve/main/pytorch_model-00001-of-00007.bin",
        "https://huggingface.co/THUDM/chatglm2-6b/resolve/main/pytorch_model-00002-of-00007.bin",
        "https://huggingface.co/THUDM/chatglm2-6b/resolve/main/pytorch_model-00003-of-00007.bin",
        "https://huggingface.co/THUDM/chatglm2-6b/resolve/main/pytorch_model-00004-of-00007.bin",
        "https://huggingface.co/THUDM/chatglm2-6b/resolve/main/pytorch_model-00005-of-00007.bin",
        "https://huggingface.co/THUDM/chatglm2-6b/resolve/main/pytorch_model-00006-of-00007.bin",
        "https://huggingface.co/THUDM/chatglm2-6b/resolve/main/pytorch_model-00007-of-00007.bin"
    ]
    urls = [
        "https://pic1.zhimg.com/v2-ebe33942ee48bbf0b09646204eabb6b8_b.webp",
        "https://pic1.zhimg.com/80/v2-108df3deb0eca1ef6435ea9c40238044_720w.webp",
        "https://pic1.zhimg.com/80/v2-65408c56293717fcb3edb5d526cca4b0_720w.webp",
        "https://pic1.zhimg.com/80/v2-27bfbe52bbaed34b0842d420fad5df60_720w.webp",
        "https://pic1.zhimg.com/80/v2-1ed4a64364af7d844296f2d793c1b0bc_720w.webp",
        "https://pic4.zhimg.com/80/v2-bf48141aee36663a1e5dd57f3fd609bf_720w.webp",
        "https://pic1.zhimg.com/80/v2-ef2b8893f187e6dd61bb3642364eeeb8_720w.webp",
        "https://pic3.zhimg.com/80/v2-d7d3ae6461a4b97b748182fcf96edaf6_720w.webp"
    ]
    save_dir="files"

    # 线程池
    download(urls,save_dir)
    # 异步
    # asyncio.run(download_files(urls,save_dir))


