import requests
import time

def recognize_captcha(
    image_bytes: bytes, 
    api_url: str, 
    api_key: str, 
    timeout: float = 10.0
) -> dict:
    """
    调用ddddocr验证码识别API
    
    参数:
    image_bytes: 验证码图片的字节数据
    api_url: API端点URL
    api_key: API密钥
    timeout: 请求超时时间（秒）
    
    返回:
    {
        "success": bool,       # 请求是否成功
        "status_code": int,     # HTTP状态码
        "result": str,          # 识别结果（成功时）
        "client": str,          # 客户端名称（成功时）
        "error": str,           # 错误信息（失败时）
        "response_time": float  # 请求耗时（秒）
    }
    """
    start_time = time.time()
    result = {
        "success": False,
        "status_code": None,
        "result": None,
        "client": None,
        "error": None,
        "response_time": 0.0
    }
    
    try:
        # 设置请求头
        headers = {
            "api-key": api_key,
            "Content-Type": "application/octet-stream"
        }
        
        # 发送POST请求
        response = requests.post(
            url=api_url,
            headers=headers,
            data=image_bytes,
            timeout=timeout
        )
        
        # 记录响应时间
        result["response_time"] = time.time() - start_time
        result["status_code"] = response.status_code
        
        # 处理成功响应
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("status") == "success":
                result["success"] = True
                result["result"] = json_response.get("result", "")
                result["client"] = json_response.get("client", "")
                return result
        
        # 处理错误响应
        try:
            error_detail = response.json().get("detail", response.text)
        except:
            error_detail = response.text[:200]  # 截取部分错误文本
        
        result["error"] = f"API错误 ({response.status_code}): {error_detail}"
    
    except requests.exceptions.Timeout:
        result["error"] = "请求超时"
    except requests.exceptions.ConnectionError:
        result["error"] = "连接服务器失败"
    except requests.exceptions.RequestException as e:
        result["error"] = f"请求异常: {str(e)}"
    except Exception as e:
        result["error"] = f"处理响应时出错: {str(e)}"
    
    return result
