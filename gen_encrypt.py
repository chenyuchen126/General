# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 11:03:34 2022

將Server上面的設備資訊加密。

@author: Chris

"""

import json
import pathlib
import logging
import encrypt as enc 

# log 設定
FORMAT='%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT='%Y%m%d %H:%M:%S'
main_dir=pathlib.Path(__file__).parent.absolute()
logging.basicConfig(level=logging.DEBUG, 
                    filename = '{}/log/gen_encrypt.log'.format(main_dir), 
                    filemode = 'w', 
                    format = FORMAT, 
                    datefmt = DATE_FORMAT)

get_list = ["ip", "port", "user", "password", "database", "source", "sid"]

# Json格式沒有'，所以使用"雙引號
def replace_json(ans):
    return ans.strip().replace('\"','').replace("'",'"')

# 打開原始未加密的檔案
def read_plain_code(file_input_name):
    # 最後準備輸出的dict
    out = {}
    with open(file_input_name,'r', encoding='utf-8') as f:
        data = json.load(f)
        # 將所有 conn_info 的 key 取出
        db_key = data.keys()
        value = ""
        for db in db_key:
            ans = {}
            for name in get_list:
                dict_value = data.get(str(db)).get(str(name))
                if dict_value == None:
                    # 不適 ORACLE 沒有 SID 輸出 log
                    logging.info("{} is not oracle db !".format(db)) 
                    # 確認型態是否為list
                elif isinstance(dict_value,list):
                    value1 = dict_value[0]
                    value2 = dict_value[1]
                    # 例外處理list
                    value = [replace_json(str(enc.enctry(value1)).replace("b'", '"')),
                             replace_json(str(enc.enctry(value2)).replace("b'", '"'))]
                else:
                    value = replace_json(str(enc.enctry(dict_value)).replace("b'", '"'))
                # loop get_list 將 value 加密
                ans[name] = value
            # 更新到dict裡面
            out.update({db:ans})
    return out
# 檔案輸出
def output_json(file_output_name, output):
    with open (file_output_name, 'w', newline='') as fp:
        fp.write(json.dumps(output, indent=4))

# 主程式
def main(file_input_name, file_output_name):
    results=read_plain_code(file_input_name)
    output_json(file_output_name, results)

if __name__ == '__main__':
    # 輸入輸出路徑
    file_input_name = "{}/conn_before.json".format(main_dir)
    file_output_name = "{}/conn.json".format(main_dir)
    main(file_input_name, file_output_name)
