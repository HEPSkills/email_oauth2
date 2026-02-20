#!/usr/bin/env python3
import sys
import os
import atexit
import msal
import logging

# ================= CONFIGURATION =================
# CERN Production Config
CLIENT_ID = "543725ae-fd38-436a-a717-009b1a8137be"
AUTHORITY = "https://login.microsoftonline.com/cern.ch"
# 必须加上 offline_access 才能拿到 Refresh Token，从而确保持久登录
SCOPES = [
    "https://outlook.office.com/IMAP.AccessAsUser.All",
    "https://outlook.office.com/SMTP.Send",
]
# Token 缓存文件路径 (建议放在脚本同目录下)
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token_cache.bin")
# =================================================

def get_token():
    # 1. 初始化 Token 缓存
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache.deserialize(f.read())

    # 2. 保存缓存的回调函数
    atexit.register(
        lambda: open(CACHE_FILE, "w").write(cache.serialize())
        if cache.has_state_changed else None
    )

    # 3. 创建 MSAL App
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache
    )

    result = None
    accounts = app.get_accounts()

    # 4. 尝试从缓存静默获取 Token
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    # 5. 如果缓存里没有，或者过期了，发起 Device Flow
    if not result:
        # 注意：这里我们把提示信息打印到 stderr，防止污染 stdout
        # Himalaya 只读取 stdout 作为 Token
        print("No suitable token in cache. Starting Device Flow...", file=sys.stderr)
        
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise ValueError("Fail to create device flow")

        print(f"\n{'-'*60}", file=sys.stderr)
        print(f"Please open: {flow['verification_uri']}", file=sys.stderr)
        print(f"Enter Code : {flow['user_code']}", file=sys.stderr)
        print(f"{'-'*60}\n", file=sys.stderr)
        
        # 阻塞等待用户在浏览器完成登录
        result = app.acquire_token_by_device_flow(flow)

    # 6. 输出结果
    if "access_token" in result:
        # 成功！只打印 Token 到标准输出
        print(result["access_token"], end="") 
    else:
        # 失败
        print(f"Error: {result.get('error')}", file=sys.stderr)
        print(f"Desc : {result.get('error_description')}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        get_token()
    except Exception as e:
        print(f"Script Error: {e}", file=sys.stderr)
        sys.exit(1)
