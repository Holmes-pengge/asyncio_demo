import json
import socket
import time

from pythonping import ping

"""  
{
        "domains": [{
                "url": "www.baidu.com",
                "isalvie": 0,
                "finalurl": ""

        }, {
                "url": "www.sina.com",
                "isalvie": 1,
                "finalurl": "https://www.sina.com"
        }]
}
"""


# def ping_domain(domain):
#     resp = ping(domain, count=4, size=10)
#     print(resp)
#     if 'Round Trip Times min/avg/max is' in resp:


def ping_domain(filename):
    # 读取域名文件
    result_ls = []
    with open(filename, 'r', encoding='gb18030', errors='ignore') as fp:
        for line in fp.readlines():
            host = line.strip()
            item = {}
            try:
                ip = socket.gethostbyname(host)
                resp = ping(ip, timeout=2, count=4, size=10, df=False)
                if resp.success():
                    print(host)
                    item = {
                        "url": host,
                        "isalvie": 1,
                        "finalurl": "https://{}".format(host),
                    }
            # except AttributeError as exc:
            #     # with open('fail_domain.txt', 'a') as f:
            #     #     f.write(line)
            #     item = {
            #         "url": host,
            #         "isalvie": 0,
            #         "finalurl": "",
            #     }
            # except socket.gaierror as err:
            #     # with open('fail_domain.txt', 'a') as f:
            #     #     f.write(line)
            #     item = {
            #         "url": host,
            #         "isalvie": 0,
            #         "finalurl": "",
            #     }
            # except socket.error as err:
            #     # with open('fail_domain.txt', 'a') as f:
            #     #     f.write(line)
            #     item = {
            #         "url": host,
            #         "isalvie": 0,
            #         "finalurl": "",
            #     }

            except Exception as exc:
                item = {
                    "url": host,
                    "isalvie": 0,
                    "finalurl": "",
                }
            # finally:
            result_ls.append(item)
    print(result_ls)
    with open('domain.txt', 'w') as f:
        f.write(json.dumps(result_ls))
    # ping_domain('www.baidrrrru.com')
    # ping_domain('www.baidu.com')
    # ping_domain('www.sina123456.com')


def main():
    # filename = r'D:\tmp\unclass_test'
    filename = r'D:\tmp\unclass'
    ping_domain(filename)


if __name__ == '__main__':
    # filename = r'D:\tmp\unclass_test'
    # # main(filename)
    # ls = [{'url': 'zhyww.cn', 'isalvie': 1, 'finalurl': 'https://zhyww.cn'}, {'url': 'btrchina.com', 'isalvie': 1, 'finalurl': 'https://btrchina.com'}, {'url': 'xjfzb.com', 'isalvie': 0, 'finalurl': ''}, {'url': 'hb96365.com', 'isalvie': 1, 'finalurl': 'https://hb96365.com'}, {'url': 'ruikeos.com', 'isalvie': 1, 'finalurl': 'https://ruikeos.com'}, {'url': 'qcloudcdn.com', 'isalvie': 0, 'finalurl': ''}, {'url': 'lswhj.top', 'isalvie': 0, 'finalurl': ''}, {'url': 'gzsrs.cn', 'isalvie': 1, 'finalurl': 'https://gzsrs.cn'}, {'url': 'tengda.fun', 'isalvie': 1, 'finalurl': 'https://tengda.fun'}, {'url': 'sqzsb.com', 'isalvie': 1, 'finalurl': 'https://sqzsb.com'}, {'url': 'djymedia.com', 'isalvie': 1, 'finalurl': 'https://djymedia.com'}, {'url': 'pzdlawyer.cn', 'isalvie': 1, 'finalurl': 'https://pzdlawyer.cn'}, {}, {'url': 'gzedu.com', 'isalvie': 1, 'finalurl': 'https://gzedu.com'}, {'url': 'boaiyun.cn', 'isalvie': 1, 'finalurl': 'https://boaiyun.cn'}, {'url': 'gzredcross.cn', 'isalvie': 1, 'finalurl': 'https://gzredcross.cn'}, {'url': 'gzhrsaas.com', 'isalvie': 0, 'finalurl': ''}, {}, {}, {}, {}, {'url': 'canc.com.cn', 'isalvie': 1, 'finalurl': 'https://canc.com.cn'}, {'url': 'mninfo.cn', 'isalvie': 0, 'finalurl': ''}, {'url': 'eeioe.com', 'isalvie': 0, 'finalurl': ''}, {}, {}, {'url': 'sltv.net', 'isalvie': 1, 'finalurl': 'https://sltv.net'}, {'url': 'tpdz.net.cn', 'isalvie': 0, 'finalurl': ''}]
    # with open('domain.json', 'w') as f:
    #     f.write(json.dumps(ls))
    start_time = time.time()
    main()
    print(time.time() - start_time)

# 1. 还有异常没能捕获到
# 2. 设置了 timeout=2，可是有的domain 等待时间却超过 2s
