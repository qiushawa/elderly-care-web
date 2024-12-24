from functools import wraps
from flask import request, jsonify
def parameters(param_name, param_type, description, required=True):
    """
    A decorator to extract and validate parameters from a Flask request.
    """
    def decorator(func):
        if not hasattr(func, '_parameters'):
            func._parameters = []
        if required:
            desc =description+ " (必填)"
        else:
            desc = description + " (可選)"

        func._parameters.append({
            "name": param_name,
            "type": param_type,
            "description": desc,
        })

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract parameters from the request body
            body = request.json.get("body", {})
            if param_name not in body and required:
                return jsonify({
                    "success": False,
                    "error": f"Missing parameter: {param_name}"
                }), 400

            # Validate parameter type
            try:
                if param_name in body:
                    kwargs[param_name] = param_type(body[param_name])
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "error": f"Invalid type for parameter: {param_name}. Expected {param_type.__name__}"
                }), 400

            return func(*args, **kwargs)
        return wrapper
    return decorator

def url_parameters(param_name, param_type, description):
    """
    A decorator to extract and validate parameters from Flask URL arguments.
    """
    def decorator(func):
        if not hasattr(func, '_url_parameters'):
            func._url_parameters = []
        func._url_parameters.append({
            "name": param_name,
            "type": param_type,
            "description": description,
        })

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the parameter exists in URL arguments
            if param_name not in kwargs:
                return jsonify({
                    "success": False,
                    "error": f"Missing URL parameter: {param_name}"
                }), 400

            # Validate parameter type
            try:
                kwargs[param_name] = param_type(kwargs[param_name])
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "error": f"Invalid type for URL parameter: {param_name}. Expected {param_type.__name__}"
                }), 400

            return func(*args, **kwargs)
        return wrapper
    return decorator
def route_with_description(
    bp, rule, methods=['GET'], title = None, description=None, 
    example_response = {
            "message": "Response example",
            "success": "true"
        },
    **options):
    def decorator(func):
        endpoint = options.pop('endpoint', func.__name__) 
        @wraps(func)
        @bp.route(rule, endpoint=endpoint, methods=methods)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)
        
        # 設置額外的屬性
        
        wrapped_func.route = rule.replace("<", "{").replace(">", "}")
        wrapped_func.methods = methods
        wrapped_func.description = description
        wrapped_func.title = title
        wrapped_func.example_response = example_response
        return wrapped_func
    return decorator
def generate_route_metadata(route_func):
    """
    根據路由函數提取元數據，並格式化為指定的 JSON 結構。
    """
    if not hasattr(route_func, "route") or not hasattr(route_func, "methods"):
        raise ValueError("路由函數缺少必要的元數據屬性")

    # 提取描述與方法
    route_metadata = {
        "title": route_func.title or "No description provided",
        "description": route_func.description or "No description provided",
        "method": route_func.methods[0] if route_func.methods else "GET",
        "params": {},
        "request": {
            "body": {}
        },
        "response": route_func.example_response
        
    }
    
    # 提取參數
    if hasattr(route_func, "_parameters"):
        for param in route_func._parameters:
            name = param["name"]
            param_type = param["type"].__name__  # 獲取類型名稱
            description = param["description"]
            
            # 更新參數資訊
            route_metadata["params"][name] = {
                "type": param_type,
                "description": description
            }
            route_metadata["request"]["body"][name] = param_type
    
    # 提取 URL 參數
    if hasattr(route_func, "_url_parameters"):
        for param in route_func._url_parameters:
            name = param["name"]
            param_type = param["type"].__name__
            description = param["description"]
            # 更新參數資訊
            route_metadata["params"][name] = {
                "type": param_type,
                "description": description
            }
    return route_metadata
