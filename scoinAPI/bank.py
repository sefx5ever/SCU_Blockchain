import requests
import json

class Bank_Connection:
    def __init__(self,l='http://52.44.57.177:8888/'):
        """
        説明：初始化物件。

        變數：
            l : str（http://3.87.137.58:8888/） : 設定 IOTA API 鏈接
        """
        self.l = l

    def connection_test(self,l=None):
        """
        説明：測試 IOTA API 連綫。

        變數：
            l : str（None） : 設定 IOTA API 鏈接，若需切換其它鏈接，可只針對function進行輸入
        """
        if l == None:
            l = self.l
            
        r = requests.get(l)
        if r.status_code == 200:
            print('【connection_test】: Connection successfully!')
            return self.return_dict(status = True)
        else:
            print('【connection_test】: Connection failed!')
            self.return_dict(status = False)

    def create_did(self,name:str,password,method:str='light',l=None, \
                    description='Marmot Bank Member',pub_key:str=''):
        """
        説明：注冊 did 帳號

        變數：
            name        : str                       : 設定 did / 登錄使用
            l           : str（None）               : 設定 IOTA API 鏈接，若需切換其它鏈接，可只針對function進行輸入
            password    : str                       : 設定帳號密碼
            method      : str（light）              : 固定變數
            description : str（Marmot Bank Member） : 設定更多相關説明
            pub_key     : str（''）                 : 若有自訂 RSA hash 可進行設定
        """
        if l == None:
            l = self.l
            
        headers = { 
            "Content-Type" : "application/json" , 
            "X-API-key" : password
        }
        data = json.dumps(self.return_dict(
            method = method,
            name = name, 
            description = description, 
            pub_key = pub_key
        ))
        
        try:
            res = requests.post(l + 'new_did',headers = headers,data = data)
        
            if res.status_code == 200:
                print('【create_did】: Sign up successfully!')
                return self.return_dict(status = True,res_data = res.text)
            elif res.status_code == 409:
                print('【create_did】: Did was existed!')
            elif res.status_code == 400:
                print('【create_did】: Invalid format!')
            else:
                print('【create_did】: ', res.text)
        except Exception as e:
            print('【create_did】: ',e)
        return self.return_dict(status = False)

    def get_did(self,hash_:str,l=None):
        """
        説明：透過帳號 Hash 值獲取帳號内容

        變數：
            hash_ : str         : 設定帳號 Hash 值
            l     : str（None） : 設定 IOTA API 鏈接，若需切換其它鏈接，可只針對function進行輸入
        """
        if l == None:
            l = self.l
            
        payload = {
            'hash' : hash_
        }
        
        try:
            res = requests.get(l + 'did',params = payload)

            if res.text != '':
                res_data = json.loads(res.text)
                print('【get_did】: Get hash data successfully!')
                return self.return_dict(status = True,res_data = res_data)
            else:
                print('【get_did】: Did not found!')
        except Exception as e:
            print('【get_did】: ',e)
        return self.return_dict(status = False)

    def get_balance(self,name,l=None):
        """
        説明：透過帳號 did 獲取帳號 token 内容

        變數：
            name : str         : 設定帳號 did
            l    : str（None） : 設定 IOTA API 鏈接，若需切換其它鏈接，可只針對function進行輸入
        """
        if l == None:
            l = self.l
            

        payload = self.return_dict(user = name)
        
        try:
            res = requests.get(l + 'get_balance',params = payload)
            token = res.text.split('\n')
            print('【get_balance】: Get balance successfully!')
            if res.status_code == 200:
                return self.return_dict(
                    status = True,
                    res_data = self.return_dict(
                        status = True,
                        name = name,
                        token = token,
                        count = len(token)
                    )
                )
        except Exception as e:
            print('【get_balance】: ',e)
        return self.return_dict(status = False)

    def verify_token(self,password,name,token:str,l=None):
        """
        説明：驗證 token 是否為自身 token

        變數：
            password : str         : 設定帳號密碼
            name     : str         : 設定帳號 did
            token    ：str         : 需被驗證的 token 之 Hash 值            
            l        : str（None） : 設定 IOTA API 鏈接，若需切換其它鏈接，可只針對function進行輸入
        """
        if l == None:
            l = self.l
            
        headers = { 
            'Content-Type' : 'application/json', 
            'X-API-key' : password 
        }
        
        data = json.dumps(self.return_dict(
            user = name,
            token = token
        ))
        
        try:
            res = requests.post(l + 'verify_token',headers = headers,data = data)

            if res.status_code == 200:
                print('【verify_token】: Token valid!')
                return self.return_dict(status = True)
            elif res.status_code == 403:
                print('【verify_token】: Permission deny!')
            elif res.status_code == 400:
                print('【verify_token】: Token invalid!')
            else:
                print('【verify_token】: Function error!')
        except:
            print('【verify_token】: Requests error!')
        return self.return_dict(status = False)

    def send_token(self,password,sen,rev,num:int,layer:str,method=1, \
                    description="Marmot Bank Transaction",l=None):
        """
        説明：透過 token 之 Hash 值進行轉賬

        變數：
            layer       : str                            : 設定 SCoin 體系之層級
            password    : str                            : 設定帳號密碼
            sen         : str                            : 設定發送人
            rev         : str                            : 設定收款人 
            number      : int                            : 需要轉賬數量
            method      : str（1）                       ：設定交易類別
            description : str（Marmot Bank Transaction） ：設定交易説明
            l           : str（None）                    : 設定 IOTA API 鏈接，若需切換其它鏈接，可只針對function進行輸入
        """
        l = self.l if l == None else l

        headers = { 
            'Content-Type' : 'application/json', 
            'X-API-key' : password 
        }

        sen_data = self.get_balance(sen)
        if sen_data['status'] == True:
            token_list = sen_data['res_data']['token']
            if (token_list[0] == '') | (sen_data['res_data']['count'] < num):
                print('【send_token】: Account sender not enough amount!')
                return self.return_dict(status = False)

        try:
            result = list()
            print(token_list[:num])
            for txn in token_list[:num]:                
                data = json.dumps(self.return_dict(
                    sen = sen,
                    rev = rev,
                    method = layer,
                    description = description,
                    txn = '' if layer == '1' else txn
                ))
            
                res = requests.post(l + 'send_token',headers = headers,data = data)
                
                if res.status_code == 200:
                    print('【send_token】: Transaction sucessfully!')
                    result.append(self.return_dict(
                        sen = sen,
                        rev = rev,
                        new_txn_hash = res.text
                    ))
                elif res.status_code == 404:
                    print('【send_token】: Sendor and Receiver does not exist!')
                    return self.return_dict(status = False)
                elif res.status_code == 403:
                    print('【send_token】: Permission deny!')
                    return self.return_dict(status = False)
                else:
                    print('【send_token】: Function error!')
                    return self.return_dict(status = False)
            return self.return_dict(status = True,res_data = result)
        except Exception as e:
            print('【send_token】: ',e)
        return self.return_dict(status = False)

    def set_central_bank(self,password,name,l=None):
        """
        説明： 設定 did 帳號為央行權限

        變數：
            password  : str         : 設定帳號密碼
            name      : str         : 設定帳號 did
            l         : str（None） : 設定 IOTA API 鏈接，若需切換其它鏈接，可只針對function進行輸入
        """
        if l == None:
            l = self.l
            
        headers = { 'X-API-key' : password }
        payload = self.return_dict(username = name)
        
        try:
            res = requests.get(l + 'set_layer1',headers = headers,params = payload)
            
            if res.status_code == 200:
                print('【set_central_bank】: Set central bank successfully!')
                return self.return_dict(status = True)
            elif res.status_code == 400:
                print('【set_central_bank】: No such account or account already exist')
            elif res.status_code == 403:
                print('【set_central_bank】: Authentication fail!')
            else:
                print('【set_central_bank】: Function error!')
        except Exception as e:
            print('【set_central_bank】: ',e)
        return self.return_dict(status = False)

    def snapshot(self,password,user,token,l=None):
        if l == None:
            l = self.l

        pass

    def remove_layer1(self,l=None):
        if l == None:
            l = self.l
            
        pass

    def get_all_cluster(self,l=None):
        if l == None:
            l = self.l
            
        pass

    def bridge(self,l=None):
        if l == None:
            l = self.l
            
        pass

    def get_enseed(self,l=None):
        if l == None:
            l = self.l
            
        pass
        
    def get_transaction_by_timestamp(self,l=None):
        if l == None:
            l = self.l
            
        pass

    def get_user_by_timestamp(self,l=None):
        if l == None:
            l = self.l
            
        pass

    def info(self,l=None):
        if l == None:
            l = self.l
            
        pass

    @staticmethod
    def return_dict(**kwargs):
        return kwargs